import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict
import math
from collections import Counter
from Bio import Entrez, SeqIO
from Bio.Seq import Seq
import io
import re

class NCBISequenceAnalyzer:
    """
    Retrieve and analyze sequences from NCBI
    """
    def __init__(self, email: str):
        """Initialize with user email (required by NCBI)"""
        Entrez.email = email
        self.sequence = None
        self.gene_info = {}

    def fetch_sequence(self, gene_id: str, database: str = "nucleotide") -> str:
        """
        Fetch sequence from NCBI using gene ID
        For IP3R1: "NM_001099952.2" (human ITPR1 mRNA)
        """
        try:
            # Fetch sequence
            handle = Entrez.efetch(db=database, id=gene_id, rettype="gb", retmode="text")
            record = SeqIO.read(handle, "genbank")
            handle.close()

            # Store sequence and info
            self.sequence = str(record.seq)
            self.gene_info = {
                'id': gene_id,
                'length': len(self.sequence),
                'name': record.description,
                'features': record.features
            }

            return self.sequence

        except Exception as e:
            print(f"Error fetching sequence: {e}")
            return None

    def analyze_sequence(self) -> Dict:
        """
        Comprehensive sequence analysis
        """
        if not self.sequence:
            raise ValueError("No sequence loaded. Please fetch sequence first.")

        analysis = {
            'length': len(self.sequence),
            'gc_content': self._calculate_gc_content(),
            'codon_analysis': self._analyze_codons(),
            'repeats': self._find_repeats(),
            'mathematical_patterns': self._find_mathematical_patterns()
        }

        return analysis

    def _calculate_gc_content(self) -> float:
        """Calculate GC content percentage"""
        gc_count = self.sequence.count('G') + self.sequence.count('C')
        return (gc_count / len(self.sequence)) * 100

    def _analyze_codons(self) -> Dict:
        """Analyze codon usage and patterns"""
        # Convert to coding sequence if not already
        if 'mrna' in self.gene_info['name'].lower():
            coding_seq = self.sequence
        else:
            coding_seq = str(Seq(self.sequence).transcribe())

        codons = [coding_seq[i:i+3] for i in range(0, len(coding_seq)-2, 3)]
        codon_usage = Counter(codons)

        return {
            'total_codons': len(codons),
            'unique_codons': len(codon_usage),
            'most_common': codon_usage.most_common(5)
        }

    def _find_repeats(self) -> Dict:
        """Find sequence repeats and patterns"""
        # Look for direct repeats (4+ bases)
        repeats = {}
        for length in range(4, 11):
            repeat_dict = {}
            for i in range(len(self.sequence) - length + 1):
                seq = self.sequence[i:i+length]
                if seq in repeat_dict:
                    repeat_dict[seq] += 1
                else:
                    repeat_dict[seq] = 1
            # Filter for sequences that appear multiple times
            repeats[length] = {seq: count for seq, count in repeat_dict.items()
                             if count > 1}

        return repeats

    def _find_mathematical_patterns(self) -> Dict:
        """Find mathematical patterns in sequence"""
        length = len(self.sequence)

        # Prime factorization
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

        # Fibonacci check
        def is_fibonacci(n):
            # Generate Fibonacci numbers up to n
            a, b = 0, 1
            fib_numbers = {0, 1}
            while b <= n:
                a, b = b, a + b
                fib_numbers.add(b)
            return n in fib_numbers

        return {
            'prime_factors': get_prime_factors(length),
            'is_fibonacci': is_fibonacci(length),
            'divisible_by_3': length % 3 == 0,
            'golden_ratio_approx': length / (length//2) if length > 1 else None
        }

    def visualize_sequence_patterns(self) -> None:
        """
        Create comprehensive sequence visualization
        """
        if not self.sequence:
            raise ValueError("No sequence loaded")

        fig = plt.figure(figsize=(20, 10))

        # 1. Nucleotide distribution plot
        ax1 = plt.subplot(231)
        nucleotides = ['A', 'T', 'G', 'C']
        counts = [self.sequence.count(n) for n in nucleotides]
        ax1.bar(nucleotides, counts)
        ax1.set_title('Nucleotide Distribution')

        # 2. GC content along sequence
        ax2 = plt.subplot(232)
        window_size = 100
        gc_content = []
        for i in range(0, len(self.sequence) - window_size, window_size):
            window = self.sequence[i:i+window_size]
            gc = (window.count('G') + window.count('C')) / window_size
            gc_content.append(gc)
        ax2.plot(range(len(gc_content)), gc_content)
        ax2.set_title('GC Content Distribution')

        # 3. Sequence spiral
        ax3 = plt.subplot(233)
        turns = int(len(self.sequence) / 100)  # One turn per 100 bases
        theta = np.linspace(0, turns*2*np.pi, len(self.sequence))
        r = np.linspace(0, 1, len(self.sequence))
        colors = [{'A': 0, 'T': 1, 'G': 2, 'C': 3}[n] for n in self.sequence]
        ax3.scatter(r*np.cos(theta), r*np.sin(theta), c=colors,
                   cmap='Set2', s=1, alpha=0.6)
        ax3.set_title('Sequence Spiral')
        ax3.set_aspect('equal')

        # 4. Codon position analysis
        ax4 = plt.subplot(234)
        codon_pos = np.array(range(len(self.sequence))) % 3
        ax4.hist(codon_pos, bins=3, alpha=0.7)
        ax4.set_title('Codon Position Distribution')

        # 5. Repeat pattern visualization
        ax5 = plt.subplot(235)
        repeat_lengths = list(self._find_repeats().keys())
        repeat_counts = [len(repeats) for repeats in self._find_repeats().values()]
        ax5.bar(repeat_lengths, repeat_counts)
        ax5.set_title('Repeat Pattern Distribution')

        plt.tight_layout()
        plt.show()

def analyze_ip3r():
    """Analyze IP3 receptor sequence"""
    # Initialize analyzer
    analyzer = NCBISequenceAnalyzer("george.dickinson@gmail.com")  # Replace with your email

    # Fetch IP3R1 sequence (human)
    sequence = analyzer.fetch_sequence("NM_001099952.2")

    if sequence:
        # Perform analysis
        print("Analyzing IP3R1 sequence...")
        analysis = analyzer.analyze_sequence()

        # Print results
        print("\nSequence Analysis Results:")
        print(f"Length: {analysis['length']} nucleotides")
        print(f"GC Content: {analysis['gc_content']:.2f}%")
        print("\nCodon Analysis:")
        print(f"Total codons: {analysis['codon_analysis']['total_codons']}")
        print(f"Most common codons: {analysis['codon_analysis']['most_common']}")

        print("\nMathematical Patterns:")
        print(f"Prime factors: {analysis['mathematical_patterns']['prime_factors']}")
        print(f"Is Fibonacci length: {analysis['mathematical_patterns']['is_fibonacci']}")

        # Create visualizations
        print("\nGenerating visualizations...")
        analyzer.visualize_sequence_patterns()

    else:
        print("Failed to fetch sequence")

if __name__ == "__main__":
    analyze_ip3r()
