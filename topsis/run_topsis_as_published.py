"""Recompute the TOPSIS ranking from Table 2 exactly as published in the
article (NE_Arch_B C1 = 95.80%), to verify it reproduces Tables 3-5.
"""
import csv
import json
import pathlib

import numpy as np

from topsis import max_min_topsis, print_result

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def load_weights():
    names, types, weights = [], [], []
    with open(DATA / "table1_ahp_weights.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            names.append(row["criterio"])
            types.append(row["tipo"])
            weights.append(float(row["peso"]))
    return names, types, weights


def load_alternatives(path):
    alts, matrix = [], []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(row for row in f if not row.lstrip().startswith("#"))
        for row in reader:
            alts.append(row["arquitectura"])
            matrix.append(
                [
                    float(row["C1_precision_test_pct"]),
                    float(row["C2_tiempo_inferencia_ms"]),
                    float(row["C3_parametros_millones"]),
                    float(row["C4_capacidad_optimizacion"]),
                ]
            )
    return alts, np.array(matrix)


def main():
    criteria, types, weights = load_weights()
    alts, matrix = load_alternatives(DATA / "table2_architecture_metrics_as_published.csv")

    result = max_min_topsis(alts, criteria, types, weights, matrix)
    print_result(result)

    out = {
        "alternatives": result.alternatives,
        "ranking": result.ranking,
        "cci": {a: float(c) for a, c in zip(result.alternatives, result.cci)},
        "d_positive": {a: float(d) for a, d in zip(result.alternatives, result.d_positive)},
        "d_negative": {a: float(d) for a, d in zip(result.alternatives, result.d_negative)},
    }
    out_path = ROOT / "topsis" / "results" / "topsis_as_published.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nGuardado en {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
