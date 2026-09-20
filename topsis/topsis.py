"""Generic Max-Min TOPSIS implementation.

Reproduces the procedure described in Castro Pinza, Vera Pinargote, Rumbaut Rangel
& Leyva Vazquez, "Modelo hibrido de neuroevolucion para optimizar arquitecturas DNN
con AHP-TOPSIS", Neutrosophic Computing and Machine Learning, Vol. 44 (2026),
section 2.2 ("En la tercera fase se aplico TOPSIS con normalizacion Max-Min").

Criteria types: 'benefit' (higher is better) or 'cost' (lower is better).
Normalization matches the article: for cost criteria the normalized score is
inverted so that 1.0 always corresponds to the most convenient value.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class TopsisResult:
    alternatives: list[str]
    criteria: list[str]
    normalized: np.ndarray
    weighted: np.ndarray
    ideal_positive: np.ndarray
    ideal_negative: np.ndarray
    d_positive: np.ndarray
    d_negative: np.ndarray
    cci: np.ndarray
    ranking: list[str]


def max_min_topsis(
    alternatives: list[str],
    criteria: list[str],
    types: list[str],
    weights: list[float],
    matrix: np.ndarray,
) -> TopsisResult:
    matrix = np.asarray(matrix, dtype=float)
    weights = np.asarray(weights, dtype=float)
    n_alt, n_crit = matrix.shape
    assert len(alternatives) == n_alt
    assert len(criteria) == n_crit == len(types) == len(weights)
    assert abs(weights.sum() - 1.0) < 1e-3, "AHP weights must sum to 1"

    normalized = np.zeros_like(matrix)
    for j, kind in enumerate(types):
        col = matrix[:, j]
        col_min, col_max = col.min(), col.max()
        span = col_max - col_min
        if span == 0:
            normalized[:, j] = 1.0
            continue
        if kind == "benefit":
            normalized[:, j] = (col - col_min) / span
        elif kind == "cost":
            normalized[:, j] = (col_max - col) / span
        else:
            raise ValueError(f"unknown criterion type: {kind}")

    weighted = normalized * weights
    ideal_positive = weighted.max(axis=0)
    ideal_negative = weighted.min(axis=0)

    d_positive = np.sqrt(((weighted - ideal_positive) ** 2).sum(axis=1))
    d_negative = np.sqrt(((weighted - ideal_negative) ** 2).sum(axis=1))
    with np.errstate(invalid="ignore", divide="ignore"):
        cci = d_negative / (d_positive + d_negative)
    cci = np.nan_to_num(cci)

    order = np.argsort(-cci)
    ranking = [alternatives[i] for i in order]

    return TopsisResult(
        alternatives=alternatives,
        criteria=criteria,
        normalized=normalized,
        weighted=weighted,
        ideal_positive=ideal_positive,
        ideal_negative=ideal_negative,
        d_positive=d_positive,
        d_negative=d_negative,
        cci=cci,
        ranking=ranking,
    )


def print_result(result: TopsisResult) -> None:
    print(f"{'Alternativa':<20}" + "".join(f"{c:>12}" for c in result.criteria) + f"{'D+':>10}{'D-':>10}{'CCi':>10}")
    for i, name in enumerate(result.alternatives):
        row = "".join(f"{v:12.4f}" for v in result.weighted[i])
        print(f"{name:<20}{row}{result.d_positive[i]:10.4f}{result.d_negative[i]:10.4f}{result.cci[i]:10.4f}")
    print("\nRanking (mejor a peor):")
    for pos, name in enumerate(result.ranking, start=1):
        idx = result.alternatives.index(name)
        print(f"  {pos}. {name}  (CCi = {result.cci[idx]:.4f})")
