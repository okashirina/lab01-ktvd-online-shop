"""Единые статистические преобразования для ноутбука и тестов."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats


PAGE_BINS = [-0.5, 0.5, 5.5, 15.5, 30.5, 60.5, float("inf")]
PAGE_LABELS = ["0", "1–5", "6–15", "16–30", "31–60", "61+"]


def load_sessions(path: str = "data/online_shoppers_intention.csv") -> pd.DataFrame:
    frame = pd.read_csv(path)
    required = {"ProductRelated", "Revenue", "VisitorType", "Weekend", "Month"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Нет обязательных столбцов: {sorted(missing)}")
    result = frame.copy()
    result["ProductRelated"] = pd.to_numeric(result["ProductRelated"], errors="raise").astype(int)
    result["Revenue"] = result["Revenue"].astype(int)
    if not result["ProductRelated"].ge(0).all() or not result["Revenue"].isin([0, 1]).all():
        raise ValueError("Некорректные значения случайных величин")
    return result


def contingency_analysis(frame: pd.DataFrame) -> tuple[pd.DataFrame, float, float, int, float, float]:
    grouped = pd.cut(frame["ProductRelated"], bins=PAGE_BINS, labels=PAGE_LABELS)
    observed = pd.crosstab(grouped, frame["Revenue"], dropna=False)
    chi2, p_value, df, expected = stats.chi2_contingency(observed, correction=False)
    n = observed.to_numpy().sum()
    cramer_v = np.sqrt(chi2 / (n * min(observed.shape[0] - 1, observed.shape[1] - 1)))
    return observed, float(chi2), float(p_value), int(df), float(expected.min()), float(cramer_v)


def wilson_interval(successes: int, trials: int, alpha: float = 0.05) -> tuple[float, float]:
    if trials <= 0:
        raise ValueError("trials должен быть положительным")
    z = stats.norm.ppf(1 - alpha / 2)
    p = successes / trials
    denominator = 1 + z**2 / trials
    center = (p + z**2 / (2 * trials)) / denominator
    radius = z * np.sqrt(p * (1 - p) / trials + z**2 / (4 * trials**2)) / denominator
    return float(center - radius), float(center + radius)

