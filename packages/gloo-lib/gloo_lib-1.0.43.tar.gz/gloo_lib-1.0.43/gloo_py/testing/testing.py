from enum import StrEnum
import inspect
import typing
import httpx
from pydantic import BaseModel
import pytest
import asyncio

from ..env import global_project_id, global_api_key, global_gloo_service
from ..logging.base_logger import GlooLogger, GlooTestCtx

###

U = typing.TypeVar("U", bound=BaseModel)


class GlooTestCaseBase(typing.TypedDict):
    name: str


T = typing.TypeVar("T", bound=GlooTestCaseBase)


def post(
    url: str,
    data: typing.Dict[str, typing.Any],
    model: typing.Optional[typing.Type[U]] = None,
):
    try:
        data.update({"project_id": global_project_id()})
        with httpx.Client() as client:
            result = client.post(
                f"{global_gloo_service()}/{url}",
                json=data,
                headers={"Authorization": f"Bearer {global_api_key()}"},
            )
            if result.status_code == 200:
                if model:
                    return model.parse_obj(result.json())
                return result.json()
            raise Exception(f"Error: /{url} {result.status_code} {result.text}")
    except Exception as e:
        raise e


class CreateCycleResponse(BaseModel):
    test_cycle_id: str
    dashboard_url: str


def create_cycle_id(context: None) -> str:
    response = post("tests/create-cycle", {"context": context}, CreateCycleResponse)
    if not response:
        raise Exception(
            "Failed to register test with Gloo Services. Did you forget to run init_gloo with a project_id anywhere in the call path?"
        )
    print(f"See tests at: {response.dashboard_url}")
    return response.test_cycle_id


class TestCaseStatus(StrEnum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    PASSED = "PASSED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    EXPECTED_FAILURE = "EXPECTED_FAILURE"


def create_test_case(dataset_name: str, case_name: str, case_args_name: typing.List[T]):
    post(
        "tests/create-case",
        {
            "test_cycle_id": global_gloo_cycle_id(),
            "test_dataset_name": dataset_name,
            "test_name": case_name,
            "test_case_args": case_args_name,
        },
    )


def update_test_case(
    dataset_name: str,
    case_name: str,
    case_args_name: str,
    status: TestCaseStatus,
    result_data: typing.Any,
    error_data: typing.Any,
):
    post(
        "tests/update",
        {
            "test_cycle_id": global_gloo_cycle_id(),
            "test_dataset_name": dataset_name,
            "test_case_definition_name": case_name,
            "test_case_arg_name": case_args_name,
            "status": status,
            "result_data": result_data,
            "error_data": error_data,
        },
    )


###


class GlooTestDataset(typing.Generic[T]):
    def __init__(self, name, test_cases: typing.List[T]):
        self.name = name
        self.test_cases = test_cases


GLOO_CYCLE_ID = None


def global_gloo_cycle_id() -> str:
    global GLOO_CYCLE_ID
    if GLOO_CYCLE_ID is None:
        GLOO_CYCLE_ID = create_cycle_id(None)
    return GLOO_CYCLE_ID


@pytest.fixture(scope="session", autouse=True)
def gloo_connection():
    with GlooLogger() as logger:
        yield


class DefaultResponse(BaseModel):
    data: typing.Any


class TestCaseInitialized(BaseModel):
    language: str = "python"
    code: str
    data: typing.Any


# Define a decorator that will take a user test function and run it against each test case in a suite
def with_suite(
    suite: GlooTestDataset[T] | typing.List[GlooTestDataset[T]],
    *,
    arg_name: str = "test_case",
) -> typing.Callable:
    suites = suite if isinstance(suite, list) else [suite]
    test_cases = [
        pytest.param((s.name, tc), id=f'{s.name}::{tc["name"]}')
        for s in suites
        for tc in s.test_cases
    ]

    def decorator(
        test_func: typing.Callable[
            [
                T,
                typing.Callable[[typing.Any], typing.Awaitable[None]],
            ],
            typing.Coroutine[typing.Any, typing.Any, None],
        ]
    ) -> typing.Callable:
        for s in suites:
            create_test_case(s.name, test_func.__name__, s.test_cases)

        def wrapped_test_func(test_case: typing.Tuple[str, T]) -> None:
            with GlooTestCtx(
                {
                    "test_case_arg_name": test_case[1]["name"],
                    "test_dataset_name": test_case[0],
                    "test_case_name": test_func.__name__,
                    "test_cycle_id": global_gloo_cycle_id(),
                }
            ), GlooLogger() as logger:
                # Get the source code of the test function so we can pass it to the logger
                source_code = inspect.getsource(test_func)

                # Call update_test_case before running the test
                update_test_case(
                    test_case[0],
                    test_func.__name__,
                    test_case[1]["name"],
                    TestCaseStatus.RUNNING,
                    None,
                    None,
                )
                asyncio.run(
                    logger.log_event(
                        "TestCase",
                        output=TestCaseInitialized(code=source_code, data=test_case[1]),
                    )
                )
                error_message = None
                try:

                    async def log_value(value) -> None:
                        if not isinstance(value, BaseModel):
                            value = DefaultResponse(data=value)

                        await logger.log_event("TestEvent", output=value)

                    asyncio.run(test_func(test_case[1], log_value))
                except Exception as e:
                    error_message = {"message": str(e)}
                    asyncio.run(
                        logger.log_event(
                            "TestFailure",
                            output=DefaultResponse(data=str(e)),
                            error_code=1,
                        )
                    )
                    raise  # Re-raise the exception so pytest can handle it
                finally:
                    # Call update_test_case after running the test (success)
                    update_test_case(
                        test_case[0],
                        test_func.__name__,
                        test_case[1]["name"],
                        TestCaseStatus.PASSED
                        if error_message is None
                        else TestCaseStatus.FAILED,
                        None,
                        error_message,
                    )

        wrapped_test_func.__name__ = test_func.__name__
        return pytest.mark.parametrize(arg_name, test_cases)(wrapped_test_func)

    return decorator
