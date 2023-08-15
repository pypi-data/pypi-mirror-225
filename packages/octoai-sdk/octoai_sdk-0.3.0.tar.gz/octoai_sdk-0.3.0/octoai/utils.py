"""Various utilities."""

import logging
import random
import time
from typing import Callable

import httpx

from octoai.errors import OctoAIClientError

LOG = logging.getLogger(__name__)


def retry(
    fn: Callable[[], httpx.Response],
    retry_count: int = 5,
    interval: float = 1.0,
    exp_backoff: float = 2.0,
    jitter: float = 1.0,
    maximum_backoff: float = 30.0,
) -> httpx.Response:
    """Retry an HTTP request with exponential backoff and jitter.

    :param fn: function to call
    :type fn: Callable[[], httpx.Response]
    :param retry_count: number of times to retry, defaults to 5
    :type retry_count: int, optional
    :param interval: duration to wait before retry, defaults to 1.0
    :type interval: float, optional
    :param exp_backoff: exponent to increase interval each try, defaults to 2.0
    :type exp_backoff: float, optional
    :param jitter: , defaults to 1.0
    :type jitter: float, optional
    :param maximum_backoff: max duration to wait, defaults to 30.0
    :type maximum_backoff: float, optional
    :raises OctoAIClientError: occurs when a client error is thrown.
    :return: response from api server
    :rtype: httpx.Response
    """
    try:
        resp = fn()
        if retry_count - 1 == 0:
            return resp
        # Raise HTTPStatusError for 4xx or 5xx.
        resp.raise_for_status()
    except httpx.HTTPStatusError:
        if resp.status_code >= 500 or resp.status_code == 429:
            time.sleep(interval + random.uniform(0, jitter))
            return retry(
                fn,
                retry_count - 1,
                interval * exp_backoff,
                exp_backoff,
                jitter,
                maximum_backoff,
            )

        # Raise error on all other client errors.
        elif 400 <= resp.status_code < 499 and resp.status_code != 429:
            # Raise error. Do not retry.
            raise OctoAIClientError(f"Client error: {resp.status_code}\n{resp.text}")

    # Raise error without retry on all other exceptions.
    return resp


def health_check(
    fn: Callable[[], httpx.Response],
    timeout: float = 900.0,
    interval: float = 1.0,
    iteration_count: int = 0,
) -> httpx.Response:
    """Check the health of an endpoint.

    :param fn: Get request for endpoint health check.
    :type fn: Callable[[], httpx.Response]
    :param timeout: seconds before health_check times out, defaults to 900.0
    :type timeout: int, optional
    :param interval: seconds to wait before checking endpoint health again,
        defaults to 1.0
    :type interval: int, optional
    :param iteration_count: count total attempts for cold start warning,
        defaults to 0
    :type iteration_count: int
    :raises OctoAIClientError: Client-side failure such as missing api token
    :return: Response once timeout has passed
    :rtype: httpx.Response
    """
    start = time.time()
    try:
        resp = fn()
        if timeout <= 0:
            return resp
        # Raise HTTPStatusError for 4xx or 5xx.
        resp.raise_for_status()
    except httpx.HTTPStatusError:
        if iteration_count == 0:
            LOG.warning(
                "Your endpoint may take several minutes to start and be ready to serve "
                "inferences. You can increase your endpoint's min replicas to mitigate "
                "cold starts."
            )
        if resp.status_code >= 500 or resp.status_code == 429:
            stop = time.time()
            current = stop - start
            time.sleep(interval)
            return health_check(
                fn, timeout - current - interval, interval, iteration_count + 1
            )

        # Raise error on all other client errors.
        elif 400 <= resp.status_code < 499 and resp.status_code != 429:
            # Raise error. Do not retry.
            raise OctoAIClientError(f"Client error: {resp.status_code}\n{resp.text}")

    # Raise error without retry on all other exceptions.
    return resp
