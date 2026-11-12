// Shared building blocks for the lesson figures: a figure panel with a controls column and a plot area, labelled
// number inputs / selects / segmented buttons, small tables, and the "Check with Python" button.
import { esc, api, isStatic, slider } from './core.js';
import { jsCompute, diff } from './js_compute.js';

let uid = 0;

// figure(host, title, caption): returns { ctl, out, foot } elements inside a new panel.
export function figure(host, title, caption = '', source = '') {
  const el = document.createElement('section');
  el.className = 'panel fig';
  el.innerHTML = `<h3>${esc(title)}</h3>${caption ? `<p class="cap">${caption}</p>` : ''}
    <div class="figgrid"><div class="ctl-col"></div><div class="out"></div></div>
    <div class="foot">${source ? `<span class="src">${esc(source)}</span>` : ''}</div>`;
  host.appendChild(el);
  return { el, ctl: el.querySelector('.ctl-col'), out: el.querySelector('.out'), foot: el.querySelector('.foot') };
}

export function sl(host, label, min, max, step, value, onInput, fmt) {
  return slider(host, { id: `s${++uid}`, label, min, max, step, value, fmt }, onInput);
}

export function numInput(host, label, value, onChange, { min, max, step = 1 } = {}) {
  const id = `n${++uid}`, w = document.createElement('div');
  w.className = 'ctl';
  w.innerHTML = `<label for="${id}">${esc(label)}</label><input id="${id}" type="number" value="${value}"
    ${min !== undefined ? `min="${min}"` : ''} ${max !== undefined ? `max="${max}"` : ''} step="${step}">`;
  host.appendChild(w);
  const inp = w.querySelector('input');
  inp.addEventListener('input', () => {
    let v = +inp.value;
    if (inp.value === '' || !Number.isFinite(v)) return;
    if (min !== undefined) v = Math.max(min, v);
    if (max !== undefined) v = Math.min(max, v);
    onChange(v);
  });
  return inp;
}

export function textInput(host, label, value, onChange, { area = false, placeholder = '' } = {}) {
  const id = `t${++uid}`, w = document.createElement('div');
  w.className = 'ctl';
  const tag = area ? 'textarea' : 'input';
  w.innerHTML = `<label for="${id}">${esc(label)}</label><${tag} id="${id}" placeholder="${esc(placeholder)}" spellcheck="false"
    ${area ? '' : `value="${esc(value)}"`}>${area ? esc(value) + '</textarea>' : ''}`;
  host.appendChild(w);
  const inp = w.querySelector(tag);
  inp.addEventListener('input', () => onChange(inp.value));
  return inp;
}

export function select(host, label, options, value, onChange) {
  const id = `c${++uid}`, w = document.createElement('div');
  w.className = 'ctl';
  w.innerHTML = `<label for="${id}">${esc(label)}</label><select id="${id}">${options.map(o => {
    const [v, t] = Array.isArray(o) ? o : [o, o];
    return `<option value="${esc(v)}" ${v === value ? 'selected' : ''}>${esc(t)}</option>`;
  }).join('')}</select>`;
  host.appendChild(w);
  const s = w.querySelector('select');
  s.addEventListener('change', () => onChange(s.value));
  return s;
}

export function checkbox(host, label, checked, onChange) {
  const id = `k${++uid}`, w = document.createElement('div');
  w.className = 'ctl chk';
  w.innerHTML = `<input type="checkbox" id="${id}" ${checked ? 'checked' : ''}><label for="${id}">${esc(label)}</label>`;
  host.appendChild(w);
  const c = w.querySelector('input');
  c.addEventListener('change', () => onChange(c.checked));
  return c;
}

export function table(head, rows, cls = '') {
  return `<div class="scroll"><table class="${cls}"><thead><tr>${head.map(h => `<th>${esc(h)}</th>`).join('')}</tr></thead>
    <tbody>${rows.map(r => `<tr>${r.map(c => `<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
}

export const kv = pairs => `<dl class="kv">${pairs.map(([k, v]) => `<div><dt>${esc(k)}</dt><dd>${v}</dd></div>`).join('')}</dl>`;
export const num = (v, d = 4) => (v === null || v === undefined ? '–' : typeof v === 'number' ? esc(String(+v.toFixed(d))) : esc(String(v)));

// "Check with Python": re-run this figure's parameters through the repo's Python code (local app only) and compare.
export function checkButton(fig, name, params, data) {
  if (isStatic()) return;
  const b = document.createElement('button');
  b.className = 'alt small-btn';
  b.textContent = 'Check with Python';
  const out = document.createElement('span');
  out.className = 'chk-out small';
  fig.foot.append(b, out);
  b.addEventListener('click', async () => {
    b.disabled = true; out.textContent = ' running the Python code...'; out.className = 'chk-out small mute';
    try {
      const p = params(), r = await api(`/python/${name}`, { body: p });
      const d = diff(jsCompute(name, p, data), r.result, { rtol: 1e-8, atol: 1e-9 });
      out.className = `chk-out small ${d ? 'err' : 'ok'}`;
      out.textContent = d ? ` differs at ${d.path}: JS ${d.js} vs Python ${d.python}` : ` identical to ${name}() in Python`;
    } catch (e) { out.className = 'chk-out small err'; out.textContent = ' ' + e.message; }
    b.disabled = false;
  });
}
