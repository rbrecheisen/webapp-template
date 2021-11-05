from .simple.simpletask import SimpleTask, SimpleTaskForm
from .printdataset.task import PrintDataSetTask, PrintDataSetTaskForm
from .copydataset.task import CopyDataSetTask, CopyDataSetTaskForm


TASK_REGISTRY = {
    'SimpleTask': {
        'class': SimpleTask, 'form_class': SimpleTaskForm},
    'PrintDataSetTask': {
        'class': PrintDataSetTask, 'form_class': PrintDataSetTaskForm},
    'CopyDataSetTask': {
        'class': CopyDataSetTask, 'form_class': CopyDataSetTaskForm},
}
