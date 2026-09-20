"""Recompute the TOPSIS ranking using the CORRECTED Table 2, where NE_Arch_B
and Modelo_referencia use the validated 10-run means from section 3.4 of the
article (86.41% and 82.40%) instead of the single-run values originally
published in Table 2 (95.80% and 94.90%).

This is expected to NOT reproduce Table 5 of the published article -- that
is the point: it shows what the AHP-TOPSIS ranking looks like once the
internal inconsistency flagged in docs/DISCREPANCY_NOTE.md is corrected.
"""
import json
import pathlib

from run_topsis_as_published import load_alternatives, load_weights
from topsis import max_min_topsis, print_result

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def main():
    criteria, types, weights = load_weights()
    alts, matrix = load_alternatives(DATA / "table2_architecture_metrics_corrected.csv")

    result = max_min_topsis(alts, criteria, types, weights, matrix)
    print_result(result)

    out = {
        "alternatives": result.alternatives,
        "ranking": result.ranking,
        "cci": {a: float(c) for a, c in zip(result.alternatives, result.cci)},
        "d_positive": {a: float(d) for a, d in zip(result.alternatives, result.d_positive)},
        "d_negative": {a: float(d) for a, d in zip(result.alternatives, result.d_negative)},
        "note": (
            "NE_Arch_B y Modelo_referencia usan la media validada de 10 corridas "
            "(seccion 3.4) en vez del valor de una sola corrida de la Tabla 2 "
            "original. Ver docs/DISCREPANCY_NOTE.md."
        ),
    }
    out_path = ROOT / "topsis" / "results" / "topsis_corrected.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nGuardado en {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
