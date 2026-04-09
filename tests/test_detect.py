from hallucination_detector import Claim, DetectionResult, Detector, detect
from hallucination_detector.models import Label


def test_detect_returns_result():
    r = detect("The sky is blue.")
    assert isinstance(r, DetectionResult)
    assert isinstance(r.score, float)
    assert 0.0 <= r.score <= 1.0
    assert r.text == "The sky is blue."


def test_detect_with_context():
    r = detect("The Eiffel Tower is in London", context="The Eiffel Tower is in Paris, France")
    assert isinstance(r, DetectionResult)
    assert len(r.claims) > 0
    for c in r.claims:
        assert isinstance(c, Claim)
        assert c.evidence == "The Eiffel Tower is in Paris, France"


def test_detect_empty_input():
    r = detect("")
    assert isinstance(r, DetectionResult)
    assert r.claims == []
    assert r.score == 0.0


def test_claim_labels():
    for lb in Label:
        c = Claim(text="test", label=lb)
        assert c.label == lb


def test_detector_instance():
    d = Detector()
    r = d.run("Water boils at 100 degrees Celsius.")
    assert isinstance(r, DetectionResult)
    assert len(r.claims) >= 1


def test_claim_score_bounds():
    r = detect("Fact one. Fact two. Fact three.", context="Fact one is true")
    for c in r.claims:
        assert 0.0 <= c.score <= 1.0
