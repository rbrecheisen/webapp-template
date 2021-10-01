from .BaseTask import Task


class MyQuickTask(Task):

    @staticmethod
    def execute_base(task_model):
        # TODO: How to couple the task and its form
        print('Bla')
