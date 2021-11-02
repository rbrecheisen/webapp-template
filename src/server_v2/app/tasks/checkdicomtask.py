import pydicom
import pydicom.errors

from django import forms

from .basetask import Task
from ..models import FilePathModel


class CheckDicomTask(Task):

    def execute_base(self, task_model):
        files = FilePathModel.objects.filter(dataset=task_model.dataset).all()
        errors = []
        for f in files:
            try:
                p = pydicom.dcmread(f.path, stop_before_pixels=True)
            except pydicom.errors.InvalidDicomError:
                errors.append('{}: not DICOM'.format(f.path))
                continue
            required_tags = [x.strip() for x in task_model.parameters['required_tags'].split(',')]
            missing_tag = False
            for tag in required_tags:
                if tag not in p:
                    errors.append('{}: missing tag "{}"'.format(f.path, tag))
                    missing_tag = True
                    break
            if missing_tag:
                continue
            required_rows = int(task_model.parameters['required_rows'])
            if p.Rows != required_rows:
                errors.append('{}: rows {} instead of {}'.format(f.path, p.Rows, required_rows))
                continue
            required_cols = int(task_model.parameters['required_cols'])
            if p.Columns != required_cols:
                errors.append('{}: columns {} instead of {}'.format(f.path, p.Columns, required_cols))
                continue
        if len(errors) > 0:
            task_model.errors = errors
            task_model.job_status = 'failed'
            task_model.save()


class CheckDicomTaskForm(forms.Form):
    required_tags = forms.CharField(label='Required tags', max_length=1024, empty_value='P')
    required_rows = forms.IntegerField(label='Required nr. rows')
    required_cols = forms.IntegerField(label='Required nr. columns')
