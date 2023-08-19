# Example callback function
import pytest
import time
import logging
import requests
from senstile_utils.retry import retry_call
from senstile_utils.retry.retry_exception import RetryException

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Helper Functions


def always_fails(*args, **kwargs):
    raise Exception("This function always fails")


def always_succeeds():
    return "Success"


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

# TEST


def test_retry_success():
    # Test if a function that doesn't raise exceptions works as expected
    result = retry_call(always_succeeds)
    assert result == "Success"


def test_retry_fail():
    # Test if a function that always fails does raise an exception after retries
    with pytest.raises(RetryException, match="This function always fails"):
        retry_call(always_fails, max_trials=3, delay_ms=50)


def test_retry_with_args():
    # Test if a function that takes arguments is called with those arguments
    def echo_args(a, b, c):
        return a, b, c

    result = retry_call(echo_args, arguments=(1, 2, 3))
    assert result == (1, 2, 3)


def test_retry_with_kwargs():
    # Test if a function that takes keyword arguments is called with those arguments
    def echo_kwargs(a=0, b=0, c=0):
        return a, b, c

    result = retry_call(echo_kwargs, arguments={"a": 1, "b": 2, "c": 3})
    assert result == (1, 2, 3)


def test_retry_eventually_succeeds():
    # Reset the counter for the helper function
    sometimes_succeeds.counter = 0

    # This function will fail once and then succeed
    result = retry_call(sometimes_succeeds, max_trials=3, delay_ms=50)
    assert result == "Success"


def test_retry_with_mixed_args_and_kwargs():
    result = retry_call(echo_mixed_args, arguments=([1, 2], {"a": 3, "b": 4}))
    assert result == (([1, 2], {"a": 3, "b": 4}), {})


def test_retry_with_custom_delay():
    start_time = time.time()
    with pytest.raises(RetryException, match="This function always fails"):
        retry_call(always_fails, max_trials=2, delay_ms=500)
    elapsed_time = time.time() - start_time

    assert elapsed_time >= 1  # At least 2 seconds should have passed


def test_retry_with_invalid_args():
    def echo_no_args():
        return "NoArgs"

    result = retry_call(echo_no_args, arguments="InvalidArgsType")
    assert result == "NoArgs"


def test_retry_network_failure():
    # Test if a function that attempts to make a network call to a non-existing URI fails as expected
    with pytest.raises(RetryException):
        retry_call(failed_network_call, max_trials=3, delay_ms=50)


def test_retry_file_failure():
    # Test if a function that attempts to open a non-existing file fails as expected
    with pytest.raises(RetryException, match="^Maximum retry attempts reached. Attempts made: 3/3.") as exc_info:
        retry_call(open_nonexistent_file, max_trials=3, delay_ms=50)
    
    # Check if the raised exception is specifically due to a FileNotFoundError
    assert isinstance(exc_info.value.__cause__, FileNotFoundError)
    assert "No such file or directory" in str(exc_info.value.__cause__)
