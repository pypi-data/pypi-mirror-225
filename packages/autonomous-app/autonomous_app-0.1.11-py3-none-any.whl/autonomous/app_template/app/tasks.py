import time
from celery import shared_task
from autonomous import log
from app import create_app

autotask = create_app().extensions["celery"]


@shared_task()
def mocktask():
    time.sleep(1)
    log("MockTask")
    return "success"


@shared_task()
def longmocktask():
    time.sleep(30)
    return "success"


@shared_task()
def parametermocktask(*args, **kwargs):
    log("ParameterMockTask", args, kwargs)

    return args[0] + args[1]


@shared_task()
def errormocktask():
    raise Exception("ErrorMockTask")
