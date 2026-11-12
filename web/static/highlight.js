// Tiny Python syntax highlighter: one regex pass that wraps comments, strings, numbers, keywords, builtins, decorators
// and def/class names in <span class="hl-..."> (colours in style_app.css). Everything else is escaped text.
import { esc } from './core.js';

const KW = 'False None True and as assert async await break class continue def del elif else except finally for from '
  + 'global if import in is lambda nonlocal not or pass raise return try while with yield';
const BI = 'abs all any bool dict enumerate float int isinstance len list map max min print range round set sorted str sum '
  + 'super tuple type zip self';
const RE = new RegExp([
  '(#[^\\n]*)',                                                         // 1 comment
  '((?:[rbfRBF]{1,2})?(?:"""[\\s\\S]*?"""|\'\'\'[\\s\\S]*?\'\'\'|"(?:\\\\.|[^"\\\\\\n])*"|\'(?:\\\\.|[^\'\\\\\\n])*\'))', // 2 string
  '(@[\\w.]+)',                                                         // 3 decorator
  '\\b(\\d+(?:\\.\\d*)?(?:[eE][+-]?\\d+)?j?|0x[\\da-fA-F]+)\\b',          // 4 number
  `\\b(${KW.split(' ').join('|')})\\b`,                                  // 5 keyword
  `\\b(${BI.split(' ').join('|')})\\b`,                                  // 6 builtin
].join('|'), 'g');

export function highlightPython(code) {
  let out = '', last = 0, defNext = false;
  for (const m of code.matchAll(RE)) {
    let plain = code.slice(last, m.index);
    if (defNext) {     // the identifier after def/class
      plain = esc(plain).replace(/^(\s*)([A-Za-z_]\w*)/, '$1<span class="hl-def">$2</span>');
      defNext = false;
    } else plain = esc(plain);
    out += plain;
    const [t] = m, cls = m[1] ? 'com' : m[2] ? 'str' : m[3] ? 'dec' : m[4] ? 'num' : m[5] ? 'kw' : 'bi';
    out += `<span class="hl-${cls}">${esc(t)}</span>`;
    if (m[5] === 'def' || m[5] === 'class') defNext = true;
    last = m.index + t.length;
  }
  let tail = code.slice(last);
  tail = defNext ? esc(tail).replace(/^(\s*)([A-Za-z_]\w*)/, '$1<span class="hl-def">$2</span>') : esc(tail);
  return out + tail;
}

// Code block with line numbers (as a gutter) for a whole file.
export function codeBlock(code) {
  const lines = highlightPython(code.replace(/\s+$/, '')).split('\n');
  return `<pre class="code"><code>${lines.map((l, i) => `<span class="ln" aria-hidden="true">${i + 1}</span>${l}`).join('\n')}</code></pre>`;
}
