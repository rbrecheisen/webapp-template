import numpy as np

from django import forms

from ..basetask import Task
from ...models import FilePathModel

from barbell2light.dicom import is_tag_file, get_tag_pixels


class CheckTagFileTask(Task):

    def execute_base(self, task_model):
        files = FilePathModel.objects.filter(dataset=task_model.dataset).all()
        errors = []
        for f in files:
            if is_tag_file(f.path):
                tag_pixels = get_tag_pixels(f.path)
                required_labels = [x.strip() for x in task_model.parameters['required_labels'].split(',')]
                missing_label = False
                for label in required_labels:
                    if label not in tag_pixels:
                        errors.append('{}: missing label {}'.format(f.path, label))
                        missing_label = True
                        break
                if missing_label:
                    continue
                wrong_label = False
                for label in np.unique(tag_pixels):
                    if label not in required_labels:
                        errors.append('{}: wrong label {}'.format(f.path, label))
                        wrong_label = True
                        break
                if wrong_label:
                    continue
        if len(errors) > 0:
            task_model.errors = errors
            task_model.job_status = 'failed'
            task_model.save()


class CheckDicomTaskForm(forms.Form):
    required_tags = forms.CharField(label='Required tags', max_length=1024, empty_value='P')
    required_rows = forms.IntegerField(label='Required nr. rows')
    required_cols = forms.IntegerField(label='Required nr. columns')
