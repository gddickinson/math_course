"""Smoke tests for math_course modules."""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class TestEgyptianNumber(unittest.TestCase):
    """Test Egyptian number system implementation."""

    def test_to_egyptian(self):
        from ancient_numbers import EgyptianNumber
        eg = EgyptianNumber(1234)
        self.assertEqual(eg.number, 1234)
        self.assertIsNotNone(eg.egyptian)

    def test_zero_raises(self):
        from ancient_numbers import EgyptianNumber
        with self.assertRaises(ValueError):
            EgyptianNumber(0)


class TestBabylonianNumber(unittest.TestCase):
    """Test Babylonian sexagesimal number system."""

    def test_to_sexagesimal(self):
        from ancient_numbers import BabylonianNumber
        # 3661 = 1*3600 + 1*60 + 1 -> [1, 1, 1]
        bn = BabylonianNumber(3661)
        self.assertEqual(bn.sexagesimal, [1, 1, 1])

    def test_format(self):
        from ancient_numbers import BabylonianNumber
        bn = BabylonianNumber(61)
        formatted = bn.format_sexagesimal()
        self.assertIsInstance(formatted, str)


class TestEgyptianMultiplication(unittest.TestCase):
    """Test Egyptian multiplication algorithm."""

    def test_basic_multiplication(self):
        from ancient_calculations import EgyptianMultiplication
        em = EgyptianMultiplication(13, 17)
        result = em.multiply()
        self.assertEqual(result, 13 * 17)

    def test_power_of_two(self):
        from ancient_calculations import EgyptianMultiplication
        em = EgyptianMultiplication(8, 16)
        result = em.multiply()
        self.assertEqual(result, 128)


class TestBabylonianSquareRoot(unittest.TestCase):
    """Test Babylonian square root method."""

    def test_sqrt_of_4(self):
        from ancient_calculations import BabylonianSquareRoot
        bsr = BabylonianSquareRoot(4, iterations=10)
        result = bsr.calculate()
        self.assertAlmostEqual(result, 2.0, places=6)

    def test_sqrt_of_9(self):
        from ancient_calculations import BabylonianSquareRoot
        bsr = BabylonianSquareRoot(9, iterations=10)
        result = bsr.calculate()
        self.assertAlmostEqual(result, 3.0, places=6)

    def test_sqrt_of_2(self):
        import math
        from ancient_calculations import BabylonianSquareRoot
        bsr = BabylonianSquareRoot(2, iterations=20)
        result = bsr.calculate()
        self.assertAlmostEqual(result, math.sqrt(2), places=10)


class TestNumberTheory(unittest.TestCase):
    """Test number theory functions."""

    def test_euclidean_gcd(self):
        from number_theory_basics import NumberTheory
        nt = NumberTheory()
        gcd, steps = nt.euclidean_gcd(48, 18)
        self.assertEqual(gcd, 6)

    def test_sieve_of_eratosthenes(self):
        from number_theory_basics import NumberTheory
        nt = NumberTheory()
        primes = nt.sieve_of_eratosthenes(30)
        self.assertEqual(primes, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])

    def test_prime_factorization(self):
        from number_theory_basics import NumberTheory
        nt = NumberTheory()
        factors = nt.prime_factorization(60)
        # 60 = 2^2 * 3 * 5
        self.assertIn((2, 2), factors)
        self.assertIn((3, 1), factors)
        self.assertIn((5, 1), factors)


class TestBioMathPatterns(unittest.TestCase):
    """Test biological math pattern implementations."""

    def test_fibonacci(self):
        from bio_math_patterns import BioMathPatterns
        bmp = BioMathPatterns()
        self.assertEqual(bmp.fibonacci(0), 0)
        self.assertEqual(bmp.fibonacci(1), 1)
        self.assertEqual(bmp.fibonacci(10), 55)

    def test_golden_ratio(self):
        import math
        from bio_math_patterns import BioMathPatterns
        bmp = BioMathPatterns()
        expected = (1 + math.sqrt(5)) / 2
        self.assertAlmostEqual(bmp.golden_ratio, expected)


class TestRomanNumeral(unittest.TestCase):
    """Test Roman numeral conversion."""

    def test_basic_conversion(self):
        from world_numbers import RomanNumeral
        rn = RomanNumeral(2024)
        self.assertIsNotNone(str(rn))

    def test_small_numbers(self):
        from world_numbers import RomanNumeral
        rn = RomanNumeral(4)
        self.assertEqual(rn.roman, "IV")


if __name__ == "__main__":
    unittest.main()
