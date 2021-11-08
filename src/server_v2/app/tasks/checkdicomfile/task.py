import pydicom
import pydicom.errors

from django import forms

from .dicom_checker import DicomChecker
from ..basetask import Task
from ...models import FilePathModel


class CheckDicomFileTask(Task):

    def execute_base(self, task_model):
        files = FilePathModel.objects.filter(dataset=task_model.dataset).all()
        dicom_checker = DicomChecker(files)
        dicom_checker.set_required_tags(
            [x.strip() for x in task_model.parameters['required_tags'].split(',')])
        dicom_checker.set_required_dimensions(
            int(task_model.parameters['required_rows']),
            int(task_model.parameters['required_cols']))
        errors = dicom_checker.execute()
        if len(errors) > 0:
            task_model.errors = errors
            task_model.job_status = 'failed'
            task_model.save()


class CheckDicomFileTaskForm(forms.Form):
    required_tags = forms.CharField(label='Required tags', max_length=1024, empty_value='')
    required_rows = forms.IntegerField(label='Required nr. rows')
    required_cols = forms.IntegerField(label='Required nr. columns')
