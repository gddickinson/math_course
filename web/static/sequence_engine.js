// Ports of the offline parts of bio_sequence_analysis.py (NCBISequenceAnalyzer.analyze_sequence and the GC window of
// visualize_sequence_patterns) and ip3r_analysis.py (IP3RAnalyzer.analyze_domains, find_calcium_binding_sites).
// Translation uses the standard genetic code (Biopython's default table 1). Pure functions.
import { primeFactors } from './patterns_engine.js';

// Upper-case, U -> T, keep only A/C/G/T (as web/compute_seq.py clean()).
export const clean = s => s.toUpperCase().replace(/U/g, 'T').replace(/[^ACGT]/g, '');
const count = (s, ch) => s.split(ch).length - 1;

const B = 'TCAG', AA = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG';
export const CODON_TABLE = {};
for (let i = 0; i < 64; i++) CODON_TABLE[B[i >> 4] + B[(i >> 2) & 3] + B[i & 3]] = AA[i];
export function translate(s) {
  let p = '';
  for (let i = 0; i + 3 <= s.length; i += 3) p += CODON_TABLE[s.slice(i, i + 3)];
  return p;
}

// NCBISequenceAnalyzer._find_repeats(): every k-mer (k = 4..10) seen more than once, in first-seen order.
function repeats(s, top = 5) {
  const out = {};
  for (let k = 4; k <= 10; k++) {
    const m = new Map();
    for (let i = 0; i + k <= s.length; i++) { const w = s.slice(i, i + k); m.set(w, (m.get(w) || 0) + 1); }
    const rep = [...m].filter(([, c]) => c > 1);
    out[k] = { distinct: rep.length, top: rep.sort((a, b) => b[1] - a[1]).slice(0, top) };
  }
  return out;
}

function isFibonacci(n) {
  const f = new Set([0, 1]);
  let a = 0, b = 1;
  while (b <= n) { [a, b] = [b, a + b]; f.add(b); }
  return f.has(n);
}

export function sequence({ seq, mrna = false }) {
  const s = clean(seq), L = s.length;
  if (!L) return null;
  const coding = mrna ? s : s.replace(/T/g, 'U');   // _analyze_codons transcribes unless the record is an mRNA
  const codons = new Map();
  let total = 0;
  for (let i = 0; i < coding.length - 2; i += 3) { const c = coding.slice(i, i + 3); codons.set(c, (codons.get(c) || 0) + 1); total++; }
  const w = 100, windows = [];
  for (let i = 0; i < L - w; i += w) { const x = s.slice(i, i + w); windows.push((count(x, 'G') + count(x, 'C')) / w); }
  return {
    length: L, gc_content: (count(s, 'G') + count(s, 'C')) / L * 100, counts: [...'ATGC'].map(c => count(s, c)),
    codons: { total_codons: total, unique_codons: codons.size, most_common: [...codons].sort((a, b) => b[1] - a[1]).slice(0, 5) },
    repeats: repeats(s), gc_windows: windows,
    patterns: { prime_factors: primeFactors(L).prime_factors, is_fibonacci: isFibonacci(L), divisible_by_3: L % 3 === 0,
      golden_ratio_approx: L > 1 ? L / Math.floor(L / 2) : null },
  };
}

// IP3RAnalyzer tables (positions as the script gives them; it slices the nucleotide sequence with them).
export const DOMAINS = { IP3_binding: [[224, 604]], calcium_binding: [[2230, 2749]], channel_region: [[2398, 2589]],
  suppressor: [[1574, 1654]], regulatory: [[918, 1207], [1574, 1654]] };
export const MULTI = new Set(['calcium_binding', 'regulatory']);   // given as lists in Python
export const CA_MOTIFS = ['D[DNS][DNS][DNS]', '[DE][LIVMFYW][DNS][DNS]'];
export const KD = { A: 1.8, R: -4.5, N: -3.5, D: -3.5, C: 2.5, Q: -3.5, E: -3.5, G: -0.4, H: -3.2, I: 4.5, L: 3.8, K: -3.9,
  M: 1.9, F: 2.8, P: -1.6, S: -0.8, T: -0.7, W: -0.9, Y: -1.3, V: 4.2 };

export function hydrophobicity(dna) {
  const aa = translate(dna);
  return [...aa].reduce((t, a) => t + (KD[a] || 0), 0) / aa.length;
}

export function ip3r({ seq }) {
  const s = clean(seq), domains = {};
  for (const [name, regions] of Object.entries(DOMAINS)) {
    const res = regions.filter(([, e]) => e <= s.length).map(([a, e]) => {
      const d = s.slice(a, e);
      return { length: d.length, gc_content: (count(d, 'G') + count(d, 'C')) / d.length, hydrophobicity: hydrophobicity(d),
        conservation: null };
    });
    if (!res.length) continue;
    if (res.length === 1) { domains[name] = res[0]; continue; }
    const tot = res.reduce((t, r) => t + r.length, 0);
    domains[name] = { regions: res, total_length: tot, average_conservation: null, length: tot, conservation: null };
  }
  const protein = translate(s), sites = [];
  for (const m of CA_MOTIFS) {
    for (const hit of protein.matchAll(new RegExp(m, 'g'))) {
      sites.push({ motif: m, position: hit.index, sequence: hit[0],
        in_known_domain: DOMAINS.calcium_binding.some(([a, e]) => a <= hit.index * 3 && hit.index * 3 <= e) });
    }
  }
  return { protein, domains, sites };
}
