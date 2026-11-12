// Ports of ancient_numbers.py, world_numbers.py and ancient_calculations.py (pure functions, no DOM).
// Each mirrors the Python method named in its comment; engines.test.mjs checks them against the Python output.

// EgyptianNumber.SYMBOLS / to_egyptian(): additive hieroglyphs, largest value first.
export const EGYPTIAN = [[1000000, '🙏'], [100000, '𓆐'], [10000, '☝'], [1000, '𓂀'], [100, '⚪'], [10, '∩'], [1, '|']];
export function egyptian(n) {
  if (!Number.isInteger(n) || n < 1) return null;
  const out = [];
  for (const [v, s] of EGYPTIAN) while (n >= v) { out.push(s); n -= v; }
  return out.join(' ');
}

// BabylonianNumber.to_sexagesimal() / format_sexagesimal(): base-60 digits, each written with 10s and 1s wedges.
export function sexagesimal(n) {
  if (n < 0) return null;
  const r = [];
  while (n > 0) { r.push(n % 60); n = Math.floor(n / 60); }
  return r.length ? r.reverse() : [0];
}
export function babylonianText(n) {
  const d = sexagesimal(n);
  if (!d) return null;
  return d.map(v => { const s = '𐎜'.repeat(Math.floor(v / 10)) + '𐎝'.repeat(v % 10); return s || '0'; }).join(';');
}

// RomanNumeral.to_roman() (subtractive) and to_classical_roman() (additive only).
const ROMAN = [[1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'], [100, 'C'], [90, 'XC'], [50, 'L'], [40, 'XL'],
  [10, 'X'], [9, 'IX'], [5, 'V'], [4, 'IV'], [1, 'I']];
const CLASSICAL = [[1000, 'M'], [500, 'D'], [100, 'C'], [50, 'L'], [10, 'X'], [5, 'V'], [1, 'I']];
const greedy = (n, table) => { let s = ''; for (const [v, sym] of table) while (n >= v) { s += sym; n -= v; } return s; };
export const roman = n => (Number.isInteger(n) && n >= 1 ? greedy(n, ROMAN) : null);
export const romanClassical = n => (Number.isInteger(n) && n >= 1 ? greedy(n, CLASSICAL) : null);

// MayanNumeral.to_vigesimal() / format_mayan(): base-20 digits drawn as bars (5) and dots (1).
export function vigesimal(n) {
  if (n < 0) return null;
  const d = [];
  while (n > 0) { d.push(n % 20); n = Math.floor(n / 20); }
  return d.length ? d.reverse() : [0];
}
export function mayanText(n) {
  const d = vigesimal(n);
  return d && d.map(v => ('-'.repeat(Math.floor(v / 5)) + '.'.repeat(v % 5)) || '0').join(' | ');
}

// ChineseNumeral.to_chinese(): digits with place names up to 万, one 零 for a run of zeros, none at the end.
const CN_DIGITS = '零一二三四五六七八九', CN_PLACES = ['', '十', '百', '千', '万'];
export function chinese(n) {
  if (!Number.isInteger(n) || n < 0 || n >= 100000) return null;
  if (n === 0) return CN_DIGITS[0];
  const s = String(n), L = s.length;
  let r = '';
  for (let i = 0; i < L; i++) {
    const v = +s[i];
    if (v !== 0) { r += CN_DIGITS[v]; if (L - i - 1 > 0) r += CN_PLACES[L - i - 1]; }
    else if (r && r[r.length - 1] !== CN_DIGITS[0]) r += CN_DIGITS[0];
  }
  return r.replace(/零+$/, '');
}

export function numerals({ n }) {
  return { egyptian: egyptian(n), babylonian: sexagesimal(n), babylonian_text: babylonianText(n), roman: roman(n),
    roman_classical: romanClassical(n), mayan: vigesimal(n), mayan_text: mayanText(n), chinese: chinese(n) };
}

// EgyptianMultiplication.multiply(): halve the multiplier, double the multiplicand, add rows with an odd multiplier.
export function egyptianMultiply({ a, b }) {
  const steps = [];
  let result = 0;
  while (b > 0) {
    steps.push({ multiplier: b, multiplicand: a, include: (b & 1) === 1 });
    if (b & 1) result += a;
    a *= 2; b = Math.floor(b / 2);
  }
  return { result, steps };
}

// BabylonianSquareRoot.calculate(): x <- (x + n/x)/2 from x = n/2, stop when a step changes x by < 1e-10.
export function babylonianSqrt({ n, iterations = 10 }) {
  if (n < 0) return null;
  const steps = [];
  if (n === 0) return { result: 0, steps };
  let x = n / 2;
  for (let i = 0; i < iterations; i++) {
    const nx = (x + n / x) / 2;
    steps.push({ iteration: i + 1, estimate: nx, error: Math.abs(nx - x) });
    if (Math.abs(nx - x) < 1e-10) break;
    x = nx;
  }
  return { result: x, steps };
}
