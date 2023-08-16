from autonomous import log
from tasks import mocktask, longmocktask, parametermocktask, errormocktask
import time
from celery.result import AsyncResult
import pytest


def test_base_task(app):
    results = mocktask.delay()
    time.sleep(2)
    log(results.status)
    assert results.status == "SUCCESS"
    assert results.get() == "success"


def test_param_task(app):
    results = parametermocktask.delay(1, 2, "hello", key="value")
    time.sleep(1)
    log(results.status)
    assert results.status == "SUCCESS"
    assert results.get() == 3


def test_error_task(app):
    results = errormocktask.delay()
    time.sleep(2)
    log(results.status)
    assert results.status == "FAILURE"
    try:
        response = results.get()
    except Exception as e:
        log(e)
    else:
        pytest.fail(f"Exception not raised: {response}")


def test_base_long_task(app):
    task = longmocktask.delay()
    result = AsyncResult(task.id)
    log(result.status)
    result.ready()
    assert result.get() == "success"
