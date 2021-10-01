import os

from django import forms
from django.conf import settings

from .models import DataSetModel, FilePathModel


class TaskError(Exception):
    pass


class TaskUnknownError(TaskError):
    pass


class TaskExecutionError(TaskError):
    pass


class Task:

    def execute(self, task_model):
        print('Executing task {}...'.format(task_model.name))
        task_model.job_status = 'running'
        task_model.save()
        try:
            self.execute_base(task_model)
            task_model.job_status = 'finished'
            task_model.save()
        except TaskExecutionError as e:
            task_model.job_status = 'failed'
            task_model.error_message = str(e)
            task_model.save()

    @staticmethod
    def execute_base(task_model):
        raise NotImplementedError()


class TaskForm(forms.Form):
    pass


class MyQuickTask(Task):

    @staticmethod
    def execute_base(task_model):
        # TODO: How to couple the task and its form
        print('Bla')


class MyQuickTaskForm(TaskForm):
    text = forms.CharField(label='Text', max_length=16)


class MyLongRunningTask(Task):

    @staticmethod
    def execute_base(task_model):
        ds_name = '{}-{}'.format(task_model.dataset.name, task_model.name)
        ds = DataSetModel.objects.create(name=ds_name, owner=task_model.dataset.owner)
        for i in range(1000):
            file_path = os.path.join(settings.MEDIA_ROOT, '{:04d}.txt'.format(i))
            with open(file_path, 'w') as f:
                f.write('some text\n')
            FilePathModel.objects.create(file_path=file_path, dataset=ds)
        task_model.info_message = 'Successfully executed long-running task'


class PredictBodyCompositionScoresTask(Task):

    @staticmethod
    def execute_base(task_model):
        raise TaskExecutionError('Not implemented yet')


class ValidateBodyCompositionScoresTask(Task):

    @staticmethod
    def execute_base(task_model):
        raise TaskExecutionError('Not implemented yet')


TASK_REGISTRY = {
    'MyQuickTask': MyQuickTask(),
    'MyLongRunningTask': MyLongRunningTask(),
    'PredictBodyCompositionScoresTask': PredictBodyCompositionScoresTask(),
    'ValidateBodyCompositionScoresTask': ValidateBodyCompositionScoresTask(),
}
