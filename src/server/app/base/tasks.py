import time

import django_rq


class TaskError(Exception):
    pass


class TaskUnknownError(TaskError):
    pass


class MyLongRunningTask:

    def __init__(self):
        self.name = 'MyLongRunningTask'

    @django_rq.job
    def execute(self, *args, **kwargs):
        print('Executing a long-running task...')
        for i in range(1000):
            print(i)


class MyQuickTask:

    def __init__(self):
        self.name = 'MyQuickTask'

    @django_rq.job
    def execute(self, *args, **kwargs):
        print('Executing a quick task...')
