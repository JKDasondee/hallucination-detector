from hallucination_detector.core import Detector, detect
from hallucination_detector.coverage import coverage_score, omission_risk
from hallucination_detector.models import Claim, DetectionResult
from hallucination_detector.selfcheck import score_by_consistency, selfcheck_nli

__version__ = "0.3.0"
__all__ = [
    "detect",
    "Detector",
    "Claim",
    "DetectionResult",
    "score_by_consistency",
    "selfcheck_nli",
    "coverage_score",
    "omission_risk",
]
