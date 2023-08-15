from datetime import datetime, timedelta
from time import perf_counter, sleep

import pytest

import celery
from celery import group

from .conftest import get_active_redis_channels
from .tasks import (ClassBasedAutoRetryTask, ExpectedException, add,
                    add_ignore_result, add_not_typed, fail, print_unicode,
                    retry, retry_once, retry_once_priority, sleeping)

TIMEOUT = 10


_flaky = pytest.mark.flaky(reruns=5, reruns_delay=2)
_timeout = pytest.mark.timeout(timeout=300)


def flaky(fn):
    return _timeout(_flaky(fn))


def _producer(j):
    """Single producer helper function"""
    results = []
    for i in range(20):
        results.append([i + j, add.delay(i, j)])
    for expected, result in results:
        value = result.get(timeout=10)
        assert value == expected
        assert result.status == 'SUCCESS'
        assert result.ready() is True
        assert result.successful() is True
    return j


class test_tasks:
    @flaky
    def test_basic_task(self, manager):
        """Tests basic task call"""
        results = []
        # Tests calling task only with args
        for i in range(2):
            results.append([i + i, add.delay(i, i)])
        for expected, result in results:
            value = result.get(timeout=10)
            assert value == expected
            assert result.status == 'SUCCESS'
            assert result.ready() is True
            assert result.successful() is True

        results = []
        # Tests calling task with args and kwargs
        for i in range(2):
            results.append([3*i, add.delay(i, i, z=i)])
        for expected, result in results:
            value = result.get(timeout=10)
            assert value == expected
            assert result.status == 'SUCCESS'
            assert result.ready() is True
            assert result.successful() is True


class test_task_redis_result_backend:
    @pytest.fixture(autouse=True)
    def setup(self, redis_server, manager):
        redis_server.restart()
        import time
        time.sleep(1)
        if not manager.app.conf.result_backend.startswith('redis'):
            raise pytest.skip('Requires redis result backend.')

    def test_ignoring_result_no_subscriptions(self):
        assert get_active_redis_channels() == []
        result = add_ignore_result.delay(1, 2)
        assert result.ignored is True
        assert get_active_redis_channels() == []

