# Example callback function
import asyncio
import pytest
import time
import logging
import requests
from senstile_utils.retry import retry_call_async
from senstile_utils.retry.retry_exception import RetryException

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Helper Functions


async def async_always_succeeds():
    await asyncio.sleep(0.1)  # simulate some async IO work
    return "Success"


async def async_always_fails():
    await asyncio.sleep(0.1)  # simulate some async IO work
    raise Exception("This async function always fails")


def sometimes_succeeds(trials=2):
    if sometimes_succeeds.counter < trials:
        sometimes_succeeds.counter += 1
        raise Exception("Failed")
    return "Success"


sometimes_succeeds.counter = 0


def echo_mixed_args(*args, **kwargs):
    return args, kwargs


def failed_network_call():
    response = requests.get("https://nonexistentwebsite12345.com")
    # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    response.raise_for_status()
    return response.text


def open_nonexistent_file():
    with open("nonexistentfile12345.txt", "r") as f:
        return f.read()

#################### TEST ############################


@pytest.mark.asyncio
async def test_async_retry_success():
    # Test if an async function that doesn't raise exceptions works as expected
    result = await retry_call_async(async_always_succeeds)
    assert result == "Success"


@pytest.mark.asyncio
async def test_async_retry_fail():
    # Test if an async function that always fails does raise an exception after retries
    with pytest.raises(RetryException, match="^Maximum retry attempts reached. Attempts made: 3/3.") as exc_info:
        await retry_call_async(async_always_fails, max_trials=3, delay_ms=50)
    assert "This async function always fails" in str(exc_info.value.__cause__)


@pytest.mark.asyncio
async def test_retry_eventually_succeeds_2_attempts():
    sometimes_succeeds.counter = 0
    result = await retry_call_async(sometimes_succeeds, max_trials=3, delay_ms=50)
    assert result == "Success"
    assert sometimes_succeeds.counter == 2


@pytest.mark.asyncio
async def test_retry_eventually_succeeds_1_attempts():
    sometimes_succeeds.counter = 0
    result = await retry_call_async(sometimes_succeeds, arguments={"trials": 1}, max_trials=3, delay_ms=50)
    assert result == "Success"
    assert sometimes_succeeds.counter == 1


@pytest.mark.asyncio
async def test_retry_eventually_fails_after_max_attempts_has_reached():
    sometimes_succeeds.counter = 0
    with pytest.raises(RetryException, match="Failed"):
        await retry_call_async(sometimes_succeeds,arguments={"trials": 5}, max_trials=3, delay_ms=50)
    assert sometimes_succeeds.counter == 3


@pytest.mark.asyncio
async def test_retry_with_mixed_args_and_kwargs():
    result = await retry_call_async(
        echo_mixed_args, arguments=([1, 2], {"a": 3, "b": 4}))
    assert result == (([1, 2], {"a": 3, "b": 4}), {})


@pytest.mark.asyncio
async def test_retry_with_custom_delay():
    start_time = time.time()
    with pytest.raises(RetryException, match="This async function always fails"):
        await retry_call_async(async_always_fails, max_trials=2, delay_ms=500)
    elapsed_time = time.time() - start_time

    assert elapsed_time >= 1.0
