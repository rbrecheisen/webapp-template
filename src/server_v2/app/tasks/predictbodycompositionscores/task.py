import os

from django import forms

from ..basetask import Task, TaskExecutionError
from ...models import FilePathModel, DataSetModel
from barbell2light.dicom import is_dicom_file


class PredictBodyCompositionScoresTask(Task):

    @staticmethod
    def load_model(zip_file_path):
        return ''

    @staticmethod
    def load_params(file_path):
        return ''

    def load_tensorflow_models(self, dataset):
        files = FilePathModel.objects.filter(dataset=dataset).all()
        model, contour_model, params = None, None, None
        for f in files:
            file_name = os.path.split(f.path)[1]
            if file_name == 'model.zip':
                model = self.load_model(f.path)
            elif file_name == 'contour_model.zip':
                contour_model = self.load_model(f.path)
            elif file_name == 'params.json':
                params = self.load_params(f.path)
            else:
                raise TaskExecutionError('Not a TensorFlow model file {}'.format(f.path))
        return model, contour_model, params

    def execute_base(self, task_model):
        """
        This task needs to do several things:
            (1) Load one or more TensorFlow models from dataset 1
            (2) Apply those models to L3 files from dataset 2
            (3) It outputs another dataset with DICOM files, NumPy arrays and CSV scores
        Basically this task has its own dataset, namely the set from which the task was created and started.
        It also requires the ID of the dataset containing the TensorFlow models. This ID can be passed to
        the task as a parameter. Note that this requires the display of dataset IDs in the HTML interface.
        """
        errors = []
        tensorflow_models_dataset = DataSetModel.objects.get(pk=task_model.parameters['tensorflow_models_dataset_id'])
        try:
            model, contour_model, params = self.load_tensorflow_models(tensorflow_models_dataset)
        except TaskExecutionError as e:
            errors.append('Error loading TensorFlow models')
            task_model.errors = errors
            task_model.job_status = 'failed'
            task_model.save()
            return
        dataset = task_model.dataset
        files = FilePathModel.objects.filter(dataset=dataset).all()
        for f in files:
            # Check file is DICOM file
            pass


class PredictBodyCompositionScoresTaskForm(forms.Form):
    pass
