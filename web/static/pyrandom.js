// Python-compatible random numbers (MT19937), so a seed in the browser gives the same run as the Python scripts:
//  - PyRandom: the standard library's random.seed(int) / random.random() / random.uniform(a, b)
//  - NpRandom: numpy's legacy np.random.seed(int) / random_sample() / normal(loc, scale) (polar Box-Muller with cache)
// Based on the mt19937.js port used in George's organic-growth-patterns site.

const N = 624, M = 397;

class MT {
  constructor() { this.mt = new Uint32Array(N); this.idx = N + 1; }
  initGenrand(s) {
    const mt = this.mt;
    mt[0] = s >>> 0;
    for (let i = 1; i < N; i++) mt[i] = (Math.imul(1812433253, mt[i - 1] ^ (mt[i - 1] >>> 30)) + i) >>> 0;
    this.idx = N;
  }
  // init_by_array() from the reference MT code, as CPython's random.seed() uses it.
  initByArray(key) {
    this.initGenrand(19650218);
    const mt = this.mt;
    let i = 1, j = 0;
    for (let k = Math.max(N, key.length); k; k--) {
      mt[i] = ((mt[i] ^ Math.imul(mt[i - 1] ^ (mt[i - 1] >>> 30), 1664525)) + key[j] + j) >>> 0;
      i++; j++;
      if (i >= N) { mt[0] = mt[N - 1]; i = 1; }
      if (j >= key.length) j = 0;
    }
    for (let k = N - 1; k; k--) {
      mt[i] = ((mt[i] ^ Math.imul(mt[i - 1] ^ (mt[i - 1] >>> 30), 1566083941)) - i) >>> 0;
      i++;
      if (i >= N) { mt[0] = mt[N - 1]; i = 1; }
    }
    mt[0] = 0x80000000;
    this.idx = N;
  }
  twist() {
    const mt = this.mt;
    for (let i = 0; i < N; i++) {
      const y = (mt[i] & 0x80000000) | (mt[(i + 1) % N] & 0x7fffffff);
      let v = mt[(i + M) % N] ^ (y >>> 1);
      if (y & 1) v ^= 0x9908b0df;
      mt[i] = v >>> 0;
    }
    this.idx = 0;
  }
  next32() {
    if (this.idx >= N) this.twist();
    let y = this.mt[this.idx++];
    y ^= y >>> 11; y ^= (y << 7) & 0x9d2c5680; y ^= (y << 15) & 0xefc60000; y ^= y >>> 18;
    return y >>> 0;
  }
  random() { const a = this.next32() >>> 5, b = this.next32() >>> 6; return (a * 67108864 + b) / 9007199254740992; }
}

export class PyRandom extends MT {
  constructor(seed = 0) { super(); this.seed(seed); }
  // random.seed(int): the absolute value split into 32-bit words, least significant first.
  seed(s) {
    let n = BigInt(Math.abs(s));
    const key = [];
    do { key.push(Number(n & 0xffffffffn)); n >>= 32n; } while (n > 0n);
    this.initByArray(key);
  }
  uniform(a, b) { return a + (b - a) * this.random(); }
}

export class NpRandom extends MT {
  constructor(seed = 0) { super(); this.seed(seed); }
  seed(s) { this.initGenrand(s); this.gauss = null; }
  gaussian() {
    if (this.gauss !== null) { const g = this.gauss; this.gauss = null; return g; }
    let x1, x2, r2;
    do { x1 = 2 * this.random() - 1; x2 = 2 * this.random() - 1; r2 = x1 * x1 + x2 * x2; } while (r2 >= 1 || r2 === 0);
    const f = Math.sqrt(-2 * Math.log(r2) / r2);
    this.gauss = f * x1;
    return f * x2;
  }
  normal(loc, scale, n) { return Array.from({ length: n }, () => loc + scale * this.gaussian()); }
}
