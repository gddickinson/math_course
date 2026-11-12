// Tiny markdown renderer for the README text: headings, nested bullet / numbered lists, fenced code, paragraphs,
// **bold**, *italic*, `code` and [links](url). HTML in the source is escaped. No external library.
import { esc } from './core.js';

export function inline(s) {
  return esc(s)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<b>$1</b>')
    .replace(/(^|[^*])\*([^*\s][^*]*)\*/g, '$1<i>$2</i>')
    .replace(/\[([^\]]+)\]\((https?:[^)\s]+|#[^)\s]*)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
}

const LIST = /^(\s*)([-*]|\d+\.) (.*)$/;

function renderList(lines, i) {
  const base = lines[i].match(LIST)[1].length, ordered = /\d/.test(lines[i].match(LIST)[2]);
  const items = [];
  while (i < lines.length) {
    const m = lines[i].match(LIST);
    if (!m || m[1].length < base) break;
    if (m[1].length > base) { const [html, j] = renderList(lines, i); items[items.length - 1] += html; i = j; continue; }
    items.push(inline(m[3])); i++;
  }
  const tag = ordered ? 'ol' : 'ul';
  return [`<${tag}>${items.map(t => `<li>${t}</li>`).join('')}</${tag}>`, i];
}

export function markdown(src) {
  const lines = String(src || '').replace(/\r/g, '').split('\n'), out = [];
  let i = 0, para = [];
  const flush = () => { if (para.length) out.push(`<p>${inline(para.join(' '))}</p>`); para = []; };
  while (i < lines.length) {
    const ln = lines[i];
    if (/^```/.test(ln)) {
      flush();
      const code = [];
      for (i++; i < lines.length && !/^```/.test(lines[i]); i++) code.push(lines[i]);
      out.push(`<pre>${esc(code.join('\n'))}</pre>`); i++; continue;
    }
    const h = ln.match(/^(#{1,4}) (.*)$/);
    if (h) { flush(); const n = Math.min(4, h[1].length + 1); out.push(`<h${n} class="md">${inline(h[2])}</h${n}>`); i++; continue; }
    if (LIST.test(ln)) { flush(); const [html, j] = renderList(lines, i); out.push(html); i = j; continue; }
    if (/^\s*(---+|\*\*\*+)\s*$/.test(ln)) { flush(); out.push('<hr>'); i++; continue; }
    if (!ln.trim()) { flush(); i++; continue; }
    para.push(ln.trim()); i++;
  }
  flush();
  return `<div class="md">${out.join('\n')}</div>`;
}
