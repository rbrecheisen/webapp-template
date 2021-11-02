from .simpletask import SimpleTask, SimpleTaskForm
from .printdatasettask import PrintDataSetTask, PrintDataSetTaskForm
from .copydatasettask import CopyDataSetTask, CopyDataSetTaskForm


TASK_REGISTRY = {
    'SimpleTask': {
        'class': SimpleTask, 'form_class': SimpleTaskForm},
    'PrintDataSetTask': {
        'class': PrintDataSetTask, 'form_class': PrintDataSetTaskForm},
    'CopyDataSetTask': {
        'class': CopyDataSetTask, 'form_class': CopyDataSetTaskForm},
}
