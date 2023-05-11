import os

from celery import Celery


class CeleryClientDummy:
    """Dummy class for celery if it is disabled"""

    def task(self, *args, **kwargs):
        """Dummy task function"""
        return lambda x: CeleryTaskDummy()


class CeleryTaskDummy:
    """Dummy class for celery if it is disabled"""

    def delay(self, *args, **kwargs):
        """Dummy delay function"""
        return CeleryResponseDummy()


class CeleryResponseDummy:
    """Dummy class for celery if it is disabled"""

    id = None


def build_celery():
    """
    Builds a celery client if it is not disabled.
    Otherwise it returns a dummy client.

    :return: A celery client or dummy client
    """
    if os.getenv("DISABLE_CELERY", False):
        return CeleryClientDummy()
    celery = Celery(
        "proj",
        broker=os.getenv("CELERY_BROKER_URL", ""),
        backend=os.getenv("CELERY_RESULT_BACKEND", ""),
    )
    celery.conf.event_serializer = "pickle"
    celery.conf.task_serializer = "pickle"
    celery.conf.result_serializer = "pickle"
    celery.conf.accept_content = [
        "application/json",
        "application/x-python-serialize",
        "pickle",
    ]
    return celery


celery = build_celery()
