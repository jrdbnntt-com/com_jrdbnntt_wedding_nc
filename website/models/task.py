import logging
from datetime import datetime
from json import JSONEncoder, JSONDecoder
from django.utils import timezone
from django.contrib import admin
from django.db import models

logger = logging.getLogger(__name__)
json_encoder = JSONEncoder()
json_decoder = JSONDecoder()


def init():
    """ Does nothing, just here to keep import """
    pass


class Task(models.Model):
    name = models.CharField(max_length=100)
    kwargs = models.CharField(max_length=1000)
    target_unix_time = models.BigIntegerField()
    locked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "Task(target_unix_time='%d',name='%s',kwargs='%s')" % (
            self.target_unix_time,
            self.name,
            self.kwargs,
        )

    def lock(self):
        self.locked = True
        self.save()

    def finish_with_failure(self, e: Exception):
        logger.error("Task %s finished with failure: %s" % (self, e), exc_info=True)
        self.delete()

    def finish_with_success(self):
        logger.debug("Task %s finished successfully" % self)
        self.delete()

    @staticmethod
    def marshall_kwargs(kwargs: dict) -> str:
        return json_encoder.encode(task_kwargs)

    @staticmethod
    def unmarshall_kwargs(marshalled_kwargs: str) -> dict:
        return json_decoder.decode(marshalled_kwargs)

    def execute_task(self, task_executor):
        try:
            task_executor(**self.unmarshall_kwargs(self.kwargs))
            self.finish_with_success()
        except Exception as e:
            self.finish_with_failure(e)


def schedule_task(name: str, target_time: datetime, task_kwargs: dict, create_only_if_does_not_exit=True) -> Task:
    kwargs_str = Task.marshall_kwargs(task_kwargs)
    if create_only_if_does_not_exit:
        task = Task.objects.filter(name=name, kwargs=kwargs_str).all()
        if len(task) > 0:
            return task[0]

    task = Task.objects.create(
        name=name,
        task_kwargs=kwargs_str,
        target_unix_time=int(target_time.timestamp())
    )
    logger.info("Scheduled task '%s' to occur at %s (%0.3f seconds from now)" % (
        task.name,
        datetime.fromtimestamp(task.target_unix_time).isoformat(),
        (datetime.now().timestamp() - task.target_unix_time) / 1000.0
    ))
    return task


def get_processable_tasks(lock=True):
    now = int(datetime.now().timestamp())
    tasks = Task.objects.filter(locked=False, target_unix_time__lt=now).all()
    if lock:
        for task in tasks:
            task.lock()
    return tasks


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
