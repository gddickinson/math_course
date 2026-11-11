import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
import math
from collections import Counter

import math
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
from collections import Counter

class FibonacciAnalyzer:
    """Enhanced Fibonacci analysis for biological sequences"""

    def __init__(self):
        self.fib_cache = {0: 0, 1: 1}
        self.fib_list = [0, 1]  # Initialize with first two Fibonacci numbers
        self.golden_ratio = (1 + math.sqrt(5)) / 2
        self._generate_fibonacci_numbers(1000)  # Pre-generate a good set of numbers

    def _generate_fibonacci_numbers(self, limit: int) -> None:
        """Generate Fibonacci numbers up to limit"""
        while self.fib_list[-1] <= limit:
            self.fib_list.append(self.fib_list[-1] + self.fib_list[-2])

    def find_nearest_fibonacci(self, n: int) -> dict:
        """Find nearest Fibonacci numbers and related metrics"""
        # Ensure we have enough Fibonacci numbers
        while self.fib_list[-1] < n:
            self._generate_fibonacci_numbers(n * 2)

        # Find nearest numbers
        lower = max(x for x in self.fib_list if x <= n)
        upper = min(x for x in self.fib_list if x >= n)

        lower_idx = self.fib_list.index(lower)
        upper_idx = self.fib_list.index(upper)

        return {
            'nearest_lower': lower,
            'nearest_upper': upper,
            'lower_index': lower_idx,
            'upper_index': upper_idx,
            'distance_to_lower': n - lower,
            'distance_to_upper': upper - n
        }

    def plot_fibonacci_sequence(self, n: int, ax) -> None:
        """Plot Fibonacci sequence around number n"""
        analysis = self.find_nearest_fibonacci(n)

        # Get relevant range of Fibonacci numbers
        start_idx = max(2, analysis['lower_index'] - 2)
        end_idx = min(len(self.fib_list), analysis['upper_index'] + 3)

        relevant_fibs = self.fib_list[start_idx:end_idx]
        indices = list(range(start_idx, end_idx))

        ax.plot(indices, relevant_fibs, 'bo-', label='Fibonacci numbers')
        ax.axhline(y=n, color='r', linestyle='--', label='Target number')
        ax.set_title('Position in Fibonacci Sequence')
        ax.set_xlabel('Index')
        ax.set_ylabel('Value')
        ax.legend()

    def plot_distances(self, n: int, ax) -> None:
        """Plot distances to nearby Fibonacci numbers"""
        analysis = self.find_nearest_fibonacci(n)

        start_idx = max(2, analysis['lower_index'] - 2)
        end_idx = min(len(self.fib_list), analysis['upper_index'] + 3)

        relevant_fibs = self.fib_list[start_idx:end_idx]
        indices = list(range(start_idx, end_idx))
        distances = [abs(n - fib) for fib in relevant_fibs]

        ax.bar(indices, distances)
        ax.set_title('Distance to Nearby Fibonacci Numbers')
        ax.set_xlabel('Fibonacci Index')
        ax.set_ylabel('Distance')

    def plot_properties(self, n: int, ax) -> None:
        """Plot various Fibonacci-related properties"""
        analysis = self.find_nearest_fibonacci(n)

        properties = {
            'Is Fibonacci': n in self.fib_list,
            'Near Fibonacci': min(analysis['distance_to_lower'],
                                analysis['distance_to_upper']) < n * 0.1,
            'Multiple of Fib': any(n % fib == 0
                                 for fib in self.fib_list[2:analysis['upper_index']+1]
                                 if fib > 1),  # every n is a multiple of 1
            'Between Consecutive': analysis['nearest_lower'] != analysis['nearest_upper']
        }

        ax.bar(range(len(properties)),
               [1 if v else 0 for v in properties.values()],
               tick_label=list(properties.keys()))
        ax.set_xticklabels(list(properties.keys()), rotation=45, ha='right')
        ax.set_title('Fibonacci-related Properties')

    def visualize_fibonacci_analysis(self, n: int) -> None:
        """Create comprehensive visualization of Fibonacci relationships"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

        # Plot 1: Sequence position
        self.plot_fibonacci_sequence(n, ax1)

        # Plot 2: Distances
        self.plot_distances(n, ax2)

        # Plot 3: Properties
        self.plot_properties(n, ax3)

        # Plot 4: Summary
        analysis = self.find_nearest_fibonacci(n)
        summary_text = (
            f"Analysis Summary:\n\n"
            f"Target number: {n}\n"
            f"Nearest lower Fibonacci: {analysis['nearest_lower']}\n"
            f"Nearest upper Fibonacci: {analysis['nearest_upper']}\n"
            f"Distance to lower: {analysis['distance_to_lower']}\n"
            f"Distance to upper: {analysis['distance_to_upper']}"
        )
        ax4.text(0.1, 0.5, summary_text,
                verticalalignment='center',
                horizontalalignment='left',
                fontsize=10)
        ax4.axis('off')

        plt.tight_layout()
        plt.show()

class MathematicalPatternAnalyzer:
    """Enhanced mathematical pattern analysis for biological sequences"""

    def __init__(self):
        self.fibonacci_analyzer = FibonacciAnalyzer()

    def analyze_sequence_length(self, length: int) -> dict:
        """Comprehensive mathematical analysis of sequence length"""
        return {
            'fibonacci_analysis': self.fibonacci_analyzer.find_nearest_fibonacci(length),
            'prime_analysis': self.analyze_prime_factors(length),
            'divisibility_analysis': self.analyze_divisibility(length),
            'symmetry_analysis': self.analyze_symmetry(length)
        }

    def analyze_prime_factors(self, n: int) -> dict:
        """Detailed prime factorization analysis"""
        def get_prime_factors(n):
            factors = []
            d = 2
            while n > 1:
                while n % d == 0:
                    factors.append(d)
                    n //= d
                d += 1
                if d * d > n:
                    if n > 1:
                        factors.append(n)
                    break
            return factors

        factors = get_prime_factors(n)
        factor_counts = Counter(factors)

        return {
            'prime_factors': factors,
            'unique_factors': list(factor_counts.keys()),
            'factor_counts': dict(factor_counts),
            'is_prime': len(factors) == 1,
            'largest_prime_factor': max(factors) if factors else None,  # n = 1 has none
            'smallest_prime_factor': min(factors) if factors else None
        }

    def analyze_divisibility(self, n: int) -> dict:
        """Analyze various divisibility properties"""
        divisors = [i for i in range(1, n + 1) if n % i == 0]

        return {
            'divisors': divisors,
            'divisor_count': len(divisors),
            'is_even': n % 2 == 0,
            'is_multiple_of_3': n % 3 == 0,  # Important for codons
            'perfect_square': int(n ** 0.5) ** 2 == n,
            'perfect_cube': round(n ** (1/3)) ** 3 == n
        }

    def analyze_symmetry(self, n: int) -> dict:
        """Analyze symmetrical properties of the number"""
        binary = bin(n)[2:]

        return {
            'binary_representation': binary,
            'binary_palindrome': binary == binary[::-1],
            'decimal_palindrome': str(n) == str(n)[::-1],
            'digit_sum': sum(int(d) for d in str(n)),
            'digit_product': math.prod(int(d) for d in str(n))
        }

    def visualize_patterns(self, length: int) -> None:
        """Create comprehensive visualization of mathematical patterns"""
        plt.figure(figsize=(15, 10))

        # 1. Prime factor distribution
        plt.subplot(2, 2, 1)
        prime_analysis = self.analyze_prime_factors(length)
        factor_counts = prime_analysis['factor_counts']
        plt.bar(list(map(str, factor_counts.keys())),
               list(factor_counts.values()))
        plt.title('Prime Factor Distribution')
        plt.xlabel('Prime Factors')
        plt.ylabel('Count')

        # 2. Divisor visualization
        plt.subplot(2, 2, 2)
        divisors = self.analyze_divisibility(length)['divisors']
        plt.hist(divisors, bins=min(20, len(divisors)))
        plt.title('Divisor Distribution')
        plt.xlabel('Divisors')
        plt.ylabel('Frequency')

        # 3. Number properties
        plt.subplot(2, 2, 3)
        properties = {
            'Even': length % 2 == 0,
            'Multiple of 3': length % 3 == 0,
            'Perfect Square': int(length ** 0.5) ** 2 == length,
            'Palindrome': str(length) == str(length)[::-1]
        }
        plt.bar(range(len(properties)),
               [1 if v else 0 for v in properties.values()])
        plt.xticks(range(len(properties)), list(properties.keys()),
                  rotation=45, ha='right')
        plt.title('Number Properties')

        # 4. Summary
        plt.subplot(2, 2, 4)
        summary_text = (
            f"Analysis Summary:\n\n"
            f"Number: {length}\n"
            f"Prime factors: {len(prime_analysis['prime_factors'])}\n"
            f"Divisors: {len(divisors)}\n"
            f"Largest prime factor: {prime_analysis['largest_prime_factor']}\n"
            f"Binary length: {len(bin(length))-2}"
        )
        plt.text(0.1, 0.5, summary_text,
                verticalalignment='center',
                horizontalalignment='left',
                fontsize=10)
        plt.axis('off')

        plt.tight_layout()
        plt.show()
