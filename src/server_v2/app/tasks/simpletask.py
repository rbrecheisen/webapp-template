from django import forms

from .basetask import Task


class SimpleTask(Task):

    @staticmethod
    def execute_base(task_model):
        print('>>>> SIMPLE TASK [{}] <<<<<'.format(task_model.name))


class SimpleTaskForm(forms.Form):
    pass
