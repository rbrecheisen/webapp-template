import os
import django_rq

from django.conf import settings
from django.db.models.fields.files import FieldFile


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
        with open(os.path.join(settings.FILE_UPLOAD_TEMP_DIR, 'MyQuickTask.csv'), 'w') as f:
            f.write('some text\n')


class MyLongRunningTask:

    def __init__(self):
        self.name = 'MyLongRunningTask'

    @django_rq.job
    def execute(self, dataset):
        print('Executing a long-running task...')
        for i in range(1000):
            with open(os.path.join(
                    settings.FILE_UPLOAD_TEMP_DIR, 'MyLongRunningTask-{:04d}.csv'.format(i)), 'w') as f:
                f.write('some text\n')


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
