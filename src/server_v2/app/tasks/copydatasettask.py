from django import forms

from .basetask import Task
from ..models import FilePathModel


class CopyDataSetTask(Task):

    def execute_base(self, task_model):
        original = task_model.dataset
        for i in range(int(task_model.parameters['nr_times'])):
            copy = self.create_output_dataset(task_model)
            copy.name = '{}-{}'.format(copy.name, i+1)
            copy.save()
            original_files = FilePathModel.objects.filter(dataset=original).all()
            for f in original_files:
                self.create_output_file(f.path, copy)


class CopyDataSetTaskForm(forms.Form):
    nr_times = forms.IntegerField(label='Nr. times to copy', max_value=100, min_value=1)
