from django import forms

from ..basetask import Task
from ...models import FilePathModel


class PredictBodyCompositionScoresTask(Task):

    def execute_base(self, task_model):
        pass


class PredictBodyCompositionScoresTaskForm(forms.Form):
    pass
