from .BaseTask import Task, TaskExecutionError

from barbell2light.dicom import is_dicom_file


class CheckDicomTask(Task):

    @staticmethod
    def execute_base(task_model):
        """
        The purpose of this task is to check a list of DICOM files. Each file
        is checked for a number of conditions. Files that do not satisfy the
        conditions result in an error message (viewable via task's error info).
        A new dataset is created that contains file paths for those files
        satisfying all conditions.
        """
        raise TaskExecutionError('Not implemented yet')
