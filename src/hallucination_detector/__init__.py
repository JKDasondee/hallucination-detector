from hallucination_detector.core import Detector, detect
from hallucination_detector.models import Claim, DetectionResult
from hallucination_detector.selfcheck import score_by_consistency, selfcheck_nli

__version__ = "0.2.0"
__all__ = [
    "detect",
    "Detector",
    "Claim",
    "DetectionResult",
    "score_by_consistency",
    "selfcheck_nli",
]
