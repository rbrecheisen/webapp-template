class TaskError(Exception):
    pass


class TaskUnknownError(TaskError):
    pass


class MyQuickTask:

    @staticmethod
    def execute(task_model):
        print('Executing a quick task...')
        print('Bla')
        task_model.job_status = 'finished'
        task_model.save()


class MyLongRunningTask:

    @staticmethod
    def execute(task_model):
        print('Executing a long-running task...')
        for i in range(1000):
            print(i)
        task_model.job_status = 'finished'
        task_model.save()


class PredictBodyCompositionScoresTask:

    @staticmethod
    def execute(task_model):
        task_model.job_status = 'finished'
        task_model.save()


class ValidateBodyCompositionScoresTask:

    @staticmethod
    def execute(task_model):
        task_model.job_status = 'finished'
        task_model.save()


TASK_REGISTRY = {
    'MyQuickTask': MyQuickTask(),
    'MyLongRunningTask': MyLongRunningTask(),
    'PredictBodyCompositionScoresTask': PredictBodyCompositionScoresTask(),
    'ValidateBodyCompositionScoresTask': ValidateBodyCompositionScoresTask(),
}
