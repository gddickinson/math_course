// Lesson 9 figures: bio_sequence_analysis.py (NCBISequenceAnalyzer) and ip3r_analysis.py (IP3RAnalyzer), offline
// parts only: the scripts download sequences from NCBI, so here you paste a sequence (or make a random one).
import { esc, rng } from './core.js';
import { sequence, ip3r, clean, DOMAINS } from './sequence_engine.js';
import { chart, PALETTE } from './plot.js';
import { figure, sl, numInput, textInput, checkbox, table, kv, num, checkButton } from './ui.js';

const BASES = 'ATGC';
function randomSeq(n, seed) { const r = rng(seed); return Array.from({ length: n }, () => BASES[Math.floor(r() * 4)]).join(''); }

export function mount(host, { data }) {
  const state = { seq: randomSeq(3000, 1), mrna: false };
  const src = figure(host, 'Your sequence',
    'Paste a DNA or RNA sequence (FASTA headers, spaces, numbers and letters other than A/C/G/T/U are removed; U is read as T), '
    + 'or generate a random one. The scripts themselves download the human ITPR1 (IP3 receptor 1) mRNA from NCBI: '
    + 'paste that sequence (accession NM_001099952.2) to reproduce their analysis.');
  const area = textInput(src.ctl, 'Sequence', state.seq, v => { state.seq = v.split('\n').filter(l => !l.startsWith('>')).join(''); update(); },
    { area: true, placeholder: 'ATGTCTGACAAA...' });
  area.rows = 6;
  let n = 3000, seed = 1;
  sl(src.ctl, 'Random length', 100, 12000, 100, n, v => { n = v; });
  numInput(src.ctl, 'Random seed', seed, v => { seed = Math.round(v); }, { min: 0, max: 1e9 });
  const b = document.createElement('button');
  b.className = 'alt'; b.textContent = 'Random sequence';
  b.addEventListener('click', () => { state.seq = randomSeq(n, seed); area.value = state.seq; update(); });
  src.ctl.appendChild(b);
  checkbox(src.ctl, 'Record is an mRNA (codons read as given, not transcribed)', false, c => { state.mrna = c; update(); });

  const f1 = figure(host, 'Composition, codons and repeats',
    'GC content, base counts, GC fraction in windows of 100 bases, the most common codons (read in frame from the first base; '
    + 'transcribed T→U unless the record is an mRNA), repeated k-mers of length 4–10, and the number patterns of the length.',
    'NCBISequenceAnalyzer.analyze_sequence(), visualize_sequence_patterns()');
  const f2 = figure(host, 'IP3 receptor domains and calcium-binding motifs',
    'The script\'s domain table (IP3 binding core, calcium binding, channel region, suppressor, regulatory) gives amino-acid residue ranges of '
    + 'the IP3R1 protein. They are mapped onto your mRNA through its coding sequence, taken as the longest ATG…stop reading frame: residues a–b '
    + 'are nucleotides CDS start + 3(a−1) … CDS start + 3b. Domains beyond the end of the protein are skipped. Hydrophobicity is the mean '
    + 'Kyte–Doolittle value of the domain\'s amino acids; calcium motifs are EF-hand-like patterns searched in the protein. Conservation needs '
    + 'sequences from several species downloaded from NCBI, so it is empty here.', 'IP3RAnalyzer.analyze_domains(), find_calcium_binding_sites()');
  checkButton(f1, 'sequence', () => ({ seq: state.seq, mrna: state.mrna }), data);
  checkButton(f2, 'ip3r', () => ({ seq: state.seq }), data);

  function update() {
    const s = clean(state.seq);
    src.out.innerHTML = `<p>${s.length.toLocaleString('en')} bases after cleaning${s.length ? '' : ': nothing to analyse'}.</p>`;
    if (!s.length) { f1.out.innerHTML = f2.out.innerHTML = ''; return; }
    if (s.length > 200000) { f1.out.innerHTML = f2.out.innerHTML = '<p class="err">Please use at most 200 000 bases.</p>'; return; }
    const r = sequence(state);
    const mp = r.patterns;
    f1.out.innerHTML = kv([['Length', r.length], ['GC content', `${num(r.gc_content, 2)}%`],
      ['Codons (total / distinct)', `${r.codons.total_codons} / ${r.codons.unique_codons}`],
      ['Length factors', mp.prime_factors.join(' × ') || '–'], ['Fibonacci length', mp.is_fibonacci ? 'yes' : 'no'],
      ['Divisible by 3', mp.divisible_by_3 ? 'yes' : 'no'], ['length / (length // 2)', num(mp.golden_ratio_approx, 4)]])
      + '<div class="two"><div class="p1"></div><div class="p2"></div><div class="p3"></div><div class="p4"></div></div>'
      + `<div class="two"><div><h3>Most common codons</h3>${table(['Codon', 'Count'], r.codons.most_common.map(([c, k]) => [`<code>${c}</code>`, k]))}</div>
        <div><h3>Most repeated k-mers</h3>${table(['k', 'Distinct repeated', 'Top'], Object.entries(r.repeats).map(([k, v]) =>
        [k, v.distinct, v.top.slice(0, 3).map(([w, c]) => `<code>${w}</code>×${c}`).join(' ')]))}</div></div>`;
    const q = c => f1.out.querySelector(c);
    chart(q('.p1'), { w: 420, h: 240, title: 'Nucleotide distribution', x: { ticks: [...BASES].map((c, i) => [i, c]) },
      series: [{ type: 'bar', x: [0, 1, 2, 3], y: r.counts, colors: PALETTE.slice(0, 4) }] });
    chart(q('.p2'), { w: 420, h: 240, title: 'GC content distribution (windows of 100)', x: { label: 'window' }, y: { label: 'GC fraction' },
      series: [{ type: 'line', x: r.gc_windows.map((_, i) => i), y: r.gc_windows, color: 'var(--accent3)', width: 1.5 }] });
    const ks = Object.keys(r.repeats);
    chart(q('.p3'), { w: 420, h: 240, title: 'Repeat pattern distribution', x: { label: 'repeat length k', ticks: ks.map(k => [+k, k]) },
      y: { label: 'distinct repeated k-mers' }, series: [{ type: 'bar', x: ks.map(Number), y: ks.map(k => r.repeats[k].distinct), color: 'var(--accent2)' }] });
    const turns = Math.floor(s.length / 100), L = Math.min(s.length, 6000), idx = { A: 0, T: 1, G: 2, C: 3 };
    const th = i => (s.length > 1 ? i / (s.length - 1) : 0) * turns * 2 * Math.PI, rr = i => (s.length > 1 ? i / (s.length - 1) : 0);
    const pts = Array.from({ length: L }, (_, i) => i);
    chart(q('.p4'), { w: 420, h: 420, equal: true, title: `Sequence spiral (one turn per 100 bases${L < s.length ? `, first ${L}` : ''})`,
      series: [{ type: 'scatter', x: pts.map(i => rr(i) * Math.cos(th(i))), y: pts.map(i => rr(i) * Math.sin(th(i))), r: 1.3,
        colors: pts.map(i => PALETTE[idx[s[i]]]), alpha: 0.7 }] });

    const ip = ip3r(state), names = Object.keys(DOMAINS);
    f2.out.innerHTML = '<div class="plot"></div>' + (Object.keys(ip.domains).length
      ? table(['Domain', 'Residues', 'GC fraction', 'Hydrophobicity (KD)'], Object.entries(ip.domains).map(([k, d]) =>
        [k + (d.regions ? ` (${d.regions.length} regions)` : ''), d.length, d.regions ? d.regions.map(x => num(x.gc_content, 3)).join(', ') : num(d.gc_content, 3),
          d.regions ? d.regions.map(x => num(x.hydrophobicity, 3)).join(', ') : num(d.hydrophobicity, 3)]))
      : `<p class="mute">The protein (${ip.protein.length} residues) is shorter than every domain (the shortest ends at residue 604).</p>`)
      + `<h3>Calcium-binding motifs: ${ip.sites.length} found</h3>`
      + (ip.sites.length ? table(['Motif', 'Residue', 'Match', 'In calcium-binding domain'],
        ip.sites.slice(0, 40).map(t => [`<code>${esc(t.motif)}</code>`, t.position, `<code>${t.sequence}</code>`, t.in_known_domain ? 'yes' : 'no']))
        + (ip.sites.length > 40 ? `<p class="small mute">first 40 of ${ip.sites.length}</p>` : '') : '')
      + `<p class="small">Coding sequence: nucleotides ${ip.cds[0] + 1}–${ip.cds[1]} (${ip.protein.length} residues).</p><details><summary class="small">Protein (${ip.protein.length} amino acids)</summary><pre class="prot">${esc(ip.protein)}</pre></details>`;
    const segs = names.flatMap((k, i) => DOMAINS[k].map(([a, e]) => [a, i, e, i, PALETTE[i % PALETTE.length], 14]));
    chart(f2.out.querySelector('.plot'), { h: 220, ml: 118, title: 'IP3R1 domain structure (residues) and the length of your protein',
      x: { label: 'residue', min: 0, max: Math.max(2800, ip.protein.length * 1.02) }, y: { min: -0.7, max: names.length - 0.3, ticks: names.map((k, i) => [i, k.replace('_', ' ')]) },
      series: [{ type: 'segments', data: segs }, { type: 'line', x: [ip.protein.length, ip.protein.length], y: [-0.7, names.length], color: 'var(--warn)', dash: '5 4', label: 'end of your protein' }] });
  }
  update();
}
