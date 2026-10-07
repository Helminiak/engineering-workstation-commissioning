import json
import resource
import tempfile
import time
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd
import polars as pl
import scipy.linalg
import statsmodels.api as sm
from numba import njit
from sklearn.linear_model import LinearRegression

ROOT = Path(__file__).resolve().parent.parent
start = time.perf_counter()
checks = {}


def check(name, actual, expected, tol=0):
    assert abs(actual - expected) <= tol, (name, actual, expected)
    checks[name] = {
        "actual": float(actual),
        "expected": float(expected),
        "tolerance": tol,
        "status": "PASS",
    }


a = np.array([[3.0, 1.0], [1.0, 2.0]])
b = np.array([9.0, 8.0])
x = scipy.linalg.solve(a, b)
check("linear_algebra_residual", float(np.linalg.norm(a @ x - b)), 0, 1e-12)
rng = np.random.default_rng(20261006)
draws = rng.normal(size=10000)
same = np.random.default_rng(20261006).normal(size=10000)
check("seed_reproducibility", float(np.max(abs(draws - same))), 0)
data = np.arange(1.0, 101.0)
bootstrap = rng.choice(data, size=(2000, 100), replace=True).mean(axis=1)
lo, hi = np.quantile(bootstrap, [0.025, 0.975])
assert lo < 50.5 < hi
checks["bootstrap"] = {
    "actual_interval": [lo, hi],
    "expected_mean": 50.5,
    "status": "PASS",
}
points = rng.random((100000, 2))
pi = float(4 * np.mean((points**2).sum(axis=1) < 1))
check("monte_carlo_pi", pi, float(np.pi), 0.025)
t = np.arange(100.0)
y = 3 * t + 7
model = sm.OLS(y, sm.add_constant(t)).fit()
check("time_series_trend", model.params[1], 3, 1e-12)
df = pd.DataFrame({"id": range(100), "value": range(100)})
check("dataframe_sum", df.value.sum(), 4950)
with tempfile.TemporaryDirectory(dir=ROOT / "scratch") as d:
    p = Path(d) / "sample.parquet"
    df.to_parquet(p, index=False)
    pd.testing.assert_frame_equal(df, pd.read_parquet(p))
    check("parquet_rows", len(pd.read_parquet(p)), 100)
    check("duckdb_sum", duckdb.sql("select sum(value) from df").fetchone()[0], 4950)
    check("polars_sum", pl.read_parquet(p)["value"].sum(), 4950)
fit = LinearRegression().fit(t.reshape(-1, 1), y)
check("ml_training_max_error", np.max(abs(fit.predict(t.reshape(-1, 1)) - y)), 0, 1e-10)


@njit
def sum_squares(n):
    result = 0
    for i in range(n + 1):
        result += i * i
    return result


check("numba_jit", sum_squares(10), 385)
report = {
    "status": "PASS",
    "runtime_s": time.perf_counter() - start,
    "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    "checks": checks,
}
(ROOT / "evidence/scientific-validation.json").write_text(
    json.dumps(report, indent=2) + "\n"
)
print(json.dumps(report, indent=2))
