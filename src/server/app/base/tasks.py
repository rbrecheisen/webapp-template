import time

import django_rq


class TaskError(Exception):
    pass


class TaskUnknownError(TaskError):
    pass


class Task:

    @django_rq.job
    def execute_base(self, *args, **kwargs):
        self.execute(args, kwargs)

    def execute(self, *args, **kwargs):
        raise NotImplementedError()


class MyLongRunningTask(Task):

    def execute(self, *args, **kwargs):
        import time
        for i in range(1000):
            print(i)
            time.sleep(1)


class MyQuickTask(Task):

    def execute(self, *args, **kwargs):
        print('Executing a quick task...')
        time.sleep(1)
