import django_rq


class Task:

    @django_rq.job
    def execute_base(self, *args, **kwargs):
        self.execute(args, kwargs)

    def execute(self, *args, **kwargs):
        raise NotImplementedError()


class DummyTask(Task):

    def execute(self, *args, **kwargs):
        import time
        for i in range(1000):
            print(i)
            time.sleep(1)
