from ..models import DataSetModel, FilePathModel


class TaskError(Exception):
    pass


class TaskUnknownError(TaskError):
    pass


class TaskExecutionError(TaskError):
    pass


class Task:

    @staticmethod
    def create_output_dataset(task_model):
        ds_name = '{}-{}'.format(task_model.get_dataset.name, task_model.name)
        ds = DataSetModel.objects.create(name=ds_name, owner=task_model.get_dataset.owner)
        return ds

    @staticmethod
    def create_output_file(file_path, dataset):
        return FilePathModel.objects.create(file_path=file_path, dataset=dataset)

    def execute(self, task_model):
        print('Executing task {}...'.format(task_model.name))
        task_model.job_status = 'running'
        task_model.save()
        try:
            self.execute_base(task_model)
            task_model.job_status = 'finished'
            task_model.save()
        except TaskExecutionError as e:
            task_model.job_status = 'failed'
            task_model.error_message = str(e)
            task_model.save()

    @staticmethod
    def execute_base(task_model):
        raise NotImplementedError()
