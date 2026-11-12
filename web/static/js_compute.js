// The browser's counterpart of web/compute.py: the same function names and parameters, answered by the JS engines.
// Used by the lesson figures ("Check with Python" compares jsCompute(name, p) with POST /api/python/<name>) and by
// engines.test.mjs, which replays every case of tests/fixtures/course_fixture.json.
import { numerals, egyptianMultiply, babylonianSqrt } from './numerals_engine.js';
import { gcd, diophantine, primes, dnaLength, cicada, geneticSequences } from './numtheory_engine.js';
import { phyllotaxis, geneLengths, sequenceLength } from './patterns_engine.js';
import { tree, shellSpiral, population, shell3d } from './growth_engine.js';
import { advancedTree } from './tree_engine.js';
import { treeStats, treeCompare, shellStats } from './stats_engine.js';
import { sequence, ip3r } from './sequence_engine.js';

// `data` is the /api/data payload (class tables from the scripts).
export const REGISTRY = {
  numerals, egyptian_multiply: egyptianMultiply, babylonian_sqrt: babylonianSqrt, gcd, diophantine, primes,
  dna_length: dnaLength, cicada, genetic_sequences: geneticSequences, phyllotaxis, gene_lengths: geneLengths,
  sequence_length: sequenceLength, tree, shell_spiral: shellSpiral, population,
  advanced_tree: (p, d) => advancedTree(p, { species: d.tree_species, seasons: d.seasons }),
  tree_stats: (p, d) => treeStats(p, d.tree_data), tree_compare: (p, d) => treeCompare(p, d.tree_data),
  shell3d: (p, d) => shell3d(p, d.shell_species), shell_stats: (p, d) => shellStats(p, d.shell_data),
  sequence, ip3r,
};

export function jsCompute(name, params, data) { return REGISTRY[name](params, data); }

// Compare two JSON-like values; numbers within atol + rtol * |b|. Returns null when equal, else the first difference.
export function diff(a, b, { rtol = 1e-9, atol = 1e-9 } = {}, path = '') {
  if (typeof a === 'number' && typeof b === 'number') {
    if (Number.isNaN(a) && Number.isNaN(b)) return null;
    return Math.abs(a - b) <= atol + rtol * Math.abs(b) ? null : { path, js: a, python: b };
  }
  if (Array.isArray(a) || Array.isArray(b)) {
    if (!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length) {
      return { path, js: Array.isArray(a) ? `array(${a.length})` : a, python: Array.isArray(b) ? `array(${b.length})` : b };
    }
    for (let i = 0; i < a.length; i++) { const d = diff(a[i], b[i], { rtol, atol }, `${path}[${i}]`); if (d) return d; }
    return null;
  }
  if (a && b && typeof a === 'object' && typeof b === 'object') {
    const ka = Object.keys(a).sort(), kb = Object.keys(b).sort();
    if (ka.join() !== kb.join()) return { path, js: ka.join(','), python: kb.join(',') };
    for (const k of ka) { const d = diff(a[k], b[k], { rtol, atol }, `${path}.${k}`); if (d) return d; }
    return null;
  }
  return a === b ? null : { path, js: a, python: b };
}
