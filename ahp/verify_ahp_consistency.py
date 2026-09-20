"""Verify the AHP consistency ratio reported in Table 1 of the article.

IMPORTANT: the original 4x4 pairwise comparison matrix filled in by the five
expert judges was not made available to reconstruct this repository (see
docs/DISCREPANCY_NOTE.md). This script does NOT fabricate that matrix.

Instead, it independently re-derives the Consistency Index (CI) and
Consistency Ratio (CR) from the single number the article does report,
lambda_max = 4.0342, using Saaty's standard formulas and the published
Random Index (RI) table, and checks that this reproduces the article's own
CI = 0.0114 and CR = 0.0127 (1.27%).
"""

from __future__ import annotations

# Saaty's Random Index table (Saaty, 1980), indexed by matrix size n.
RANDOM_INDEX = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}


def consistency_ratio(lambda_max: float, n: int) -> tuple[float, float, float]:
    ci = (lambda_max - n) / (n - 1)
    ri = RANDOM_INDEX[n]
    cr = ci / ri if ri > 0 else 0.0
    return ci, ri, cr


def main() -> None:
    lambda_max = 4.0342
    n = 4
    weights = [0.6112, 0.2593, 0.0651, 0.0645]  # Table 1, as published

    ci, ri, cr = consistency_ratio(lambda_max, n)

    print("Verificacion independiente de la matriz AHP (Tabla 1)")
    print("=" * 55)
    print(f"n (criterios)          = {n}")
    print(f"lambda_max (publicado) = {lambda_max}")
    print(f"RI (Saaty, n=4)        = {ri}")
    print(f"CI calculado           = {ci:.4f}   (publicado: 0.0114)")
    print(f"CR calculado           = {cr:.4f}   (publicado: 0.0127)")
    print(f"CR < 0.10 -> {'ACEPTABLE' if cr < 0.10 else 'NO ACEPTABLE'}")

    w_sum = sum(weights)
    print(f"\nSuma de pesos w1..w4   = {w_sum:.4f} (debe ser ~1.0000)")

    print(
        "\nNOTA: esto confirma que CI y CR son aritmeticamente consistentes con el "
        "lambda_max publicado. No demuestra ni reconstruye la matriz de "
        "comparaciones pareadas original de los 5 expertos, que no esta "
        "disponible (ver docs/DISCREPANCY_NOTE.md)."
    )


if __name__ == "__main__":
    main()
