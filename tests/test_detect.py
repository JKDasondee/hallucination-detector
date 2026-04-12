from hallucination_detector import Claim, DetectionResult, Detector, detect
from hallucination_detector.models import Label


def test_detect_returns_result():
    r = detect("The Eiffel Tower was built in Paris, France in 1889.")
    assert isinstance(r, DetectionResult)
    assert isinstance(r.score, float)
    assert 0.0 <= r.score <= 1.0


def test_detect_with_context():
    r = detect(
        "The Eiffel Tower is located in London, England and was built in 1900.",
        context=(
            "The Eiffel Tower is a wrought-iron lattice tower in Paris, France."
            " It was constructed from 1887 to 1889."
        ),
    )
    assert isinstance(r, DetectionResult)
    for c in r.claims:
        assert isinstance(c, Claim)
        assert len(c.evidence) > 0


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
    r = d.run(
        "Albert Einstein was born in Ulm, Germany on March 14, 1879.",
        context="Albert Einstein was born on 14 March 1879 in Ulm, in the Kingdom of Württemberg in the German Empire.",
    )
    assert isinstance(r, DetectionResult)


def test_claim_score_bounds():
    r = detect(
        "Paris is the capital of France with a population of 2.1 million people.",
        context="Paris is the capital and most populous city of France, with a population of over 2.1 million.",
    )
    for c in r.claims:
        assert 0.0 <= c.score <= 1.0


def test_hallucinated_claim_detected():
    r = detect(
        "Napoleon Bonaparte was born in Moscow, Russia in 1769.",
        context="Napoleon Bonaparte was born on 15 August 1769 in Ajaccio, Corsica, France.",
    )
    if r.claims:
        assert any(c.label == Label.HALLUCINATED or c.score > 0.3 for c in r.claims)


def test_verified_claim_detected():
    r = detect(
        "Tokyo is the capital of Japan.",
        context="Tokyo is the capital city of Japan and one of the most populous cities in the world.",
    )
    if r.claims:
        assert any(c.label == Label.VERIFIED or c.score < 0.3 for c in r.claims)


def test_detect_with_samples_selfcheck():
    r = detect(
        "Paris is the capital of France.",
        samples=[
            "Paris is the capital of France.",
            "France's capital city is Paris.",
            "The capital of France is Paris.",
        ],
    )
    assert isinstance(r, DetectionResult)
    assert 0.0 <= r.score <= 1.0


def test_selfcheck_nli_function():
    from hallucination_detector import selfcheck_nli

    score = selfcheck_nli(
        "The moon is made of cheese.",
        ["The moon is a rocky body.", "The moon is not made of cheese."],
    )
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0


def test_detect_no_context_no_samples():
    r = detect("Random text without context.")
    assert isinstance(r, DetectionResult)
