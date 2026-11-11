"""Regression tests for bugs fixed in the course scripts (one class per fix).

Run: python -m pytest test_regressions.py -v
"""
import importlib.util
import io
import os
import sys
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
HAS_BIO = importlib.util.find_spec("Bio") is not None


class TestEgyptianMultiplicationSteps(unittest.TestCase):
    """show_work() printed an empty table unless multiply() had been called first."""

    def test_show_work_prints_steps(self):
        from ancient_calculations import EgyptianMultiplication
        buf = io.StringIO()
        with redirect_stdout(buf):
            EgyptianMultiplication(14, 12).show_work()
        rows = [ln for ln in buf.getvalue().splitlines() if ln.strip().startswith(("12", "6", "3", "1 "))]
        self.assertEqual(len(rows), 4, buf.getvalue())

    def test_repeated_multiply_does_not_duplicate_steps(self):
        from ancient_calculations import EgyptianMultiplication
        em = EgyptianMultiplication(14, 12)
        em.multiply()
        self.assertEqual(em.multiply(), 168)
        self.assertEqual(len(em.steps), 4)

    def test_repeated_sqrt_does_not_duplicate_steps(self):
        from ancient_calculations import BabylonianSquareRoot
        b = BabylonianSquareRoot(2)
        b.calculate()
        n = len(b.steps)
        b.calculate()
        self.assertEqual(len(b.steps), n)

    def test_sqrt_of_zero(self):
        from ancient_calculations import BabylonianSquareRoot
        self.assertEqual(BabylonianSquareRoot(0).calculate(), 0.0)


class TestNumeralEdgeCases(unittest.TestCase):
    """Chinese numerals gained a trailing 零 for round numbers; 100000+ raised KeyError; Babylonian 0 was blank."""

    def test_chinese_round_numbers(self):
        from world_numbers import ChineseNumeral
        self.assertEqual(ChineseNumeral(20).chinese, "二十")
        self.assertEqual(ChineseNumeral(100).chinese, "一百")
        self.assertEqual(ChineseNumeral(2020).chinese, "二千零二十")
        self.assertEqual(ChineseNumeral(10000).chinese, "一万")
        self.assertEqual(ChineseNumeral(1001).chinese, "一千零一")
        self.assertEqual(ChineseNumeral(2024).chinese, "二千零二十四")

    def test_chinese_out_of_range_is_value_error(self):
        from world_numbers import ChineseNumeral
        with self.assertRaises(ValueError):
            ChineseNumeral(100000)

    def test_babylonian_zero(self):
        from ancient_numbers import BabylonianNumber
        self.assertEqual(BabylonianNumber(0).sexagesimal, [0])
        self.assertEqual(BabylonianNumber(0).format_sexagesimal(), "0")


class TestGoldenRatioPairs(unittest.TestCase):
    """analyze_gene_lengths listed every golden-ratio pair once per input length."""

    def test_pairs_listed_once(self):
        from bio_math_patterns import BioMathPatterns
        a = BioMathPatterns().analyze_gene_lengths([610, 987, 1597, 2584])
        pairs = [(p[0], p[1]) for p in a["golden_ratio_approximations"]]
        self.assertEqual(pairs, [(610, 987), (987, 1597), (1597, 2584)])


class TestPatternAnalyzerEdgeCases(unittest.TestCase):
    """'Multiple of Fib' was always True (every n is a multiple of 1); n=1 crashed analyze_prime_factors."""

    def test_multiple_of_fib_ignores_one(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from bio_math_enhanced import FibonacciAnalyzer
        fa = FibonacciAnalyzer()
        fig, ax = plt.subplots()
        fa.plot_properties(7, ax)   # 7 is not a multiple of any Fibonacci number > 1
        heights = [p.get_height() for p in ax.patches]
        plt.close(fig)
        self.assertEqual(heights[2], 0)

    def test_prime_factors_of_one(self):
        from bio_math_enhanced import MathematicalPatternAnalyzer
        r = MathematicalPatternAnalyzer().analyze_prime_factors(1)
        self.assertEqual(r["prime_factors"], [])
        self.assertIsNone(r["largest_prime_factor"])


@unittest.skipUnless(HAS_BIO, "biopython not installed")
class TestIP3RAnalyzer(unittest.TestCase):
    """analyze_domains overwrote every result with the last region's slice (NameError on short sequences);
    the PROSITE-style calcium motifs ('D-[DNS]-...') were used as regexes and could never match."""

    def test_domains_short_sequence(self):
        from ip3r_analysis import IP3RAnalyzer
        r = IP3RAnalyzer("test@example.org").analyze_domains("ATG" * 100)   # shorter than every domain
        self.assertEqual(r, {})

    def test_domains_have_own_lengths(self):
        from ip3r_analysis import IP3RAnalyzer
        r = IP3RAnalyzer("test@example.org").analyze_domains("ATGGCC" * 500)  # 3000 nt
        self.assertEqual(r["IP3_binding"]["length"], 604 - 224)
        self.assertEqual(r["suppressor"]["length"], 1654 - 1574)
        self.assertEqual(r["regulatory"]["total_length"], (1207 - 918) + (1654 - 1574))
        self.assertEqual(r["regulatory"]["length"], r["regulatory"]["total_length"])

    def test_calcium_motif_matches(self):
        from ip3r_analysis import IP3RAnalyzer
        # GAT GAC AAC TCC -> D D N S, an EF-hand-like D-[DNS]-[DNS]-[DNS] match
        sites = IP3RAnalyzer("test@example.org").find_calcium_binding_sites("GATGACAACTCC")
        self.assertTrue(any(s["sequence"] == "DDNS" for s in sites))


@unittest.skipUnless(HAS_BIO, "biopython not installed")
class TestSequenceCodons(unittest.TestCase):
    """_analyze_codons tested 'mRNA' in a lower-cased string, so mRNA records were always transcribed."""

    def test_mrna_used_as_is(self):
        from bio_sequence_analysis import NCBISequenceAnalyzer
        a = NCBISequenceAnalyzer("test@example.org")
        a.sequence = "ATGATGTTT"
        a.gene_info = {"name": "Homo sapiens ITPR1, mRNA"}
        self.assertEqual(dict(a._analyze_codons()["most_common"]), {"ATG": 2, "TTT": 1})


class TestTreeModelSpecies(unittest.TestCase):
    """compare_species() left the model switched to the last species (birch)."""

    def test_species_restored(self):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from advanced_tree_patterns import AdvancedTreeModel
        m = AdvancedTreeModel("oak")
        m.compare_species()
        plt.close("all")
        self.assertEqual(m.species, "oak")
        self.assertEqual(m.params, AdvancedTreeModel.SPECIES_PARAMS["oak"])


if __name__ == "__main__":
    unittest.main()
