# -*- coding: utf-8 -*-
"""
MIT License
Copyright (c) 2023 OVINC-CN

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import re
import time
import uuid
from functools import wraps
from typing import Tuple

from redis.client import Redis
from redis.exceptions import RedisError

from client_throttler.constants import (
    DEFAULT_BUFFER_TIME,
    DEFAULT_MAX_RETRY_TIMES,
    TimeDurationUnit,
)
from client_throttler.exceptions import RateParseError, TooManyRequests, TooManyRetries


class Throttler:
    """
    Distributed rate limiting based on Redis Used to actively limit a specific call,
    calculate the waiting time for excessive requests, and continue the request after delaying through sleep.

    Period should be one of: ('ms', 'msec', 's', 'sec', 'm', 'min', 'h', 'hour', 'd', 'day')

    Previous request information used for throttling is stored in the cache.
    """

    unit_mapping = {
        "ms": TimeDurationUnit.MILLISECOND,
        "s": TimeDurationUnit.SECOND,
        "m": TimeDurationUnit.MINUTE,
        "h": TimeDurationUnit.HOUR,
        "d": TimeDurationUnit.DAY,
    }

    def __init__(
        self,
        func: callable,
        *,
        rate: str,
        redis_client: Redis,
        scope: str = "",
        enable_sleep_wait: bool = True,
        buffer_time: float = DEFAULT_BUFFER_TIME,
        max_retry_times: int = DEFAULT_MAX_RETRY_TIMES,
    ):
        """
        :param func: The rate-limited method
        :param rate: The rate limit string, eg: 1/s, 100/min, 20/5s
        :param redis_client: Redis Client
        :param scope: Decoration
        :param enable_sleep_wait: Whether to sleep and wait for retry after being rate-limited
        :param buffer_time: Buffer time for the request from being sent to arriving (seconds)
        :param max_retry_times: Maximum number of retries
        """

        self.func = func
        self.cache_key = f"Throttler:{scope}:{func.__name__}"
        self.num_requests, self.interval = self.parse_rate(rate)
        self.enable_sleep_wait = enable_sleep_wait
        self.buffer_time = buffer_time
        self.redis_client = redis_client
        self.max_retry_times = max_retry_times

    @classmethod
    def parse_rate(cls, rate: str) -> Tuple[int, float]:
        """
        Given the request rate string, return a two tuple of:
        <allowed number of requests>, <period of time in seconds>
        """

        rate_pattern = re.compile(r"^(\d+)/(\d+)?(ms|s|m|h|d)$")
        match = rate_pattern.match(rate)

        if not match:
            raise RateParseError(rate)

        num_requests = int(match.group(1))
        value = float(match.group(2) or 1)
        unit = cls.unit_mapping[match.group(3)]
        return num_requests, value * unit

    def get_request_count(self, start_time: float, tag: str, now: float) -> int:
        """
        Get the number of requests within the time interval
        :param start_time: Start time
        :param tag: Request tag
        :param now: Current time
        """

        """
        1. Delete data outside the interval
        2. Insert the current record (maximum value is used to prevent the record from being deleted)
        3. Get the number of requests within the current interval to determine if the frequency is exceeded
        4. Set the expiration time for the large key to prevent cold data from occupying space
        """
        with self.redis_client.pipeline(transaction=False) as pipe:
            pipe.zremrangebyscore(
                self.cache_key,
                0,
                start_time - TimeDurationUnit.MILLISECOND,
            )
            pipe.zadd(self.cache_key, {tag: now + TimeDurationUnit.YEAR})
            pipe.zcard(self.cache_key)
            pipe.expire(self.cache_key, int(2 * self.interval))
            _, _, count, _ = pipe.execute(False)
        return count

    def get_wait_time(self, start_time: float, now: float, tag: str) -> float:
        """
        Get the wait time
        :param start_time: Start time
        :param now: Current time
        :param tag: Request tag
        :return: Wait time (seconds)
        """

        # If rate-limited, remove the inserted record and calculate the next request time
        # based on the time of the first request in the current interval.
        with self.redis_client.pipeline(transaction=False) as pipe:
            pipe.zrem(self.cache_key, tag)
            pipe.zrangebyscore(
                self.cache_key, start_time, now, start=0, num=1, withscores=True
            )
            _, result = pipe.execute()
        if not result:
            return self.interval / 2
        _, last_time = result[0]
        return (last_time + self.interval - now) or self.interval / 2

    def update_time(self, tag: str):
        """
        Update this request's time
        :param tag: Request tag
        """

        # If there is not be limited, update the record to the current timestamp plus buffer time
        # (buffer time is used to simulate the interval between unlocking and the request)
        self.redis_client.zadd(self.cache_key, {tag: time.time() + self.buffer_time})

    def try_limit(self, tag: str) -> float:
        """
        Try to limit
        :param tag: Request tag
        :return: Wait time (seconds)
        """

        now = time.time()
        start_time = now - self.interval
        count = self.get_request_count(start_time, tag, now)
        if count > self.num_requests:
            return self.get_wait_time(start_time, now, tag)
        else:
            self.update_time(tag)
            return 0

    def wait(self, tag: str):
        """
        Wait
        :param tag: Request tag
        :return: Wait time (seconds)
        """

        retry_times = 0
        while True:
            retry_times += 1
            if retry_times > self.max_retry_times:
                raise TooManyRetries(tag, retry_times)
            wait_time = self.try_limit(tag)
            if not wait_time:
                return
            if self.enable_sleep_wait:
                time.sleep(wait_time)
                continue
            raise TooManyRequests()

    def _reset(self):
        """
        For Test
        Clean up the keys stored in Redis.
        """

        self.redis_client.delete(self.cache_key)

    def __call__(self, *args, **kwargs):
        tag = str(uuid.uuid1())
        try:
            self.wait(tag)
            return self.func(*args, **kwargs)
        except RedisError as err:
            # Ensure the key is deleted if an error occurs during execution
            self.redis_client.zrem(self.cache_key, tag)
            raise err


def throttler(
    rate: str,
    redis_client: Redis,
    scope: str = "",
    enable_sleep_wait: bool = True,
    buffer_time: float = DEFAULT_BUFFER_TIME,
    max_retry_times: int = DEFAULT_MAX_RETRY_TIMES,
):
    """
    :param interval: Time period (seconds)
    :param rate: The rate limit string, eg: 1/s, 100/min, 20/5s
    :param redis_client: Redis Client
    :param scope: Decoration
    :param enable_sleep_wait: Whether to sleep and wait for retry after being rate-limited
    :param buffer_time: Buffer time for the request from being sent to arriving (seconds)
    :param max_retry_times: Maximum number of retries
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return Throttler(
                func,
                rate=rate,
                scope=scope,
                redis_client=redis_client,
                enable_sleep_wait=enable_sleep_wait,
                buffer_time=buffer_time,
                max_retry_times=max_retry_times,
            )(*args, **kwargs)

        return wrapper

    return decorator
