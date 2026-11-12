"""Write tests/fixtures/course_fixture.json: results of the course scripts' own Python code (via web/compute.py)
that the browser's JavaScript engines must reproduce. web/static/engines.test.mjs replays every case through
js_compute.js; tests/test_web.py checks this file is still what the Python code produces.

Run: python scripts/make_course_fixture.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from test_regressions import _ip3r_mrna  # noqa: E402  (synthetic mRNA with a known CDS)
from web.compute import data_tables, run  # noqa: E402

OUT = ROOT / "tests" / "fixtures" / "course_fixture.json"
SEQ = ("ATGTCTGACAAAATGTCTAGCTTTCTACATATTGGAGACATTTGCTCTCTGTATGCGGAGGGATCCACGAATGGATTTATTTCAACTTTAGGTTTGGTTGATGATCGT"
       "TGTGTTGTACAGCCAGAAGCCGGAGATCTTAATAACCCACCCAAGAAATTCAGAGACTGCCTCTTTAAGCTATGTCCTATGAATCGATACTCCGCACAGAAGCAGTT"
       "NNACGU")   # the trailing N and U exercise the input cleaning

CASES = {
    "numerals": [{"n": n} for n in (0, 1, 4, 9, 10, 20, 59, 60, 100, 121, 1001, 1994, 2020, 2024, 3600, 3642, 3888,
                                    10000, 99999, 100000, 1234567)],
    "egyptian_multiply": [{"a": 14, "b": 12}, {"a": 13, "b": 17}, {"a": 8, "b": 16}, {"a": 7, "b": 0}, {"a": 99, "b": 1}],
    "babylonian_sqrt": [{"n": 2}, {"n": 0}, {"n": 9, "iterations": 3}, {"n": 1e6, "iterations": 30}, {"n": 0.25}],
    "gcd": [{"a": 48, "b": 18}, {"a": 18, "b": 48}, {"a": 0, "b": 7}, {"a": 7, "b": 0}, {"a": 1071, "b": 462},
            {"a": 17, "b": 13}],
    "diophantine": [{"a": 15, "b": 21, "c": 12}, {"a": 15, "b": 21, "c": 13}, {"a": -4, "b": 6, "c": 2},
                    {"a": 3, "b": -7, "c": 1}],
    "primes": [{"limit": 2, "n": 1}, {"limit": 100, "n": 840}, {"limit": 1000, "n": 9973}, {"limit": 30, "n": 3456}],
    "dna_length": [{"length": n} for n in (1, 147, 150, 294, 300, 3456, 997, 2)],
    "cicada": [{"years": 100, "predators": [2, 3, 4, 6, 8, 9, 10]}, {"years": 17, "predators": [5]},
               {"years": 1000, "predators": [2, 3]}],
    "genetic_sequences": [{"lengths": [612, 918, 1224]}, {"lengths": [7, 11]}, {"lengths": [300]}],
    "phyllotaxis": [{"n": 50, "alpha": 137.5}, {"n": 20, "alpha": 130.0}, {"n": 1, "alpha": 90}],
    "gene_lengths": [{"lengths": [610, 987, 1597, 2584]}, {"lengths": [100, 160, 200]}, {"lengths": [5]}],
    "sequence_length": [{"length": n} for n in (2584, 1, 2, 7, 64, 100, 612, 3456, 121)],
    "tree": [{"branching_angle": 30, "depth": 5, "length_decay": 0.7}, {"branching_angle": 45, "depth": 4,
                                                                       "length_decay": 0.6, "angle": 80, "length": 2}],
    "shell_spiral": [{"n_points": 40, "growth_rate": 0.1, "tightness": 1.0},
                     {"n_points": 25, "growth_rate": 0.2, "tightness": 0.8}],
    "population": [{"initial_pop": 100, "growth_rate": 0.1, "carrying_capacity": 1000, "time_steps": 100, "model": m}
                   for m in ("exponential", "logistic", "allee")] +
                  [{"initial_pop": 10, "growth_rate": 2.5, "carrying_capacity": 500, "time_steps": 40, "model": "logistic"}],
    "advanced_tree": [{"species": sp, "season": se, "light_direction": ld, "nutrient_level": nu, "stress": st, "seed": sd}
                      for sp, se, ld, nu, st, sd in (("oak", "summer", 90, 1.0, 0.0, 1), ("pine", "winter", 60, 0.8, 0.3, 7),
                                                     ("birch", "spring", 120, 0.5, 1.0, 12345), ("oak", "autumn", 90, 1.0, 0.0, 0))],
    "tree_stats": [{"species": "oak"}, {"species": "pine"}],
    "tree_compare": [{"species": "oak", "seed": 1}, {"species": "pine", "seed": 42}],
    "shell3d": [{"species": "nautilus", "n_whorls": 4, "n_points": 60}, {"species": "gastropod", "n_whorls": 2.5, "n_points": 30},
                {"species": "ammonite", "n_whorls": 3, "n_points": 30, "growth_rate": 0.306}],
    "shell_stats": [{}],
    "sequence": [{"seq": SEQ, "mrna": False}, {"seq": SEQ * 3, "mrna": True}, {"seq": "GGCC" * 60 + "AT", "mrna": False}],
    "ip3r": [{"seq": "GATGACAACTCC" * 250}, {"seq": (SEQ * 40)}, {"seq": _ip3r_mrna(2800, motif_at=2300)[0]},
             {"seq": "CCC" + _ip3r_mrna(700)[0]}],
}


def build() -> dict:
    return {"data": data_tables(), "cases": {name: [{"params": p, "result": run(name, p)} for p in cases] for name, cases in CASES.items()}}


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    data = build()
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    print(f"wrote {OUT} ({sum(len(v) for v in data['cases'].values())} cases, {OUT.stat().st_size / 1e3:.0f} kB)")
