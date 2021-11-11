from django import forms

from ..basetask import Task


class Numpy2DcmTask(Task):
    """ This task takes a dataset with DICOM files and corresponding NumPy array files and
    tries to create a fake DICOM for each NumPy array file such that it can be displayed in a
    regular DICOM viewer. This requires that the labels inside the NumPy array are properly
    scaled to gray value ranges that are distinguishable from each other and can be assessed.
    """
    def execute_base(self, task_model):
        pass


class Numpy2DcmTaskForm(forms.Form):
    pass
