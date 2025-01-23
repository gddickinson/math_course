import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
import math
from collections import Counter

class BioMathPatterns:
    """
    Comprehensive implementation of mathematical patterns in biology
    """
    def __init__(self):
        self.golden_ratio = (1 + math.sqrt(5)) / 2
        self.fibonacci_cache = {0: 0, 1: 1}
        
    def fibonacci(self, n: int) -> int:
        """Calculate nth Fibonacci number with caching"""
        if n in self.fibonacci_cache:
            return self.fibonacci_cache[n]
        
        self.fibonacci_cache[n] = self.fibonacci(n-1) + self.fibonacci(n-2)
        return self.fibonacci_cache[n]
    
    def generate_phyllotaxis(self, n_points: int, alpha: float = 137.5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate phyllotaxis pattern points
        alpha: angle between successive points (default golden angle ~137.5°)
        """
        # Convert angle to radians
        alpha_rad = alpha * np.pi / 180
        
        # Generate points
        r = np.sqrt(np.arange(n_points))  # Radius
        theta = alpha_rad * np.arange(n_points)  # Angle
        
        # Convert to Cartesian coordinates
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        return x, y
    
    def visualize_phyllotaxis(self, n_points: int = 500) -> None:
        """Create visualization of phyllotaxis pattern"""
        # Create figure with multiple patterns
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 15))
        fig.suptitle('Phyllotaxis Patterns in Nature', fontsize=16)
        
        # Standard golden angle pattern
        x, y = self.generate_phyllotaxis(n_points)
        ax1.scatter(x, y, c=range(n_points), cmap='viridis', alpha=0.6, s=10)
        ax1.set_title('Golden Angle (137.5°)')
        ax1.set_aspect('equal')
        
        # Fibonacci spiral overlay
        for i in range(5):
            radius = np.sqrt(self.fibonacci(i+7))
            theta = np.linspace(0, 2*np.pi*self.fibonacci(i)/self.fibonacci(i+1), 100)
            ax1.plot(radius*np.cos(theta), radius*np.sin(theta), 'r-', alpha=0.3)
        
        # Alternative angles
        angles = [137.3, 137.7, 130.0]
        axes = [ax2, ax3, ax4]
        for angle, ax in zip(angles, axes):
            x, y = self.generate_phyllotaxis(n_points, angle)
            ax.scatter(x, y, c=range(n_points), cmap='viridis', alpha=0.6, s=10)
            ax.set_title(f'Alternative Angle ({angle}°)')
            ax.set_aspect('equal')
        
        plt.tight_layout()
        plt.show()
    
    def analyze_gene_lengths(self, lengths: List[int]) -> Dict:
        """
        Analyze multiple gene lengths for mathematical patterns
        """
        analysis = {
            'lengths': lengths,
            'fibonacci_matches': [],
            'golden_ratio_approximations': [],
            'patterns': []
        }
        
        # Generate Fibonacci numbers up to max length
        max_length = max(lengths)
        fib_numbers = []
        i = 0
        while self.fibonacci(i) <= max_length:
            fib_numbers.append(self.fibonacci(i))
            i += 1
        
        # Analyze each length
        for length in lengths:
            # Check Fibonacci relationships
            if length in fib_numbers:
                analysis['fibonacci_matches'].append(length)
            
            # Check golden ratio approximations
            for i in range(len(lengths)):
                for j in range(i+1, len(lengths)):
                    ratio = lengths[j] / lengths[i]
                    if abs(ratio - self.golden_ratio) < 0.1:
                        analysis['golden_ratio_approximations'].append(
                            (lengths[i], lengths[j], ratio)
                        )
        
        return analysis
    
    def visualize_dna_spirals(self, sequence_length: int) -> None:
        """
        Visualize DNA sequence length as a spiral pattern
        """
        fig = plt.figure(figsize=(12, 6))
        
        # Create main spiral
        theta = np.linspace(0, 10*np.pi, sequence_length)
        r = np.linspace(0, 1, sequence_length)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        # Color points based on position in codon
        colors = np.array([i % 3 for i in range(sequence_length)])
        
        plt.scatter(x, y, c=colors, cmap='Set1', alpha=0.6, s=20)
        plt.title(f'DNA Sequence Spiral Pattern (length: {sequence_length})')
        plt.axis('equal')
        plt.grid(True, alpha=0.3)
        plt.show()
    
    def visualize_combined_patterns(self, gene_length: int) -> None:
        """
        Create combined visualization of various biological patterns
        """
        fig = plt.figure(figsize=(15, 5))
        
        # 1. Phyllotaxis subset
        ax1 = fig.add_subplot(131)
        x, y = self.generate_phyllotaxis(100)
        ax1.scatter(x, y, c=range(100), cmap='viridis', alpha=0.6, s=10)
        ax1.set_title('Phyllotaxis Pattern')
        ax1.set_aspect('equal')
        
        # 2. DNA spiral
        ax2 = fig.add_subplot(132)
        theta = np.linspace(0, 6*np.pi, gene_length)
        r = np.linspace(0, 1, gene_length)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        ax2.scatter(x, y, c=range(gene_length), cmap='coolwarm', alpha=0.6, s=10)
        ax2.set_title('DNA Spiral')
        ax2.set_aspect('equal')
        
        # 3. Fibonacci relationships
        ax3 = fig.add_subplot(133)
        fib_numbers = [self.fibonacci(i) for i in range(10)]
        ax3.plot(range(10), fib_numbers, 'bo-')
        ax3.set_title('Fibonacci Growth')
        ax3.grid(True)
        
        plt.tight_layout()
        plt.show()

def demonstrate_bio_patterns():
    """Show examples of mathematical patterns in biology"""
    bp = BioMathPatterns()
    
    # 1. Phyllotaxis patterns
    print("Generating phyllotaxis patterns...")
    bp.visualize_phyllotaxis()
    
    # 2. Gene length analysis
    print("\nAnalyzing gene lengths...")
    gene_lengths = [610, 987, 1597, 2584]  # Fibonacci-inspired lengths
    analysis = bp.analyze_gene_lengths(gene_lengths)
    print(f"Found Fibonacci matches: {analysis['fibonacci_matches']}")
    print("Golden ratio approximations:")
    for pair in analysis['golden_ratio_approximations']:
        print(f"{pair[0]}:{pair[1]} = {pair[2]:.3f}")
    
    # 3. DNA spiral visualization
    print("\nGenerating DNA spiral visualization...")
    bp.visualize_dna_spirals(612)  # Multiple of 3 for codons
    
    # 4. Combined patterns
    print("\nGenerating combined visualization...")
    bp.visualize_combined_patterns(300)

if __name__ == "__main__":
    demonstrate_bio_patterns()