import os

from django.conf import settings

from .BaseTask import Task
from ..models import DataSetModel, FilePathModel


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
