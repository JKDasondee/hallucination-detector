import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hallucination_detector import detect
from hallucination_detector.models import Label

DATA = Path(__file__).parent / "dataset.json"


def run():
    with open(DATA) as f:
        items = json.load(f)

    tp = fp = tn = fn = 0
    results = []
    t0 = time.time()

    for item in items:
        r = detect(item["text"], context=item["context"])
        pred = "hallucinated" if r.score > 0.5 else "verified"
        gold = item["label"]
        ok = pred == gold

        if gold == "hallucinated" and pred == "hallucinated":
            tp += 1
        elif gold == "verified" and pred == "verified":
            tn += 1
        elif gold == "verified" and pred == "hallucinated":
            fp += 1
        else:
            fn += 1

        results.append({
            "text": item["text"][:60],
            "gold": gold,
            "pred": pred,
            "score": round(r.score, 4),
            "ok": ok,
        })

    elapsed = time.time() - t0
    n = len(items)
    prec = tp / (tp + fp) if (tp + fp) > 0 else 0
    rec = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0
    acc = (tp + tn) / n

    print("=" * 70)
    print("HALLUCINATION DETECTOR — BENCHMARK RESULTS")
    print("=" * 70)
    print(f"Dataset: {n} items ({sum(1 for i in items if i['label']=='hallucinated')} hallucinated, {sum(1 for i in items if i['label']=='verified')} verified)")
    print(f"Time: {elapsed:.1f}s ({elapsed/n:.2f}s per claim)")
    print()
    print(f"  Accuracy:  {acc:.1%}")
    print(f"  Precision: {prec:.1%}")
    print(f"  Recall:    {rec:.1%}")
    print(f"  F1 Score:  {f1:.1%}")
    print()
    print(f"  TP={tp}  FP={fp}")
    print(f"  FN={fn}  TN={tn}")
    print()
    print("-" * 70)
    print(f"{'Text':<62} {'Gold':<14} {'Pred':<14} {'Score':>6} {'OK'}")
    print("-" * 70)
    for r in results:
        mark = "+" if r["ok"] else "X"
        print(f"{r['text']:<62} {r['gold']:<14} {r['pred']:<14} {r['score']:>6.4f} {mark}")
    print("-" * 70)


if __name__ == "__main__":
    run()
