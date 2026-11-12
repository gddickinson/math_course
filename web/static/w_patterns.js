// Lesson 5 figures: bio_math_patterns.py (BioMathPatterns), bio_math_enhanced.py (FibonacciAnalyzer,
// MathematicalPatternAnalyzer) and math_bio_demo.py: phyllotaxis, golden-ratio gene lengths, the DNA spiral and the
// full "sequence length" analysis.
import { esc } from './core.js';
import { phyllotaxis, geneLengths, dnaSpiral, sequenceLength, fibonacciWindow, PROPERTY_NAMES, GOLDEN } from './patterns_engine.js';
import { chart, ramp } from './plot.js';
import { figure, sl, numInput, textInput, table, kv, num, checkButton } from './ui.js';

function phyllo(host, data) {
  const f = figure(host, 'Phyllotaxis: seeds placed at a fixed angle',
    'Point k sits at radius √k and angle k·α. With the golden angle (≈137.5°) the seeds pack evenly into interlocking spirals; '
    + 'the script compares 137.3°, 137.7° and 130° to show how sensitive the pattern is. Colour = order of the seeds.',
    'BioMathPatterns.generate_phyllotaxis(), visualize_phyllotaxis()');
  let n = 500, alpha = 137.5;
  const show = () => {
    const { x, y } = phyllotaxis({ n, alpha });
    f.out.innerHTML = '<div class="plot sq"></div>';
    chart(f.out.querySelector('.plot'), { w: 520, h: 520, equal: true, alt: `phyllotaxis, ${n} points at ${alpha} degrees`,
      series: [{ type: 'scatter', x, y, r: Math.max(1.5, 5 - n / 300), colors: x.map((_, i) => ramp(i / n)), alpha: 0.8 }] });
  };
  sl(f.ctl, 'Points', 20, 1500, 10, n, v => { n = v; show(); });
  const a = sl(f.ctl, 'Angle α (degrees)', 120, 160, 0.1, alpha, v => { alpha = v; show(); });
  const p = document.createElement('div');
  p.className = 'presets';
  p.innerHTML = '<span class="small mute">Script angles:</span>' + [137.5, 137.3, 137.7, 130.0]
    .map(v => `<button class="alt chip" data-v="${v}">${v}°</button>`).join('');
  p.addEventListener('click', e => { const v = e.target.dataset?.v; if (v) { alpha = +v; a.value = v; a.dispatchEvent(new Event('input')); } });
  f.ctl.appendChild(p);
  checkButton(f, 'phyllotaxis', () => ({ n, alpha }), data);
  show();
}

function genes(host, data) {
  const f = figure(host, 'Gene lengths, Fibonacci numbers and the golden ratio',
    `Lengths that are Fibonacci numbers, and pairs whose ratio is within 0.1 of φ = ${GOLDEN.toFixed(6)}. The script's example uses `
    + 'Fibonacci-inspired lengths (610, 987, 1597, 2584).', 'BioMathPatterns.analyze_gene_lengths()');
  let txt = '610, 987, 1597, 2584';
  const parse = () => txt.split(/[\s,;]+/).map(Number).filter(v => Number.isInteger(v) && v > 0).slice(0, 30);
  const show = () => {
    const lengths = parse();
    if (!lengths.length) { f.out.innerHTML = '<p class="mute">Enter positive whole numbers.</p>'; return; }
    const r = geneLengths({ lengths });
    f.out.innerHTML = kv([['Fibonacci lengths', r.fibonacci_matches.join(', ') || 'none']])
      + (r.golden_ratio_approximations.length ? table(['Shorter', 'Longer', 'Ratio', 'Distance from φ'],
        r.golden_ratio_approximations.map(([a, b, q]) => [a, b, q.toFixed(4), Math.abs(q - GOLDEN).toFixed(4)]))
        : '<p class="mute">No pair (in the order given) has a ratio within 0.1 of φ.</p>');
  };
  textInput(f.ctl, 'Lengths (comma separated)', txt, v => { txt = v; show(); });
  checkButton(f, 'gene_lengths', () => ({ lengths: parse() }), data);
  show();
}

