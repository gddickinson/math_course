// Lesson 3 figures: number_theory_basics.py (NumberTheory): Euclid's algorithm with Bezout coefficients, linear
// Diophantine equations, the sieve of Eratosthenes with prime gaps, and the prime factorization tree.
import { esc } from './core.js';
import { gcd, diophantine, primes, factorize } from './numtheory_engine.js';
import { chart } from './plot.js';
import { figure, sl, numInput, table, checkButton } from './ui.js';

function euclid(host, data) {
  const f = figure(host, 'Euclidean algorithm (c. 300 BCE)',
    'Divide, keep the remainder, repeat with (b, remainder) until the remainder is 0; the last non-zero remainder is the GCD. '
    + 'The extended version also tracks x and y with a·x + b·y = gcd(a, b).', 'NumberTheory.euclidean_gcd(), extended_euclidean()');
  let a = 48, b = 18;
  const show = () => {
    const r = gcd({ a, b }), z = r.bezout;
    f.out.innerHTML = `<p class="eq">gcd(${a}, ${b}) = ${r.gcd} &nbsp; · &nbsp; ${a}·(${z.x}) + ${b}·(${z.y}) = ${a * z.x + b * z.y}</p>`
      + table(['a', 'b', 'quotient a // b', 'remainder a % b', 'equation'],
        r.steps.map(s => [s.a, s.b, s.quotient, s.remainder, `<code>${s.a} = ${s.quotient}·${s.b} + ${s.remainder}</code>`]));
  };
  numInput(f.ctl, 'a', a, v => { a = Math.round(v); show(); }, { min: 0, max: 1e9 });
  numInput(f.ctl, 'b', b, v => { b = Math.round(v); show(); }, { min: 0, max: 1e9 });
  checkButton(f, 'gcd', () => ({ a, b }), data);
  show();
}

function dioph(host, data) {
  const f = figure(host, 'Linear Diophantine equation a·x + b·y = c',
    'Integer solutions exist exactly when gcd(a, b) divides c; one solution is the Bezout pair scaled by c / gcd.',
    'NumberTheory.diophantine_solver()');
  let a = 15, b = 21, c = 12;
  const show = () => {
    if (a === 0 && b === 0) { f.out.innerHTML = '<p class="mute">a and b cannot both be 0.</p>'; return; }
    const r = diophantine({ a, b, c }), g = gcd({ a: Math.abs(a), b: Math.abs(b) }).gcd;
    f.out.innerHTML = r.exists
      ? `<p class="eq">${a}·(${r.x0}) + ${b}·(${r.y0}) = ${a * r.x0 + b * r.y0}</p><p>gcd(${Math.abs(a)}, ${Math.abs(b)}) = ${g} divides ${c}, so x = ${r.x0}, y = ${r.y0} is a solution.</p>`
      : `<p class="eq">no integer solution</p><p>gcd(${Math.abs(a)}, ${Math.abs(b)}) = ${g} does not divide ${c}.</p>`;
  };
  for (const [k, v] of [['a', a], ['b', b], ['c', c]]) {
    numInput(f.ctl, k, v, x => { x = Math.round(x); if (k === 'a') a = x; else if (k === 'b') b = x; else c = x; show(); }, { min: -1e6, max: 1e6 });
  }
  checkButton(f, 'diophantine', () => ({ a, b, c }), data);
  show();
}

function sieveFig(host, data) {
  const f = figure(host, 'Sieve of Eratosthenes (c. 240 BCE) and prime gaps',
    'Cross out the multiples of each prime starting from its square; what survives is prime. The plot shows the gap from each prime to the next.',
    'NumberTheory.sieve_of_eratosthenes(), visualize_prime_gaps()');
  let limit = 1000;
  const show = () => {
    const r = primes({ limit, n: 2 }), p = r.primes;
    const maxGap = Math.max(...r.gaps, 0), at = p[r.gaps.indexOf(maxGap)];
    f.out.innerHTML = `<p>${p.length} primes up to ${limit}; largest gap ${maxGap} (after ${at}).</p><div class="plot"></div>`
      + (limit <= 200 ? `<div class="sieve">${Array.from({ length: limit - 1 }, (_, i) => i + 2).map(v =>
        `<span class="${p.includes(v) ? 'pr' : ''}">${v}</span>`).join('')}</div>` : '');
    chart(f.out.querySelector('.plot'), { h: 280, title: `Prime gaps up to ${limit}`, x: { label: 'prime number' },
      y: { label: 'gap to next prime' }, series: [{ type: 'scatter', x: p.slice(0, -1), y: r.gaps, r: limit > 5000 ? 1.6 : 2.5, alpha: 0.6 }] });
  };
  sl(f.ctl, 'Limit', 30, 20000, 10, limit, v => { limit = v; show(); });
  checkButton(f, 'primes', () => ({ limit, n: 2 }), data);
  show();
}

function factorTree(host, data) {
  const f = figure(host, 'Prime factorization tree', 'Every integer above 1 is a product of primes in exactly one way.',
    'NumberTheory.prime_factorization(), visualize_factorization_tree()');
  let n = 840;
  const show = () => {
    const fac = factorize(n);
    if (!fac.length) { f.out.innerHTML = '<p class="mute">Numbers below 2 have no prime factors.</p>'; return; }
    const W = 640, H = 220, xs = fac.map((_, i) => (fac.length === 1 ? W / 2 : 70 + i * (W - 140) / (fac.length - 1)));
    f.out.innerHTML = `<p class="eq">${n} = ${fac.map(([p, e]) => (e > 1 ? `${p}<sup>${e}</sup>` : p)).join(' × ')}</p>
    <svg class="ftree" viewBox="0 0 ${W} ${H}" role="img" aria-label="factorization tree of ${n}">
      ${xs.map(x => `<line x1="${W / 2}" y1="52" x2="${x}" y2="150"/>`).join('')}
      <circle cx="${W / 2}" cy="34" r="30"/><text x="${W / 2}" y="40" text-anchor="middle">${esc(n)}</text>
      ${fac.map(([p, e], i) => `<circle cx="${xs[i]}" cy="172" r="30" class="leaf"/><text x="${xs[i]}" y="178" text-anchor="middle">${p}^${e}</text>`).join('')}
    </svg>`;
  };
  numInput(f.ctl, 'n', n, v => { n = Math.round(v); show(); }, { min: 1, max: 1e12 });
  checkButton(f, 'primes', () => ({ limit: 2, n }), data);
  show();
}

export function mount(host, { data }) {
  euclid(host, data);
  dioph(host, data);
  sieveFig(host, data);
  factorTree(host, data);
}
