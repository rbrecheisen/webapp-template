from .MyQuickTask import MyQuickTask
from .MyLongRunningTask import MyLongRunningTask
from .PredictBodyCompositionTask import PredictBodyCompositionScoresTask
from .ValidateBodyCompositionTask import ValidateBodyCompositionScoresTask
from .CheckDicomTask import CheckDicomTask


TASK_REGISTRY = {
    'MyQuickTask': MyQuickTask,
    'MyLongRunningTask': MyLongRunningTask,
    'PredictBodyCompositionScoresTask': PredictBodyCompositionScoresTask,
    'ValidateBodyCompositionScoresTask': ValidateBodyCompositionScoresTask,
    'CheckDicomTask': CheckDicomTask,
}

TASK_FORM_REGISTRY = {
}
