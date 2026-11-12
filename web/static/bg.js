// Background: a faint phyllotaxis disc (golden angle, as BioMathPatterns.generate_phyllotaxis) that turns slowly;
// drawn once and left still under prefers-reduced-motion.
import { phyllotaxis } from './patterns_engine.js';

export function background(canvas) {
  const ctx = canvas.getContext('2d'), { x, y } = phyllotaxis({ n: 700, alpha: 137.5 });
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let rot = 0;
  const draw = () => {
    const w = canvas.width = innerWidth, h = canvas.height = innerHeight, s = Math.min(w, h) / 70;
    ctx.clearRect(0, 0, w, h);
    const cx = w * 0.82, cy = h * 0.3, c = Math.cos(rot), sn = Math.sin(rot);
    for (let i = 0; i < x.length; i++) {
      ctx.fillStyle = `hsla(${150 + i / 4}, 90%, 60%, ${0.25 + 0.5 * i / x.length})`;
      ctx.beginPath();
      ctx.arc(cx + (x[i] * c - y[i] * sn) * s, cy + (x[i] * sn + y[i] * c) * s, 1 + i / 350, 0, 7);
      ctx.fill();
    }
  };
  draw();
  addEventListener('resize', draw);
  if (!still) setInterval(() => { rot += 0.004; draw(); }, 80);
}
