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


if __name__ == "__main__":
    unittest.main()
