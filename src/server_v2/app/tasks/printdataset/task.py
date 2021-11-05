from django import forms

from ..basetask import Task
from ...models import FilePathModel


class PrintDataSetTask(Task):

    def execute_base(self, task_model):
        print(task_model.parameters)
        files = FilePathModel.objects.filter(dataset=task_model.dataset).all()
        for f in files:
            print(f.path)


class PrintDataSetTaskForm(forms.Form):
    pass
