from .BaseTask import Task, TaskExecutionError


class PredictBodyCompositionScoresTask(Task):

    @staticmethod
    def execute_base(task_model):
        raise TaskExecutionError('Not implemented yet')
