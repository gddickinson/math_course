"""Python reference results for the interactive figures: thin wrappers that call the course scripts' own classes.

Every function takes a dict of parameters and returns plain JSON. The browser's JavaScript engines
(web/static/*_engine.js, registered in js_compute.js under the same names) must give the same answers:
scripts/make_course_fixture.py stores these results in tests/fixtures/course_fixture.json for the node tests, and the
local app's "Check with Python" button calls POST /api/python/<name> to compare a live figure with this code.
"""
import random
import sys
import warnings
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")   # the scripts import pyplot; the server never opens windows

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ancient_calculations import BabylonianSquareRoot, EgyptianMultiplication  # noqa: E402
from ancient_numbers import BabylonianNumber, EgyptianNumber  # noqa: E402
from advanced_tree_patterns import AdvancedTreeModel  # noqa: E402
from bio_growth_patterns import BioGrowthPatterns  # noqa: E402
from bio_math_enhanced import MathematicalPatternAnalyzer  # noqa: E402
from bio_math_patterns import BioMathPatterns  # noqa: E402
from bio_number_theory import BioNumberTheory  # noqa: E402
from number_theory_basics import NumberTheory  # noqa: E402
from shell_comparative_analysis import ShellComparativeAnalysis  # noqa: E402
from shell_growth_patterns import ShellGrowthAnalysis  # noqa: E402
from tree_data_analysis import TreeDataAnalysis  # noqa: E402
from world_numbers import ChineseNumeral, MayanNumeral, RomanNumeral  # noqa: E402
from web.compute_seq import sequence, ip3r  # noqa: E402,F401  (registered below)


def _f(a):
    return [float(v) for v in np.asarray(a, dtype=float)]


def _try(fn):
    try:
        return fn()
    except (ValueError, KeyError):
        return None


def numerals(p):
    n = int(p["n"])
    return {"egyptian": _try(lambda: EgyptianNumber(n).egyptian),
            "babylonian": _try(lambda: BabylonianNumber(n).sexagesimal),
            "babylonian_text": _try(lambda: BabylonianNumber(n).format_sexagesimal()),
            "roman": _try(lambda: RomanNumeral(n).roman), "roman_classical": _try(lambda: RomanNumeral(n).classical),
            "mayan": _try(lambda: MayanNumeral(n).vigesimal), "mayan_text": _try(lambda: MayanNumeral(n).format_mayan()),
            "chinese": _try(lambda: ChineseNumeral(n).chinese)}


def egyptian_multiply(p):
    em = EgyptianMultiplication(int(p["a"]), int(p["b"]))
    result = em.multiply()
    return {"result": result, "steps": em.steps}


def babylonian_sqrt(p):
    b = BabylonianSquareRoot(float(p["n"]), iterations=int(p.get("iterations", 10)))
    return {"result": float(b.calculate()), "steps": b.steps}


def gcd(p):
    nt = NumberTheory()
    g, steps = nt.euclidean_gcd(int(p["a"]), int(p["b"]))
    g2, x, y, ext = nt.extended_euclidean(int(p["a"]), int(p["b"]))
    return {"gcd": g, "steps": steps, "bezout": {"gcd": g2, "x": x, "y": y, "steps": ext}}


def diophantine(p):
    x0, y0, ok = NumberTheory().diophantine_solver(int(p["a"]), int(p["b"]), int(p["c"]))
    return {"x0": x0, "y0": y0, "exists": ok}


def primes(p):
    nt = NumberTheory()
    pr = nt.sieve_of_eratosthenes(int(p["limit"]))
    return {"primes": pr, "gaps": [pr[i + 1] - pr[i] for i in range(len(pr) - 1)],
            "factors": [list(f) for f in nt.prime_factorization(int(p.get("n", 840)))]}


def dna_length(p):
    a = BioNumberTheory().analyze_dna_length(int(p["length"]))
    return {**a, "factors": [list(f) for f in a["factors"]]}


def cicada(p):
    res = BioNumberTheory().simulate_cicada_lifecycle(int(p["years"]), [int(c) for c in p["predators"]])
    return [{"cycle": c, **v} for c, v in res.items()]


def genetic_sequences(p):
    return BioNumberTheory().analyze_genetic_sequences([int(v) for v in p["lengths"]])


def phyllotaxis(p):
    x, y = BioMathPatterns().generate_phyllotaxis(int(p["n"]), float(p["alpha"]))
    return {"x": _f(x), "y": _f(y)}


def gene_lengths(p):
    a = BioMathPatterns().analyze_gene_lengths([int(v) for v in p["lengths"]])
    return {**a, "golden_ratio_approximations": [list(t) for t in a["golden_ratio_approximations"]]}


