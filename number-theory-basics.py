import math
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple

class NumberTheory:
    """
    Implementation of fundamental number theory concepts with historical context
    """
    def __init__(self):
        self.sieve_cache = {}  # Cache for sieve of Eratosthenes results
    
    def euclidean_gcd(self, a: int, b: int) -> Tuple[int, List[dict]]:
        """
        Implement Euclidean algorithm for GCD (circa 300 BCE)
        Returns GCD and steps of calculation
        """
        steps = []
        while b:
            steps.append({
                'a': a,
                'b': b,
                'quotient': a // b,
                'remainder': a % b
            })
            a, b = b, a % b
        return a, steps

    def extended_euclidean(self, a: int, b: int) -> Tuple[int, int, int, List[dict]]:
        """
        Extended Euclidean algorithm to find Bézout's identity
        ax + by = gcd(a,b)
        """
        steps = []
        if a == 0:
            return b, 0, 1, steps
            
        old_r, r = a, b
        old_s, s = 1, 0
        old_t, t = 0, 1
        
        while r:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t
            
            steps.append({
                'quotient': quotient,
                'remainder': r,
                'x': s,
                'y': t
            })
            
        return old_r, old_s, old_t, steps

    def sieve_of_eratosthenes(self, n: int) -> List[int]:
        """
        Implement the Sieve of Eratosthenes (circa 240 BCE)
        One of the earliest known systematic methods for finding prime numbers
        """
        if n in self.sieve_cache:
            return self.sieve_cache[n]
            
        primes = [True] * (n + 1)
        primes[0] = primes[1] = False
        
        for i in range(2, int(math.sqrt(n)) + 1):
            if primes[i]:
                for j in range(i * i, n + 1, i):
                    primes[j] = False
                    
        result = [i for i in range(n + 1) if primes[i]]
        self.sieve_cache[n] = result
        return result

    def prime_factorization(self, n: int) -> List[Tuple[int, int]]:
        """
        Find prime factorization of a number
        Returns list of (prime, exponent) tuples
        """
        if n < 2:
            return []
            
        factors = []
        primes = self.sieve_of_eratosthenes(int(math.sqrt(n)) + 1)
        
        for prime in primes:
            if prime * prime > n:
                break
                
            if n % prime == 0:
                exponent = 0
                while n % prime == 0:
                    exponent += 1
                    n //= prime
                factors.append((prime, exponent))
                
        if n > 1:
            factors.append((n, 1))
            
        return factors

    def visualize_prime_gaps(self, limit: int) -> None:
        """
        Visualize the gaps between consecutive prime numbers
        """
        primes = self.sieve_of_eratosthenes(limit)
        gaps = [primes[i+1] - primes[i] for i in range(len(primes)-1)]
        
        plt.figure(figsize=(12, 6))
        plt.plot(primes[:-1], gaps, 'b.', alpha=0.5)
        plt.title(f'Prime Gaps up to {limit}')
        plt.xlabel('Prime Number')
        plt.ylabel('Gap to Next Prime')
        plt.grid(True)
        plt.show()

    def diophantine_solver(self, a: int, b: int, c: int) -> Tuple[int, int, bool]:
        """
        Solve linear Diophantine equation: ax + by = c
        Returns particular solution (x0, y0) and whether solution exists
        """
        gcd, x, y, _ = self.extended_euclidean(abs(a), abs(b))
        
        if c % gcd != 0:
            return 0, 0, False
            
        x0 = x * (c // gcd)
        y0 = y * (c // gcd)
        
        if a < 0: x0 = -x0
        if b < 0: y0 = -y0
        
        return x0, y0, True

    def visualize_factorization_tree(self, n: int) -> None:
        """
        Create a visualization of the prime factorization as a tree
        """
        def plot_node(x, y, value, ax):
            circle = plt.Circle((x, y), 0.2, fill=False)
            ax.add_patch(circle)
            ax.text(x, y, str(value), ha='center', va='center')
            
        def plot_edge(x1, y1, x2, y2, ax):
            ax.plot([x1, x2], [y1, y2], 'k-')
            
        factors = self.prime_factorization(n)
        if not factors:
            return
            
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.axis('off')
        
        # Plot root
        plot_node(0, 1.5, n, ax)
        
        # Plot prime factors
        x_positions = np.linspace(-1.5, 1.5, len(factors))
        for i, (prime, exp) in enumerate(factors):
            x = x_positions[i]
            plot_node(x, 0, f"{prime}^{exp}", ax)
            plot_edge(0, 1.3, x, 0.2, ax)
            
        plt.title(f'Prime Factorization Tree of {n}')
        plt.show()

def demonstrate_number_theory():
    """Show examples of number theory concepts"""
    nt = NumberTheory()
    
    # Example 1: GCD calculation
    print("Calculating GCD of 48 and 18:")
    gcd, steps = nt.euclidean_gcd(48, 18)
    print(f"Steps in Euclidean algorithm:")
    for step in steps:
        print(f"a={step['a']}, b={step['b']}, q={step['quotient']}, r={step['remainder']}")
    print(f"GCD = {gcd}\n")
    
    # Example 2: Prime factorization
    n = 840
    print(f"Prime factorization of {n}:")
    factors = nt.prime_factorization(n)
    factorization = " × ".join([f"{p}^{e}" for p, e in factors])
    print(f"{n} = {factorization}\n")
    
    # Example 3: Diophantine equation
    a, b, c = 15, 21, 12
    x0, y0, exists = nt.diophantine_solver(a, b, c)
    if exists:
        print(f"Solution to {a}x + {b}y = {c}:")
        print(f"x = {x0}, y = {y0}\n")
    
    # Example 4: Visualize prime gaps and factorization
    print("Generating visualizations...")
    nt.visualize_prime_gaps(1000)
    nt.visualize_factorization_tree(840)

if __name__ == "__main__":
    demonstrate_number_theory()