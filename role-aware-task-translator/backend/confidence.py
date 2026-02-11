import math

def compute_retrieval_confidence(matches, weights=None):
    """
    Computes confidence using weighted Top-K similarity scores
    """

    if not matches:
        return 0.0

    scores = [m.score for m in matches]

    # ---- Step 1: Normalize scores ----
    score_sum = sum(scores)
    if score_sum == 0:
        return 0.0

    normalized = [s / score_sum for s in scores]

    # ---- Step 2: Weights ----
    if not weights:
        # Default decaying weights
        weights = [0.5, 0.3, 0.2]

    # Trim to min length
    k = min(len(normalized), len(weights))
    weighted_confidence = 0.0

    for i in range(k):
        weighted_confidence += normalized[i] * weights[i]

    # ---- Step 3: Optional Top-1 dominance boost ----
    top1 = scores[0]
    top2 = scores[1] if len(scores) > 1 else 0

    margin = top1 - top2

    if margin > 0.15:
        weighted_confidence += 0.05
    elif margin < 0.05:
        weighted_confidence *= 0.85

    # ---- Step 4: Scale to percentage ----
    confidence_percent = min(weighted_confidence * 100, 100)

    return round(confidence_percent, 2)
