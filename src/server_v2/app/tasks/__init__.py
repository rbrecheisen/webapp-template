from .simple.task import SimpleTask, SimpleTaskForm
from .printdataset.task import PrintDataSetTask, PrintDataSetTaskForm
from .copydataset.task import CopyDataSetTask, CopyDataSetTaskForm
from .checkdicom.task import CheckDicomTask, CheckDicomTaskForm
from .checktagfile.task import CheckTagFileTask, CheckTagFileTaskForm
from .loadtensorflowmodels.task import LoadTensorFlowModelsTask, LoadTensorFlowModelsTaskForm
from .predictbodycompositionscores.task import PredictBodyCompositionScoresTask, PredictBodyCompositionScoresTaskForm


TASK_REGISTRY = {
    'SimpleTask': {
        'class': SimpleTask, 'form_class': SimpleTaskForm},
    'PrintDataSetTask': {
        'class': PrintDataSetTask, 'form_class': PrintDataSetTaskForm},
    'CopyDataSetTask': {
        'class': CopyDataSetTask, 'form_class': CopyDataSetTaskForm},
    'CheckDicomTask': {
        'class': CheckDicomTask, 'form_class': CheckDicomTaskForm},
    'CheckTagFileTask': {
        'class': CheckTagFileTask, 'form_class': CheckTagFileTaskForm},
    'LoadTensorFlowModelsTask': {
        'class': LoadTensorFlowModelsTask, 'form_class': LoadTensorFlowModelsTaskForm},
    'PredictBodyCompositionScoresTask': {
        'class': PredictBodyCompositionScoresTask, 'form_class': PredictBodyCompositionScoresTaskForm},
}
