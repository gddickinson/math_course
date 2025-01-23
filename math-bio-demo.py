from bio_math_enhanced import FibonacciAnalyzer, MathematicalPatternAnalyzer
from ip3r_analysis import IP3RAnalyzer

def analyze_sequence_mathematics(sequence_length: int):
    """
    Perform comprehensive mathematical analysis of a sequence length
    """
    # Initialize analyzers
    math_analyzer = MathematicalPatternAnalyzer()

    print(f"\nAnalyzing sequence length: {sequence_length}")
    print("=" * 50)

    # Get comprehensive mathematical analysis
    analysis = math_analyzer.analyze_sequence_length(sequence_length)

    # Print Fibonacci analysis
    print("\nFibonacci Analysis:")
    print("-" * 20)
    fib_analysis = analysis['fibonacci_analysis']
    print(f"Nearest Fibonacci numbers:")
    print(f"  Lower: {fib_analysis['nearest_lower']}")
    print(f"  Upper: {fib_analysis['nearest_upper']}")
    print(f"Distances:")
    print(f"  To lower: {fib_analysis['distance_to_lower']}")
    print(f"  To upper: {fib_analysis['distance_to_upper']}")
    print(f"Position in sequence:")
    print(f"  Lower index: {fib_analysis['lower_index']}")
    print(f"  Upper index: {fib_analysis['upper_index']}")

    # Print prime analysis
    print("\nPrime Analysis:")
    print("-" * 20)
    prime_analysis = analysis['prime_analysis']
    print(f"Prime factors: {prime_analysis['prime_factors']}")
    print(f"Is prime: {prime_analysis['is_prime']}")
    print(f"Largest prime factor: {prime_analysis['largest_prime_factor']}")

    # Print divisibility analysis
    print("\nDivisibility Analysis:")
    print("-" * 20)
    div_analysis = analysis['divisibility_analysis']
    print(f"Number of divisors: {div_analysis['divisor_count']}")
    print(f"Is multiple of 3 (codon relevant): {div_analysis['is_multiple_of_3']}")
    print(f"Perfect square: {div_analysis['perfect_square']}")

    # Create visualizations
    print("\nGenerating visualizations...")
    math_analyzer.visualize_patterns(sequence_length)
    print("\nGenerating Fibonacci analysis...")
    math_analyzer.fibonacci_analyzer.visualize_fibonacci_analysis(sequence_length)

def analyze_ip3r_combined(email: str):
    """
    Combine mathematical and biological analysis of IP3R
    """
    # Initialize analyzers
    ip3r = IP3RAnalyzer(email)
    math_analyzer = MathematicalPatternAnalyzer()

    # Fetch human IP3R sequence
    print("Fetching IP3R sequence...")
    sequences = ip3r.fetch_homologs(["Homo sapiens"])

    if "Homo sapiens" in sequences:
        sequence = sequences["Homo sapiens"]
        sequence_length = len(sequence.seq)

        # Perform mathematical analysis
        print("\nPerforming mathematical analysis...")
        analyze_sequence_mathematics(sequence_length)

        # Analyze domains and their lengths
        print("\nAnalyzing domain lengths...")
        domain_analysis = ip3r.analyze_domains(str(sequence.seq))

        for domain, data in domain_analysis.items():
            print(f"\nAnalyzing {domain} domain (length: {data['length']}):")
            domain_math = math_analyzer.analyze_sequence_length(data['length'])
            print(f"  Prime factors: {domain_math['prime_analysis']['prime_factors']}")
            fib_analysis = domain_math['fibonacci_analysis']
            print(f"  Nearest Fibonacci numbers: {fib_analysis['nearest_lower']} < {data['length']} < {fib_analysis['nearest_upper']}")
    else:
        print("Failed to fetch IP3R sequence")

if __name__ == "__main__":
    # Example 1: Analyze a specific sequence length
    print("Example 1: Analyzing a specific sequence length")
    sequence_length = 2584  # Example length (a Fibonacci number)
    analyze_sequence_mathematics(sequence_length)

    # Example 2: Analyze IP3R sequence
    print("\nExample 2: Analyzing IP3R sequence")
    analyze_ip3r_combined("george.dickinson@gmail.com")  # Replace with your email
