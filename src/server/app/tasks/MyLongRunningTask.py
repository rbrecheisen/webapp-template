import os

from django.conf import settings
from django import forms

from .BaseTask import Task


class MyLongRunningTask(Task):

    def execute_base(self, task_model):
        ds = self.create_output_dataset(task_model)
        for i in range(int(task_model.parameters['nr_iterations'])):
            file_path = os.path.join(settings.MEDIA_ROOT, '{:04d}.txt'.format(i))
            with open(file_path, 'w') as f:
                f.write('some text\n')
            self.create_output_file(file_path, ds)
        task_model.info_message = 'Successfully executed long-running task'


class MyLongRunningTaskForm(forms.Form):
    nr_iterations = forms.IntegerField(label='Nr. iterations', min_value=1, max_value=1000)
