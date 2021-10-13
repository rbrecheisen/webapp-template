from .BaseTask import Task


class MyQuickTask(Task):

    @staticmethod
    def execute_base(task_model):
        task_model.info_message = 'Successfully executed quick task'
