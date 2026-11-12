// Ports of bio_math_patterns.py (BioMathPatterns) and bio_math_enhanced.py (FibonacciAnalyzer,
// MathematicalPatternAnalyzer). Pure functions; engines.test.mjs compares them with the Python output.

export const GOLDEN = (1 + Math.sqrt(5)) / 2;

export function fibonacci(n) { let a = 0, b = 1; for (let i = 0; i < n; i++) [a, b] = [b, a + b]; return a; }

// numpy.linspace(a, b, n) as numpy computes it (step = (b - a) / (n - 1), last point exactly b).
export function linspace(a, b, n) {
  if (n === 1) return [a];
  const step = (b - a) / (n - 1), out = new Array(n);
  for (let i = 0; i < n; i++) out[i] = a + i * step;
  out[n - 1] = b;
  return out;
}

// BioMathPatterns.generate_phyllotaxis(): point i at radius sqrt(i), angle i * alpha (degrees).
export function phyllotaxis({ n, alpha }) {
  const rad = alpha * Math.PI / 180, x = new Array(n), y = new Array(n);
  for (let i = 0; i < n; i++) { const r = Math.sqrt(i), t = rad * i; x[i] = r * Math.cos(t); y[i] = r * Math.sin(t); }
  return { x, y };
}

// BioMathPatterns.analyze_gene_lengths(): Fibonacci members and pairs whose ratio is within 0.1 of phi.
export function geneLengths({ lengths }) {
  const max = Math.max(...lengths), fibs = [];
  for (let i = 0; fibonacci(i) <= max; i++) fibs.push(fibonacci(i));
  const pairs = [];
  for (let i = 0; i < lengths.length; i++) for (let j = i + 1; j < lengths.length; j++) {
    const ratio = lengths[j] / lengths[i];
    if (Math.abs(ratio - GOLDEN) < 0.1) pairs.push([lengths[i], lengths[j], ratio]);
  }
  return { lengths, fibonacci_matches: lengths.filter(l => fibs.includes(l)), golden_ratio_approximations: pairs, patterns: [] };
}

// BioMathPatterns.visualize_dna_spirals(): theta 0..turns*2pi, r 0..1, colour = position in codon (i % 3).
export function dnaSpiral(length, turns = 5) {
  const th = linspace(0, turns * 2 * Math.PI, length), r = linspace(0, 1, length);
  return { x: th.map((t, i) => r[i] * Math.cos(t)), y: th.map((t, i) => r[i] * Math.sin(t)), codon: th.map((_, i) => i % 3) };
}

// FibonacciAnalyzer: list [0, 1, 1, 2, ...] grown past max(1000, n).
function fibList(n) {
  const f = [0, 1];
  const grow = limit => { while (f[f.length - 1] <= limit) f.push(f[f.length - 1] + f[f.length - 2]); };
  grow(1000);
  while (f[f.length - 1] < n) grow(n * 2);
  return f;
}

// FibonacciAnalyzer.find_nearest_fibonacci()
export function nearestFibonacci(n, f = fibList(n)) {
  const lower = Math.max(...f.filter(x => x <= n)), upper = Math.min(...f.filter(x => x >= n));
  return { nearest_lower: lower, nearest_upper: upper, lower_index: f.indexOf(lower), upper_index: f.indexOf(upper),
    distance_to_lower: n - lower, distance_to_upper: upper - n };
}

// MathematicalPatternAnalyzer.analyze_prime_factors() (its own trial-division loop)
export function primeFactors(n) {
  const f = [];
  let d = 2;
  while (n > 1) {
    while (n % d === 0) { f.push(d); n /= d; }
    d += 1;
    if (d * d > n) { if (n > 1) f.push(n); break; }
  }
  const counts = new Map();
  for (const p of f) counts.set(p, (counts.get(p) || 0) + 1);
  return { prime_factors: f, unique_factors: [...counts.keys()], factor_counts: [...counts.entries()],
    is_prime: f.length === 1, largest_prime_factor: f.length ? Math.max(...f) : null,
    smallest_prime_factor: f.length ? Math.min(...f) : null };
}

export function divisibility(n) {
  const divisors = [];
  for (let i = 1; i <= n; i++) if (n % i === 0) divisors.push(i);
  return { divisors, divisor_count: divisors.length, is_even: n % 2 === 0, is_multiple_of_3: n % 3 === 0,
    perfect_square: Math.floor(n ** 0.5) ** 2 === n, perfect_cube: Math.round(n ** (1 / 3)) ** 3 === n };
}

export function symmetry(n) {
  const bin = n.toString(2), dec = String(n), rev = s => [...s].reverse().join('');
  return { binary_representation: bin, binary_palindrome: bin === rev(bin), decimal_palindrome: dec === rev(dec),
    digit_sum: [...dec].reduce((s, d) => s + +d, 0), digit_product: [...dec].reduce((s, d) => s * +d, 1) };
}

export const PROPERTY_NAMES = ['Is Fibonacci', 'Near Fibonacci', 'Multiple of Fib', 'Between Consecutive'];

// MathematicalPatternAnalyzer.analyze_sequence_length() + the bars of FibonacciAnalyzer.plot_properties()
export function sequenceLength({ length: n }) {
  const f = fibList(n), fa = nearestFibonacci(n, f);
  const properties = [
    f.includes(n),
    Math.min(fa.distance_to_lower, fa.distance_to_upper) < n * 0.1,
    f.slice(2, fa.upper_index + 1).some(x => x > 1 && n % x === 0),
    fa.nearest_lower !== fa.nearest_upper,
  ];
  return { fibonacci_analysis: fa, prime_analysis: primeFactors(n), divisibility_analysis: divisibility(n),
    symmetry_analysis: symmetry(n), properties };
}

// FibonacciAnalyzer.plot_fibonacci_sequence(): indices and values around n.
export function fibonacciWindow(n) {
  const f = fibList(n), fa = nearestFibonacci(n, f);
  const s = Math.max(2, fa.lower_index - 2), e = Math.min(f.length, fa.upper_index + 3), idx = [];
  for (let i = s; i < e; i++) idx.push(i);
  return { index: idx, value: idx.map(i => f[i]) };
}
