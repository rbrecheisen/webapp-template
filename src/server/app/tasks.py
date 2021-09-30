import os
import django_rq

from .backend import create_dataset
from django.core.files.uploadedfile import TemporaryUploadedFile


class TaskError(Exception):
    pass


class TaskUnknownError(TaskError):
    pass


class MyQuickTask:

    def __init__(self):
        self.name = 'MyQuickTask'

    @django_rq.job
    def execute(self, dataset):
        print('Executing a quick task...')
        txt = 'some text\n'
        f = TemporaryUploadedFile('MyQuickTask.csv', 'text/plain', len(txt), 'utf-8')
        f.file.write(txt)
        f.file.seek(0)
        create_dataset([f], None)


class MyLongRunningTask:

    def __init__(self):
        self.name = 'MyLongRunningTask'

    @django_rq.job
    def execute(self, dataset):
        print('Executing a long-running task...')
        for i in range(1000):
            print(i)


class PredictBodyCompositionScoresTask:

    def __init__(self):
        self.name = 'PredictBodyCompositionScoresTask'

    @django_rq.job
    def execute(self, dataset):
        """ What should this task do? It applies our deep learning model to each file in the
        dataset and then calculates a number of scores as well as a PNG image of the result.
        """
        pass


class ValidateBodyCompositionScoresTask:

    def __init__(self):
        self.name = 'ValidateBodyCompositionScoresTask'

    @django_rq.job
    def execute(self, dataset):
        pass


TASK_REGISTRY = {
    'MyQuickTask': MyQuickTask(),
    'MyLongRunningTask': MyLongRunningTask(),
    'PredictBodyCompositionScoresTask': PredictBodyCompositionScoresTask(),
    'ValidateBodyCompositionScoresTask': ValidateBodyCompositionScoresTask(),
}
