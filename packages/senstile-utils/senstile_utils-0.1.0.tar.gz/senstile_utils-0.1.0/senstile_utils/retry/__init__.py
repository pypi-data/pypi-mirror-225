import asyncio
import inspect
import logging
import time
from typing import Any, Callable, Dict, Tuple, Union

from senstile_utils.retry.retry_exception import RetryException

log = logging.getLogger(__name__)


def retry_call(callback: Callable, arguments: Union[Tuple[Any], Dict[str, Any]] = None, max_trials=3, delay_ms=1000):
    def task():
        trials = 0
        last_exception = None
        while trials < max_trials:
            try:
                if isinstance(arguments, tuple):
                    return callback(*arguments)
                elif isinstance(arguments, dict):
                    return callback(**arguments)
                else:
                    return callback()
            except Exception as e:
                trials += 1
                last_exception = e
                log.info(f"Retrying call {callback}, attempt: {trials}")
                time.sleep(delay_ms / 1000)
        raise RetryException(trials, max_trials,
                             last_exception) from last_exception
    return task()


async def retry_call_async(callback: Callable, arguments: Union[Tuple[Any], Dict[str, Any]] = None, max_trials=3, delay_ms=1000):
    trials = 0
    last_exception = None

    while trials < max_trials:
        try:
            # Check if the callback is asynchronous
            if inspect.iscoroutinefunction(callback):
                if isinstance(arguments, tuple):
                    return await callback(*arguments)
                elif isinstance(arguments, dict):
                    return await callback(**arguments)
                else:
                    return await callback()
            else:
                if isinstance(arguments, tuple):
                    return callback(*arguments)
                elif isinstance(arguments, dict):
                    return callback(**arguments)
                else:
                    return callback()

        except Exception as e:
            trials += 1
            last_exception = e
            log.info(f"Retrying call {callback}, attempt: {trials}")
            await asyncio.sleep(delay_ms / 1000)

    raise RetryException(trials, max_trials,
                         last_exception) from last_exception
