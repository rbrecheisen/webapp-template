from django import forms

from ..basetask import Task
from ...models import FilePathModel


class PredictBodyCompositionScoresTask(Task):

    def execute_base(self, task_model):
        """
        This task needs to do several things:
        (1) Load one or more TensorFlow models from file (dataset 1)
        (2) Apply those models to L3 files (dataset 2)
        (3) It outputs another dataset with DICOM files, NumPy arrays and CSV scores
        Basically this task has its own dataset, namely the set from which the task was created and started.
        It also requires the ID of the dataset containing the TensorFlow models. This ID can be passed to
        the task as a parameter. Note that this requires the display of dataset IDs in the HTML interface.
        """
        dataset = task_model.dataset
        files = FilePathModel.objects.filter(dataset=dataset).all()
        for f in files:
            pass


class PredictBodyCompositionScoresTaskForm(forms.Form):
    pass
