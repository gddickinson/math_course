// Port of advanced_tree_patterns.py (AdvancedTreeModel.generate_tree): binary branching whose length depends on the
// season, light exposure and nutrients, with random angle variation from Python's random.uniform (PyRandom), so a
// seed gives the same tree as `random.seed(seed)` before calling the Python method.
import { PyRandom } from './pyrandom.js';

const rad = d => d * Math.PI / 180;

// AdvancedTreeModel.calculate_environmental_factor(): light falls with depth and with the angle away from the light.
export function lightFactor(depth, angle, light, maxDepth) {
  return Math.max(0.1, Math.cos(rad(Math.abs(angle - light))) * (1 - depth / maxDepth));
}

// Returns segments [x0, y0, x1, y1, depth, thickness, health, light_exposure(end), nutrient_level(end)]
// in the Python list order. `species` and `seasons` are the class tables (from /api/data).
export function advancedTree({ species, season, light_direction, nutrient_level, stress, seed }, { species: sp, seasons }) {
  const P = sp[species], S = seasons[season], rnd = new PyRandom(seed), out = [];
  const grow = node => {
    if (node.depth >= P.max_depth || node.health < 0.1) return;
    const light = node.light * P.light_sensitivity, nut = node.nutrient * P.nutrient_sensitivity;
    const g = S.growth_modifier * light * nut;
    const len = node.length * P.length_decay * g, thick = node.thickness * P.thickness_decay;
    const v = P.branching_variation * (1 + stress);
    const angles = [node.angle + P.base_angle * (1 + rnd.uniform(-v, v)),
      node.angle - P.base_angle * (1 + rnd.uniform(-v, v))];
    for (const a of angles) {
      const child = { x: node.x + len * Math.cos(rad(a)), y: node.y + len * Math.sin(rad(a)), angle: a, length: len,
        depth: node.depth + 1, thickness: thick, health: node.health * S.health_modifier,
        light: lightFactor(node.depth + 1, a, light_direction, P.max_depth), nutrient: node.nutrient * 0.9 };
      out.push([node.x, node.y, child.x, child.y, node.depth, node.thickness, node.health, child.light, child.nutrient]);
      grow(child);
    }
  };
  grow({ x: 0, y: 0, angle: 90, length: 1, depth: 0, thickness: 0.2, health: 1, light: 1, nutrient: nutrient_level });
  return out;
}