def sequence_length(p):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    n = int(p["length"])
    an = MathematicalPatternAnalyzer()
    a = an.analyze_sequence_length(n)
    a["prime_analysis"]["factor_counts"] = [[k, v] for k, v in a["prime_analysis"]["factor_counts"].items()]
    fig, ax = plt.subplots()
    an.fibonacci_analyzer.plot_properties(n, ax)       # the property bars are computed inside the plot method
    a["properties"] = [bool(bar.get_height()) for bar in ax.patches]
    plt.close(fig)
    return a


def tree(p):
    segs = BioGrowthPatterns().generate_tree((0, 0), angle=float(p.get("angle", 90)), length=float(p.get("length", 1)),
                                             branching_angle=float(p["branching_angle"]), depth=int(p["depth"]),
                                             length_decay=float(p["length_decay"]))
    return [[float(s.x), float(s.y), float(e.x), float(e.y), s.depth] for s, e in segs]


def shell_spiral(p):
    x, y = BioGrowthPatterns().generate_shell_spiral(int(p.get("n_points", 1000)), float(p["growth_rate"]),
                                                     float(p["tightness"]))
    return {"x": _f(x), "y": _f(y)}


def population(p):
    r = BioGrowthPatterns().simulate_population_growth(float(p["initial_pop"]), float(p["growth_rate"]),
                                                       float(p["carrying_capacity"]), int(p["time_steps"]), p["model"])
    return _f(r["population"])


def advanced_tree(p):
    m = AdvancedTreeModel(p["species"])
    random.seed(int(p["seed"]))
    segs = m.generate_tree((0, 0), season=p["season"], light_direction=float(p["light_direction"]),
                           nutrient_level=float(p["nutrient_level"]), environmental_stress=float(p["stress"]))
    return [[float(s.x), float(s.y), float(e.x), float(e.y), s.depth, float(s.thickness), float(s.health),
             float(e.light_exposure), float(e.nutrient_level)] for s, e in segs]


def tree_stats(p):
    a = TreeDataAnalysis().analyze_branching_patterns(p["species"])
    return {k: {"mean": float(v["mean"]), "std": float(v["std"]), "ci": _f(v["ci"])} for k, v in a.items()}


def tree_compare(p):
    t = TreeDataAnalysis()
    np.random.seed(int(p["seed"]))
    model = t.generate_model_predictions(p["species"])
    np.random.seed(int(p["seed"]))
    comp = t.compare_with_model(p["species"])
    return {"model": {k: _f(v) for k, v in model.items()},
            "comparisons": {k: {kk: float(vv) for kk, vv in v.items()} for k, v in comp.items()}}


def shell3d(p):
    s = ShellGrowthAnalysis()
    params = s.SPECIES_PARAMETERS[p["species"]]
    if "growth_rate" in p:
        params = type(params)(**{**params.__dict__, "growth_rate": float(p["growth_rate"])})
    x, y, z = s.generate_shell_spiral(params, n_points=int(p.get("n_points", 1000)), n_whorls=float(p["n_whorls"]))
    return {"x": _f(x), "y": _f(y), "z": _f(z),
            "metrics": {k: float(v) for k, v in s.calculate_growth_metrics(params).items()}}


def shell_stats(p):
    s = ShellComparativeAnalysis()
    t = s.analyze_temperature_effects()
    out = {"temperature_growth_correlation": _f(t["temperature_growth_correlation"]),
           "temperature_size_correlation": _f(t["temperature_size_correlation"]),
           "mean_growth_rate": float(t["mean_growth_rate"]), "mean_temperature": float(t["mean_temperature"])}
    out["compare"] = {sp: _jsonable(s.compare_modern_fossil(sp)) for sp in s.SHELL_DATA}
    return out


def _jsonable(v):
    if isinstance(v, dict):
        return {k: _jsonable(x) for k, x in v.items()}
    return float(v) if isinstance(v, (float, np.floating)) else v


def data_tables():
    """Parameter tables and measurement data held in the scripts' class attributes (for /api/data)."""
    from dataclasses import asdict
    return {"tree_species": AdvancedTreeModel.SPECIES_PARAMS, "seasons": AdvancedTreeModel.SEASON_EFFECTS,
            "tree_data": TreeDataAnalysis.EXAMPLE_TREE_DATA,
            "shell_species": {k: asdict(v) for k, v in ShellGrowthAnalysis.SPECIES_PARAMETERS.items()},
            "shell_data": {sp: {per: [asdict(m) for m in ms] for per, ms in d.items()}
                           for sp, d in ShellComparativeAnalysis.SHELL_DATA.items()}}


REGISTRY = {f.__name__: f for f in (numerals, egyptian_multiply, babylonian_sqrt, gcd, diophantine, primes, dna_length,
                                    cicada, genetic_sequences, phyllotaxis, gene_lengths, sequence_length, tree,
                                    shell_spiral, population, advanced_tree, tree_stats, tree_compare, shell3d,
                                    shell_stats, sequence, ip3r)}


def run(name: str, params: dict):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return REGISTRY[name](params)
