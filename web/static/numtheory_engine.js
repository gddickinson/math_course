// Ports of number_theory_basics.py (NumberTheory) and bio_number_theory.py (BioNumberTheory). Pure functions.
// Python's // and % round toward minus infinity; pyDiv / pyMod keep that behaviour for negative inputs.

export const pyDiv = (a, b) => Math.floor(a / b);
export const pyMod = (a, b) => ((a % b) + b) % b;
export const gcd2 = (a, b) => { a = Math.abs(a); b = Math.abs(b); while (b) [a, b] = [b, a % b]; return a; };
export const lcm2 = (a, b) => (a && b ? Math.abs(a * b) / gcd2(a, b) : 0);

// NumberTheory.euclidean_gcd(): repeated division with the remainder table.
export function euclidean(a, b) {
  const steps = [];
  while (b) { steps.push({ a, b, quotient: pyDiv(a, b), remainder: pyMod(a, b) }); [a, b] = [b, pyMod(a, b)]; }
  return { gcd: a, steps };
}

// NumberTheory.extended_euclidean(): gcd and Bezout coefficients x, y with a*x + b*y = gcd.
export function extendedEuclid(a, b) {
  const steps = [];
  if (a === 0) return { gcd: b, x: 0, y: 1, steps };
  let [or, r, os, s, ot, t] = [a, b, 1, 0, 0, 1];
  while (r) {
    const q = pyDiv(or, r);
    [or, r] = [r, or - q * r]; [os, s] = [s, os - q * s]; [ot, t] = [t, ot - q * t];
    steps.push({ quotient: q, remainder: r, x: s, y: t });
  }
  return { gcd: or, x: os, y: ot, steps };
}

export function gcd({ a, b }) {
  const e = euclidean(a, b);
  return { gcd: e.gcd, steps: e.steps, bezout: extendedEuclid(a, b) };
}

// NumberTheory.diophantine_solver(): one solution of a*x + b*y = c, if gcd(a, b) divides c.
export function diophantine({ a, b, c }) {
  const { gcd: g, x, y } = extendedEuclid(Math.abs(a), Math.abs(b));
  if (pyMod(c, g) !== 0) return { x0: 0, y0: 0, exists: false };
  let x0 = x * pyDiv(c, g), y0 = y * pyDiv(c, g);
  if (a < 0) x0 = -x0;
  if (b < 0) y0 = -y0;
  return { x0, y0, exists: true };
}

// NumberTheory.sieve_of_eratosthenes(): cross out multiples of each prime from its square.
export function sieve(n) {
  const isP = new Uint8Array(n + 1).fill(1);
  isP[0] = 0; isP[1] = 0;
  for (let i = 2; i <= Math.floor(Math.sqrt(n)); i++) if (isP[i]) for (let j = i * i; j <= n; j += i) isP[j] = 0;
  const out = [];
  for (let i = 0; i <= n; i++) if (isP[i]) out.push(i);
  return out;
}

// NumberTheory.prime_factorization(): [[prime, exponent], ...] by trial division with sieved primes.
export function factorize(n) {
  if (n < 2) return [];
  const f = [];
  for (const p of sieve(Math.floor(Math.sqrt(n)) + 1)) {
    if (p * p > n) break;
    if (n % p === 0) { let e = 0; while (n % p === 0) { e++; n /= p; } f.push([p, e]); }
  }
  if (n > 1) f.push([n, 1]);
  return f;
}

export function primes({ limit, n = 840 }) {
  const pr = sieve(limit);
  return { primes: pr, gaps: pr.slice(1).map((p, i) => p - pr[i]), factors: factorize(n) };
}

// BioNumberTheory.analyze_dna_length(): factors, codon (x3) and nucleosome (147 bp) checks.
export function dnaLength({ length }) {
  const factors = length < 2 ? [] : factorize(length);
  const implications = [];
  if (length % 3 === 0) implications.push('Length is divisible by 3 - suitable for protein coding');
  if (length % 147 < 10) implications.push('Length is close to nucleosome unit multiple');
  if (factors.length === 1 && factors[0][1] === 1) implications.push('Prime length - potential evolutionary significance');
  return { length, factors, is_multiple_3: length % 3 === 0,
    possible_nucleosome_units: length >= 147 ? length / 147 : 0, implications };
}

// BioNumberTheory.simulate_cicada_lifecycle(): for cycles 10-20 years, count years // lcm(cycle, predator) meetings.
export function cicada({ years, predators }) {
  const small = new Set(sieve(20)), out = [];
  for (let cycle = 10; cycle <= 20; cycle++) {
    const encounters = predators.reduce((s, p) => s + pyDiv(years, lcm2(cycle, p)), 0);
    out.push({ cycle, encounters, is_prime: small.has(cycle), relative_fitness: 1 / (encounters + 1) });
  }
  return out;
}

// BioNumberTheory.analyze_genetic_sequences(): gcd, lcm and common factors of several sequence lengths.
export function geneticSequences({ lengths }) {
  const g = lengths.reduce((a, b) => gcd2(a, b)), l = lengths.reduce((a, b) => lcm2(a, b));
  const common = [];
  for (let i = 1; i <= Math.min(...lengths); i++) if (lengths.every(x => x % i === 0)) common.push(i);
  const patterns = [];
  if (common.includes(3)) patterns.push('All sequences are potential protein coding (divisible by 3)');
  if (g > 1) patterns.push(`Common unit of ${g} bases found`);
  return { lengths, gcd: g, lcm: l, common_factors: common, patterns };
}
