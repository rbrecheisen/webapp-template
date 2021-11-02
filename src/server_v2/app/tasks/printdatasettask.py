from django import forms

from .basetask import Task
from ..models import FilePathModel


class PrintDataSetTask(Task):

    @staticmethod
    def execute_base(task_model):
        print(task_model.parameters)
        files = FilePathModel.objects.filter(dataset=task_model.dataset).all()
        for f in files:
            print(f.path)


class PrintDataSetTaskForm(forms.Form):
    pass