function spiral(host) {
  const f = figure(host, 'A DNA sequence drawn as a spiral',
    'Positions 0 … L−1 wound outwards five times; colour marks the position within each codon (i mod 3).',
    'BioMathPatterns.visualize_dna_spirals()');
  let L = 612;
  const show = () => {
    const s = dnaSpiral(L), C = ['var(--accent2)', 'var(--accent)', 'var(--accent3)'];
    f.out.innerHTML = '<div class="plot sq"></div>';
    chart(f.out.querySelector('.plot'), { w: 460, h: 460, equal: true, alt: 'DNA spiral',
      series: [{ type: 'scatter', x: s.x, y: s.y, r: 3, colors: s.codon.map(c => C[c]), alpha: 0.7 },
        ...['1st', '2nd', '3rd'].map((t, i) => ({ type: 'scatter', x: [], y: [], color: C[i], label: `${t} codon position` }))] });
  };
  sl(f.ctl, 'Sequence length', 30, 1500, 3, L, v => { L = v; show(); });
  show();
}

function seqLen(host, data) {
  const f = figure(host, 'Mathematical analysis of a sequence length',
    'The full analysis run by math_bio_demo.py: nearest Fibonacci numbers, prime factors, divisors and symmetry of a length '
    + '(its example: 2584, a Fibonacci number).', 'MathematicalPatternAnalyzer.analyze_sequence_length(), FibonacciAnalyzer');
  let n = 2584;
  const show = () => {
    const r = sequenceLength({ length: n }), fa = r.fibonacci_analysis, pa = r.prime_analysis, da = r.divisibility_analysis;
    const w = fibonacciWindow(n);
    f.out.innerHTML = `<div class="two"><div class="p1"></div><div class="p2"></div><div class="p3"></div><div class="p4"></div></div>
      <div class="two"><div>${kv([['Nearest Fibonacci', `${fa.nearest_lower} (F${fa.lower_index}) ≤ ${n} ≤ ${fa.nearest_upper} (F${fa.upper_index})`],
        ['Properties', PROPERTY_NAMES.map((t, i) => `${t}: ${r.properties[i] ? 'yes' : 'no'}`).join('<br>')],
        ['Prime factors', pa.prime_factors.join(' × ') || '–'], ['Is prime', pa.is_prime ? 'yes' : 'no'],
        ['Largest prime factor', num(pa.largest_prime_factor)]])}</div>
      <div>${kv([['Divisors', da.divisor_count], ['Multiple of 3 (codons)', da.is_multiple_of_3 ? 'yes' : 'no'],
        ['Perfect square / cube', `${da.perfect_square ? 'yes' : 'no'} / ${da.perfect_cube ? 'yes' : 'no'}`],
        ['Binary', `<code>${esc(r.symmetry_analysis.binary_representation)}</code>${r.symmetry_analysis.binary_palindrome ? ' (palindrome)' : ''}`],
        ['Digit sum / product', `${r.symmetry_analysis.digit_sum} / ${r.symmetry_analysis.digit_product}`]])}</div></div>`;
    const q = s => f.out.querySelector(s);
    chart(q('.p1'), { w: 420, h: 250, title: 'Position in Fibonacci sequence', x: { label: 'index' }, y: { label: 'value' },
      series: [{ type: 'line', x: w.index, y: w.value, markers: true, label: 'Fibonacci numbers' }, { type: 'hline', y: n, color: 'var(--accent2)', label: 'target' }] });
    chart(q('.p2'), { w: 420, h: 250, title: 'Distance to nearby Fibonacci numbers', x: { label: 'Fibonacci index' }, y: { label: 'distance' },
      series: [{ type: 'bar', x: w.index, y: w.value.map(v => Math.abs(n - v)), color: 'var(--accent3)' }] });
    chart(q('.p3'), { w: 420, h: 250, title: 'Fibonacci-related properties', y: { min: 0, max: 1.1, ticks: [[0, 'no'], [1, 'yes']] },
      x: { ticks: ['Is Fib', 'Near', 'Multiple', 'Between'].map((t, i) => [i, t]) }, alt: PROPERTY_NAMES.join(', '),
      series: [{ type: 'bar', x: [0, 1, 2, 3], y: r.properties.map(Number), color: 'var(--accent)' }] });
    const fc = pa.factor_counts;
    chart(q('.p4'), { w: 420, h: 250, title: 'Prime factor distribution', x: { label: 'prime factor', ticks: fc.map(([p], i) => [i, String(p)]) },
      y: { label: 'count', min: 0 }, series: [{ type: 'bar', x: fc.map((_, i) => i), y: fc.map(([, c]) => c), color: 'var(--accent2)' }] });
  };
  numInput(f.ctl, 'Sequence length', n, v => { n = Math.round(v); show(); }, { min: 1, max: 100000 });
  checkButton(f, 'sequence_length', () => ({ length: n }), data);
  show();
}

export function mount(host, { data }) {
  phyllo(host, data);
  genes(host, data);
  spiral(host);
  seqLen(host, data);
}
