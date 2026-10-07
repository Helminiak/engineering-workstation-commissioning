"""Descriptive forensic correlation and benchmark regression checks."""

import math
import statistics


def pearson(x, y):
    if len(x) != len(y) or len(x) < 3 or not all(math.isfinite(v) for v in [*x, *y]):
        raise ValueError("At least three paired finite values required")
    mx = statistics.mean(x)
    my = statistics.mean(y)
    covariance = sum((a - mx) * (b - my) for a, b in zip(x, y))
    den = math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
    if den == 0:
        raise ValueError("Constant series has undefined correlation")
    return covariance / den


def performance_regression(baseline, current, threshold=0.1):
    if (
        len(baseline) < 3
        or len(current) < 3
        or not all(math.isfinite(v) and v > 0 for v in [*baseline, *current])
    ):
        raise ValueError("At least three positive finite timings required")
    old = statistics.median(baseline)
    new = statistics.median(current)
    ratio = new / old - 1
    return {
        "baseline_median": old,
        "current_median": new,
        "relative_change": ratio,
        "threshold": threshold,
        "regression": ratio > threshold,
        "method": "Median ratio; descriptive flag, not a statistical significance test",
    }
