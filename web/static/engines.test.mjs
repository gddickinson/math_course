// Node test: every JS engine must reproduce the course scripts' Python results stored in
// tests/fixtures/course_fixture.json (written by scripts/make_course_fixture.py from web/compute.py).
// Run: node web/static/engines.test.mjs
import { readFileSync } from 'node:fs';
import assert from 'node:assert/strict';
import { REGISTRY, jsCompute, diff } from './js_compute.js';
import { PyRandom, NpRandom } from './pyrandom.js';
import { tPpf, betainc } from './stats_engine.js';

const fx = JSON.parse(readFileSync(new URL('../../tests/fixtures/course_fixture.json', import.meta.url)));
// statistics (incomplete beta, t quantiles) are computed differently from scipy: agree to ~1e-12, test at 1e-8
const TOL = { tree_stats: { rtol: 1e-8, atol: 1e-10 }, tree_compare: { rtol: 1e-8, atol: 1e-10 },
  shell_stats: { rtol: 1e-8, atol: 1e-10 } };

let checks = 0;
for (const [name, cases] of Object.entries(fx.cases)) {
  assert.ok(REGISTRY[name], `no JS engine for ${name}`);
  for (const { params, result } of cases) {
    const d = diff(jsCompute(name, params, fx.data), result, TOL[name]);
    assert.equal(d, null, `${name} ${JSON.stringify(params).slice(0, 80)}: ${JSON.stringify(d)}`);
    checks++;
  }
}
assert.deepEqual(Object.keys(REGISTRY).sort(), Object.keys(fx.cases).sort(), 'every engine has fixture cases');

// known values: CPython random.seed(1); random.random() and numpy np.random.seed(0); random_sample()
assert.equal(new PyRandom(1).random(), 0.13436424411240122);
assert.equal(new NpRandom(0).random(), 0.5488135039273248);
assert.ok(Math.abs(tPpf(0.975, 19) - 2.093024054408263) < 1e-12);
assert.ok(Math.abs(betainc(2, 3, 0.4) - 0.5248) < 1e-12);
checks += 4;
console.log(`engines: ${checks} checks passed`);
