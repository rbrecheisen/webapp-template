import django_rq


class Task:

    @django_rq.job
    def execute(self, *args, **kwargs):
        raise NotImplementedError()
