from .simple.task import SimpleTask, SimpleTaskForm
from .printdataset.task import PrintDataSetTask, PrintDataSetTaskForm
from .copydataset.task import CopyDataSetTask, CopyDataSetTaskForm
from .checkdicomfile.task import CheckDicomFileTask, CheckDicomFileTaskForm
from .checktagfile.task import CheckTagFileTask, CheckTagFileTaskForm
from .predictbodycompositionscores.task import PredictBodyCompositionScoresTask, PredictBodyCompositionScoresTaskForm


TASK_REGISTRY = {
    'SimpleTask': {
        'class': SimpleTask,
        'form_class': SimpleTaskForm
    },
    'PrintDataSetTask': {
        'class': PrintDataSetTask,
        'form_class': PrintDataSetTaskForm
    },
    'CopyDataSetTask': {
        'class': CopyDataSetTask,
        'form_class': CopyDataSetTaskForm
    },
    'CheckDicomFileTask': {
        'class': CheckDicomFileTask,
        'form_class': CheckDicomFileTaskForm
    },
    'CheckTagFileTask': {
        'class': CheckTagFileTask,
        'form_class': CheckTagFileTaskForm
    },
    'PredictBodyCompositionScoresTask': {
        'class': PredictBodyCompositionScoresTask,
        'form_class': PredictBodyCompositionScoresTaskForm
    },
}
