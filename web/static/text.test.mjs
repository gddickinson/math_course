// Node test for the tiny markdown renderer and Python highlighter (no DOM needed).
// Run: node web/static/text.test.mjs
import assert from 'node:assert/strict';
import { markdown } from './md.js';
import { highlightPython, codeBlock } from './highlight.js';

const md = markdown('# Title\n\n1. Item one\n   - sub *a* and **b**\n   - `code` <x>\n2. Item two\n\nText [link](https://example.org).');
assert.match(md, /<h2 class="md">Title<\/h2>/);
assert.match(md, /<ol><li>Item one<ul><li>sub <i>a<\/i> and <b>b<\/b><\/li><li><code>code<\/code> &lt;x&gt;<\/li><\/ul><\/li><li>Item two<\/li><\/ol>/);
assert.match(md, /<a href="https:\/\/example.org" target="_blank" rel="noopener">link<\/a>/);
assert.ok(!markdown('<script>x</script>').includes('<script>'));

const h = highlightPython('def f(x):  # say <hi>\n    return "a<b" + 3.5\nclass Tree:\n    pass');
assert.match(h, /<span class="hl-kw">def<\/span> <span class="hl-def">f<\/span>/);
assert.match(h, /<span class="hl-com"># say &lt;hi&gt;<\/span>/);
assert.match(h, /<span class="hl-str">&quot;a&lt;b&quot;<\/span>/);
assert.match(h, /<span class="hl-num">3.5<\/span>/);
assert.match(h, /<span class="hl-def">Tree<\/span>/);
const plain = s => s.replace(/<[^>]+>/g, '').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&amp;/g, '&');
const src = 'x = """doc\nstring"""\nprint(f\'{x}\')  # done';
assert.equal(plain(highlightPython(src)), src, 'highlighting keeps the text');
assert.equal(codeBlock('a\nb').match(/class="ln"/g).length, 2);
console.log('text: markdown + highlighter checks passed');
