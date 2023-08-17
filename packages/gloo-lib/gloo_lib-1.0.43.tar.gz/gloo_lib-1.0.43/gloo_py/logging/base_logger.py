import asyncio
import atexit
import datetime
import os
import queue
import threading
import time
import typing
import uuid
from pydantic import BaseModel
import requests
from .payload import EventType, GlooLLMTaskDetails, GlooLoggerPayload, GlooTestContext
from ..env import global_api_key, global_gloo_service, base_context

T = typing.TypeVar("T", bound=BaseModel)
U = typing.TypeVar("U", bound=BaseModel)


import contextvars

test_context_var: contextvars.ContextVar[
    GlooTestContext | None
] = contextvars.ContextVar("test_context_var", default=None)

# This will act as the context for each coroutine.
active_contexts_var: contextvars.ContextVar[
    typing.List["GlooPipelineCtx"]
] = contextvars.ContextVar("active_contexts_var", default=[])

RETRIES = 1
TIMEOUT = 3 # seconds

class GlooTestCtx:
    def __init__(self, test_ctx: GlooTestContext) -> None:
        self.test_ctx = test_ctx

    # Asynchronous context manager methods
    async def __aenter__(self):
        test_context_var.set(self.test_ctx)

    async def __aexit__(self, exc_type, exc_value, traceback):
        test_context_var.set(None)

    # Regular context manager methods
    def __enter__(self):
        test_context_var.set(self.test_ctx)
        
    def __exit__(self, exc_type, exc_value, traceback):
        test_context_var.set(None)

class GlooPipelineCtx:
    def __init__(self, *, chainId: str, tags: typing.List[str] = []) -> None:
        self.chainId = chainId
        self.tags = tags

    async def __aenter__(self) -> "GlooPipelineCtx":
        contexts = active_contexts_var.get()
        contexts.append(self)
        active_contexts_var.set(contexts)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        contexts = active_contexts_var.get()
        contexts.pop()
        active_contexts_var.set(contexts)



def cleanup_function():
    logger.stop_worker()

atexit.register(cleanup_function)

