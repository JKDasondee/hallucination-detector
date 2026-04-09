from hallucination_detector import detect

r = detect(
    "The Great Wall of China is visible from space",
    context="The Great Wall of China is not visible from space with the naked eye",
)

print(f"Score: {r.score}")
for c in r.claims:
    print(f"  [{c.label.value}] {c.text} (score={c.score})")
