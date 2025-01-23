import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
import math
from collections import Counter

class BioNumberTheory:
    """
    Implementation of number theory applications in biology
    """
    def __init__(self):
        self.prime_cache = {}
    
    def get_primes(self, n: int) -> List[int]:
        """Simple prime number generator"""
        if n in self.prime_cache:
            return self.prime_cache[n]
            
        sieve = [True] * (n + 1)
        sieve[0] = sieve[1] = False
        
        for i in range(2, int(math.sqrt(n)) + 1):
            if sieve[i]:
                for j in range(i * i, n + 1, i):
                    sieve[j] = False
                    
        primes = [i for i in range(n + 1) if sieve[i]]
        self.prime_cache[n] = primes
        return primes

    def analyze_dna_length(self, length: int) -> Dict:
        """
        Analyze DNA sequence length properties
        Returns prime factorization and relevant biological implications
        """
        def prime_factorize(n: int) -> List[Tuple[int, int]]:
            factors = []
            primes = self.get_primes(int(math.sqrt(n)) + 1)
            
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
        
        factors = prime_factorize(length)
        
        # Analyze biological significance
        analysis = {
            'length': length,
            'factors': factors,
            'is_multiple_3': length % 3 == 0,  # Important for codons
            'possible_nucleosome_units': length / 147 if length >= 147 else 0,  # 147 bp is nucleosome length
            'implications': []
        }
        
        # Add biological implications
        if length % 3 == 0:
            analysis['implications'].append("Length is divisible by 3 - suitable for protein coding")
        if length % 147 < 10:
            analysis['implications'].append("Length is close to nucleosome unit multiple")
        if len(factors) == 1 and factors[0][1] == 1:  # Prime length
            analysis['implications'].append("Prime length - potential evolutionary significance")
            
        return analysis

    def simulate_cicada_lifecycle(self, years: int, predator_cycles: List[int]) -> Dict:
        """
        Simulate cicada lifecycle interactions with predators
        Demonstrates why prime number cycles are advantageous
        """
        def calculate_encounters(cycle: int, predator_cycles: List[int], years: int) -> int:
            encounters = 0
            for predator_cycle in predator_cycles:
                encounters += years // math.lcm(cycle, predator_cycle)
            return encounters
        
        cycles = range(10, 21)  # Test cycles from 10 to 20 years
        results = {}
        
        for cycle in cycles:
            encounters = calculate_encounters(cycle, predator_cycles, years)
            results[cycle] = {
                'encounters': encounters,
                'is_prime': cycle in self.get_primes(20),
                'relative_fitness': 1 / (encounters + 1)  # Simple fitness model
            }
            
        return results

    def analyze_genetic_sequences(self, lengths: List[int]) -> Dict:
        """
        Analyze multiple genetic sequence lengths for patterns and relationships
        """
        def gcd_all(numbers: List[int]) -> int:
            """Calculate GCD of multiple numbers"""
            result = numbers[0]
            for i in range(1, len(numbers)):
                result = math.gcd(result, numbers[i])
            return result
        
        analysis = {
            'lengths': lengths,
            'gcd': gcd_all(lengths),
            'lcm': math.lcm(*lengths),
            'common_factors': [],
            'patterns': []
        }
        
        # Find common factors
        min_length = min(lengths)
        for i in range(1, min_length + 1):
            if all(length % i == 0 for length in lengths):
                analysis['common_factors'].append(i)
        
        # Analyze patterns
        if 3 in analysis['common_factors']:
            analysis['patterns'].append("All sequences are potential protein coding (divisible by 3)")
        if analysis['gcd'] > 1:
            analysis['patterns'].append(f"Common unit of {analysis['gcd']} bases found")
            
        return analysis

    def visualize_cicada_fitness(self, results: Dict) -> None:
        """
        Create visualization of cicada lifecycle fitness
        """
        cycles = list(results.keys())
        fitness = [results[cycle]['relative_fitness'] for cycle in cycles]
        is_prime = [results[cycle]['is_prime'] for cycle in cycles]
        
        plt.figure(figsize=(12, 6))
        
        # Plot bars with different colors for prime/non-prime
        for i, (cycle, fit, prime) in enumerate(zip(cycles, fitness, is_prime)):
            color = 'red' if prime else 'blue'
            plt.bar(cycle, fit, color=color, alpha=0.6)
        
        plt.title('Relative Fitness of Different Cicada Lifecycle Lengths')
        plt.xlabel('Cycle Length (Years)')
        plt.ylabel('Relative Fitness')
        
        # Add legend
        plt.bar(0, 0, color='red', alpha=0.6, label='Prime Cycles')
        plt.bar(0, 0, color='blue', alpha=0.6, label='Non-Prime Cycles')
        plt.legend()
        
        plt.grid(True, alpha=0.3)
        plt.show()

    def visualize_dna_factorization(self, length: int) -> None:
        """
        Create visualization of DNA length factorization
        """
        analysis = self.analyze_dna_length(length)
        factors = analysis['factors']
        
        plt.figure(figsize=(12, 6))
        
        # Create pie chart of prime factors
        labels = [f"Prime: {p}" for p, e in factors]
        sizes = [e for p, e in factors]
        
        plt.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.title(f'Prime Factorization of DNA Sequence Length: {length}')
        
        plt.axis('equal')
        plt.show()

def demonstrate_bio_number_theory():
    """Show examples of number theory in biology"""
    bnt = BioNumberTheory()
    
    # Example 1: DNA sequence analysis
    print("Analyzing DNA sequence length: 3456 bp")
    dna_analysis = bnt.analyze_dna_length(3456)
    print("Factorization:", dna_analysis['factors'])
    print("Biological implications:", dna_analysis['implications'])
    
    # Example 2: Cicada lifecycle analysis
    print("\nAnalyzing cicada lifecycles")
    predator_cycles = [2, 3, 4, 6, 8, 9, 10]  # Example predator cycles
    cicada_results = bnt.simulate_cicada_lifecycle(100, predator_cycles)
    
    # Example 3: Genetic sequence pattern analysis
    print("\nAnalyzing multiple genetic sequences")
    sequence_lengths = [612, 918, 1224]  # Example sequence lengths
    pattern_analysis = bnt.analyze_genetic_sequences(sequence_lengths)
    print("Common factors:", pattern_analysis['common_factors'])
    print("Patterns found:", pattern_analysis['patterns'])
    
    # Visualizations
    print("\nGenerating visualizations...")
    bnt.visualize_cicada_fitness(cicada_results)
    bnt.visualize_dna_factorization(3456)

if __name__ == "__main__":
    demonstrate_bio_number_theory()