class GlooLogger:
    _instance = None  # class variable to hold the instance

    def __new__(cls):
        # If an instance already exists, return it. Otherwise, create a new instance.
        if cls._instance is None:
            cls._instance = super(GlooLogger, cls).__new__(cls)
            # You can also initialize other attributes here, if needed
            cls._instance._initialized = False
        return cls._instance

    def __enter__(self):
        if self._worker_thread and self._worker_thread.is_alive():
            return self
        
        self._stop_worker_flag = False
        self._nest_level += 1

        self._worker_thread = threading.Thread(target=self._worker_thread_fn)
        # Set it as a daemon thread
        # self._worker_thread.daemon = True
        self._worker_thread.start()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._nest_level -= 1
        if self._nest_level == 0:
            self.stop_worker()

    def __init__(self):
        if self._initialized:
            return

        self.__context = None
        self._nest_level = 0

        # Create an async queue
        self._queue = queue.Queue[GlooLoggerPayload]()

        # Start the worker task# Start the worker task
        self._stop_worker_flag = False
        self.failed_log_attempts = 0
        self.dropped_logs = 0
        self._worker_thread = None


        self._lock = threading.Lock() # async lock for counters

        self._initialized = True
    

    def stop_worker(self):
        if self._worker_thread and self._worker_thread.is_alive():
            # Here, you'll need a mechanism to stop the loop gracefully
            # For simplicity, I'm going to use the sentinel value you had in the queue.
            self._stop_worker_flag = True
            self._worker_thread.join()
            self._worker_thread = None
            self.print_stats()

    @property
    def _context(self):
        if self.__context is None:
            self.__context = base_context()
        return self.__context


    async def __log_base(self, chainIds: typing.List[str], tags: typing.List[str], start_date: datetime.datetime = datetime.datetime.utcnow()):          
        request_id = str(uuid.uuid4())

        # Get test context
        test_context = test_context_var.get()

        # Get the active contexts for this coroutine.
        active_contexts = active_contexts_var.get()
        ctx_chains = [c.chainId for c in active_contexts] + chainIds
        ctx_tags = [t for c in active_contexts for t in c.tags]
        merged_tags = list(set(tags + ctx_tags))

        return {
            **self._context,
            "created_at": start_date.isoformat() + "Z",
            "test_context": test_context,
            "event_id": request_id,
            "chain_ids": ctx_chains,
            "tags": merged_tags,
        }

    async def log_event(
        self,
        event_name: str,
        output: T,
        *,
        start_date: datetime.datetime = datetime.datetime.utcnow(),
        chainId: typing.List[str] = [],
        tags: typing.List[str] = [],
        latency_ms: int = 0,
        error_code: int = 0,
    ):
        if self._stop_worker_flag:
            self.increment_dropped_logs()
            return
        shared = await self.__log_base(chainId, tags, start_date)
        # Add schema to the queue
        self._queue.put(
            {
                **shared,
                "event_name": event_name,
                "event_type": EventType.Log,
                # GlooTaskOutput
                "output": output.dict(),
                # For now we don't compute this.
                "output_type": {
                    "name": output.__class__.__name__,
                    "version": 0,
                    # This is a poor mans version to get some data.
                    # We should use a proper schema here.
                    "fields": output.__class__.schema_json(),
                },
                "latency_ms": latency_ms,
                "error_code": error_code,
            }
        )

    async def log_llm_task_success(
        self,
        task_name: str,
        input: U,
        output: T,
        *,
        details: GlooLLMTaskDetails,
        start_date: datetime.datetime,
        chainId: typing.List[str] = [],
        tags: typing.List[str] = [],
    ):
        if self._stop_worker_flag:
            self.increment_dropped_logs()
            return
        latency_ms = int((datetime.datetime.utcnow() - start_date).total_seconds() * 1000)
        shared = await self.__log_base(chainId, tags, start_date)
        # Add schema to the queue
        self._queue.put(
            {
                **shared,
                "event_name": task_name,
                "event_type": EventType.TaskLLM,
                "input":  input.dict(),
                # For now we don't compute this.
                "input_type": {
                    "name": input.__class__.__name__,
                    "version": 0,
                    # This is a poor mans version to get some data.
                    # We should use a proper schema here.
                    "fields": input.__class__.schema_json(),
                },
                # GlooTaskOutput
                "output": output.dict(),
                # For now we don't compute this.
                "output_type": {
                    "name": output.__class__.__name__,
                    "version": 0,
                    # This is a poor mans version to get some data.
                    # We should use a proper schema here.
                    "fields": output.__class__.schema_json(),
                },
                "latency_ms": latency_ms,
                "error_code": 0,
                "task_llm": details,
            }
        )

    async def log_llm_task_fail(
        self,
        task_name: str,
        input: U,
        *,
        details: GlooLLMTaskDetails,
        start_date: datetime.datetime,
        chainId: typing.List[str] = [],
        tags: typing.List[str] = [],
        error_code: int = 1,
        error_message: str = "Unknown error",
    ):
        if self._stop_worker_flag:
            self.increment_dropped_logs()
            return
        latency_ms = int((datetime.datetime.utcnow() - start_date).total_seconds() * 1000)
        shared = await self.__log_base(chainId, tags, start_date)
        # Add schema to the queue
        self._queue.put(
            {
                **shared,
                "event_name": task_name,
                "event_type": EventType.TaskLLM,
                "input":  input.dict(),
                # For now we don't compute this.
                "input_type": {
                    "name": input.__class__.__name__,
                    "version": 0,
                    # This is a poor mans version to get some data.
                    # We should use a proper schema here.
                    "fields": input.__class__.schema_json(),
                },
                "error_code": error_code,
                "error_metadata": error_message,
                "latency_ms": latency_ms,
                "task_llm": details,
            }
        )


    def increment_failed_attempts(self):
        with self._lock:
            self.failed_log_attempts += 1

    def increment_dropped_logs(self):
        with self._lock:
            self.dropped_logs += 1

    def _worker_thread_fn(self):
        while not self._stop_worker_flag:
            try:
                payload = self._queue.get(timeout=0.1)
                self._emit_log(payload)
            except:
                time.sleep(0.1)
        # Flush the queue
        while not self._queue.empty():
            payload = self._queue.get()
            self._emit_log(payload)
                

    def _emit_log(self, payload):
        # Emits log (override this in a derived class)
        for retry in range(RETRIES):
            try:
                result = requests.post(
                    f"{global_gloo_service()}/log",
                    json=payload,
                    headers={"Authorization": f"Bearer {global_api_key()}"},
                    timeout=TIMEOUT
                )

                if result.status_code == 200:
                    return  # Success
                else:
                    self.increment_failed_attempts()
                    # Don't retry on errors where the service rejected the request
                    return

            except requests.RequestException as error:
                self.increment_failed_attempts()
        self.increment_dropped_logs()

    def print_stats(self):
        if self.failed_log_attempts == 0 and self.dropped_logs == 0:
            return
        print(f"[GLOO] Failed log attempts: {self.failed_log_attempts}")
        print(f"[GlOO] Dropped logs: {self.dropped_logs}")

logger = GlooLogger()

__all__ = ["GlooLogger", "GlooPipelineCtx", "GlooTestCtx"]
