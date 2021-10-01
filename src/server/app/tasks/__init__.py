from .MyQuickTask import MyQuickTask
from .MyLongRunningTask import MyLongRunningTask
from .PredictBodyCompositionTask import PredictBodyCompositionScoresTask
from .ValidateBodyCompositionTask import ValidateBodyCompositionScoresTask


TASK_REGISTRY = {
    'MyQuickTask': MyQuickTask(),
    'MyLongRunningTask': MyLongRunningTask(),
    'PredictBodyCompositionScoresTask': PredictBodyCompositionScoresTask(),
    'ValidateBodyCompositionScoresTask': ValidateBodyCompositionScoresTask(),
}
