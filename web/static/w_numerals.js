// Lesson 1 figures: ancient_numbers.py (EgyptianNumber, BabylonianNumber) and world_numbers.py (RomanNumeral,
// MayanNumeral, ChineseNumeral): one number written in every system, with the place-value expansion.
import { esc } from './core.js';
import { numerals } from './numerals_engine.js';
import { figure, sl, numInput, table, checkButton } from './ui.js';

const sup = n => String(n).split('').map(d => '⁰¹²³⁴⁵⁶⁷⁸⁹'[d]).join('');
const expansion = (digits, base) => digits.map((d, i) => `${d}×${base}${sup(digits.length - 1 - i)}`).join(' + ');

// Mayan digits as stacked bars and dots, most significant level on top (as the script prints them left to right).
function mayanSVG(digits) {
  const H = 26, rows = digits.map((d, k) => {
    const bars = Math.floor(d / 5), dots = d % 5, y0 = k * (H * 2.2);
    if (d === 0) return `<ellipse cx="40" cy="${y0 + 22}" rx="16" ry="8" class="shell0"/><text x="80" y="${y0 + 27}" class="tk">0</text>`;
    let s = '';
    for (let i = 0; i < dots; i++) s += `<circle cx="${40 + (i - (dots - 1) / 2) * 13}" cy="${y0 + 6}" r="4.5" class="dot"/>`;
    for (let b = 0; b < bars; b++) s += `<rect x="16" y="${y0 + 15 + b * 9}" width="48" height="6" rx="2" class="bar"/>`;
    return s + `<text x="80" y="${y0 + 27}" class="tk">${d} × 20${sup(digits.length - 1 - k)}</text>`;
  });
  return `<svg class="mayan" viewBox="0 0 170 ${digits.length * H * 2.2}" role="img" aria-label="Mayan digits">${rows.join('')}</svg>`;
}

export function mount(host, { data }) {
  const f = figure(host, 'One number, six number systems',
    'Egyptian hieroglyphs are additive (one symbol per power of ten, repeated); Babylonian cuneiform is positional in base 60, '
    + 'Mayan in base 20; Roman numerals are shown with and without subtractive notation; Chinese numerals name each place up to 万 (10 000).',
    'EgyptianNumber, BabylonianNumber, RomanNumeral, MayanNumeral, ChineseNumeral');
  let n = 2024;
  const show = () => {
    const r = numerals({ n });
    const no = why => `<span class="mute">${esc(why)}</span>`;
    f.out.innerHTML = `<p class="big-n">${n}</p>` + table(['System', 'Written', 'How'], [
      ['Egyptian', r.egyptian ? `<span class="glyphs">${esc(r.egyptian)}</span>` : no('positive integers only'), 'additive: 1, 10, 100, ... 1 000 000'],
      ['Babylonian', `<span class="glyphs">${esc(r.babylonian_text)}</span><br><code>${r.babylonian.join(';')}</code>`,
        `${n} = ${expansion(r.babylonian, 60)}`],
      ['Roman (subtractive)', r.roman ? `<code>${r.roman}</code>` : no('positive integers only'), 'IV = 5 − 1, CM = 1000 − 100'],
      ['Roman (classical)', r.roman_classical ? `<code>${r.roman_classical}</code>` : no('positive integers only'), 'additive only: IIII, DCCCC'],
      ['Mayan', `<code>${esc(r.mayan_text)}</code>`, `${n} = ${expansion(r.mayan, 20)}`],
      ['Chinese', r.chinese ? `<span class="glyphs">${r.chinese}</span>` : no('below 100 000 only'), 'digit + place name (十 百 千 万)'],
    ], 'systems') + `<div class="mayan-wrap"><span class="small mute">Mayan levels (bar = 5, dot = 1):</span>${mayanSVG(r.mayan)}</div>`;
  };
  const inp = numInput(f.ctl, 'Number', n, v => { n = Math.round(v); sl1.value = Math.min(n, 4000); show(); }, { min: 0, max: 99999999 });
  const sl1 = sl(f.ctl, 'Slide', 0, 4000, 1, n, v => { n = v; inp.value = v; show(); });
  const presets = document.createElement('div');
  presets.className = 'presets';
  presets.innerHTML = '<span class="small mute">Script examples:</span>' + [1, 123, 3642, 60, 121, 3600, 1994, 2024, 3888]
    .map(v => `<button class="alt chip" data-v="${v}">${v}</button>`).join('');
  presets.addEventListener('click', e => { const v = e.target.dataset?.v; if (v) { n = +v; inp.value = n; sl1.value = Math.min(n, 4000); show(); } });
  f.ctl.appendChild(presets);
  checkButton(f, 'numerals', () => ({ n }), data);
  show();
}
