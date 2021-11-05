import os
from django import forms

from ..basetask import Task
from ...models import FilePathModel


class LoadTensorFlowModelsTask(Task):

    def load_and_unpack_model_zip(self, model_zip, target_dir):
        pass

    def execute_base(self, task_model):
        """
        Loads TensorFlow model ZIP files and unpacks them to a target directory specified
        in the task parameters. So, if you specify the models should be unpacked to directory X
        then another task, like PredictBodyCompositionScoresTask, can load the models from directory X
        """
        dataset = task_model.dataset
        files = FilePathModel.objects.filter(dataset=dataset).all()
        for f in files:
            file_name = os.path.split(f.path)[1]
            if file_name == 'model.zip':
                print('>>> loaded model.zip')
            elif file_name == 'contour_model.zip':
                print('>>> loaded contour_model.zip')
            elif file_name == 'params.json':
                print('>>> loaded params.json')
            else:
                task_model.errors.append('{} unknown file'.format(f.path))
                task_model.job_status = 'failed'
                task_model.save()
                break


class LoadTensorFlowModelsTaskForm(forms.Form):
    pass
