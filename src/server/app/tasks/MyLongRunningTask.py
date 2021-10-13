import os

from django.conf import settings

from .BaseTask import Task


class MyLongRunningTask(Task):

    def execute_base(self, task_model):
        ds = self.create_output_dataset(task_model)
        for i in range(1000):
            file_path = os.path.join(settings.MEDIA_ROOT, '{:04d}.txt'.format(i))
            with open(file_path, 'w') as f:
                f.write('some text\n')
            self.create_output_file(file_path, ds)
        task_model.info_message = 'Successfully executed long-running task'
