from django import forms

from .BaseTask import Task, TaskForm


class MyQuickTask(Task):

    @staticmethod
    def execute_base(task_model):
        task_model.info_message = 'Successfully executed quick task'


class MyQuickTaskForm(TaskForm):
    name = forms.CharField(label='name', max_length=128)
