"""Minimal CMA-ES (Hansen's (mu/mu_w, lambda) with rank-one + rank-mu update, CSA step size), numpy only, state in JSON.
Coordinates are the knob z in [-1, 1] (0 = base). ask() returns clipped vectors (the evaluated, repaired points); tell() uses
those repaired points (simple bound handling). Minimises -score."""
import json, math
import numpy as np
class CMA:
    def __init__(self, n, x0=None, sigma=0.6, lam=12, seed=0):
        self.n = n; self.lam = lam; self.mu = lam // 2
        w = np.log(self.mu + 0.5) - np.log(np.arange(1, self.mu + 1)); self.w = w / w.sum(); self.mueff = 1.0 / (self.w ** 2).sum()
        self.cc = (4 + self.mueff / n) / (n + 4 + 2 * self.mueff / n); self.cs = (self.mueff + 2) / (n + self.mueff + 5)
        self.c1 = 2 / ((n + 1.3) ** 2 + self.mueff); self.cmu = min(1 - self.c1, 2 * (self.mueff - 2 + 1 / self.mueff) / ((n + 2) ** 2 + self.mueff))
        self.damps = 1 + 2 * max(0, math.sqrt((self.mueff - 1) / (n + 1)) - 1) + self.cs; self.chiN = math.sqrt(n) * (1 - 1 / (4 * n) + 1 / (21 * n * n))
        self.m = np.zeros(n) if x0 is None else np.array(x0, float); self.sigma = sigma
        self.C = np.eye(n); self.pc = np.zeros(n); self.ps = np.zeros(n); self.g = 0; self.seed = seed
    def _eig(self):
        C = (self.C + self.C.T) / 2; d, B = np.linalg.eigh(C); d = np.sqrt(np.maximum(d, 1e-20)); return B, d
    def ask(self):
        rng = np.random.default_rng(self.seed * 100003 + self.g); B, d = self._eig()
        X = [self.m + self.sigma * (B @ (d * rng.standard_normal(self.n))) for _ in range(self.lam)]
        return [np.clip(x, -1, 1) for x in X]
    def tell(self, X, f):
        """X: evaluated points, f: values to MINIMISE (same order)."""
        X = np.array(X); idx = np.argsort(f)[:self.mu]; old = self.m.copy()
        self.m = (self.w[:, None] * X[idx]).sum(0)
        B, d = self._eig(); invsq = B @ np.diag(1 / d) @ B.T; y = (self.m - old) / self.sigma
        self.ps = (1 - self.cs) * self.ps + math.sqrt(self.cs * (2 - self.cs) * self.mueff) * (invsq @ y)
        hs = np.linalg.norm(self.ps) / math.sqrt(1 - (1 - self.cs) ** (2 * (self.g + 1))) / self.chiN < 1.4 + 2 / (self.n + 1)
        self.pc = (1 - self.cc) * self.pc + hs * math.sqrt(self.cc * (2 - self.cc) * self.mueff) * y
        Y = (X[idx] - old) / self.sigma
        self.C = (1 - self.c1 - self.cmu) * self.C + self.c1 * (np.outer(self.pc, self.pc) + (1 - hs) * self.cc * (2 - self.cc) * self.C) \
                 + self.cmu * (self.w[:, None, None] * np.einsum('ki,kj->kij', Y, Y)).sum(0)
        self.sigma *= math.exp((self.cs / self.damps) * (np.linalg.norm(self.ps) / self.chiN - 1)); self.sigma = min(self.sigma, 1.0)
        self.g += 1
    def save(self, f):
        json.dump({k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in self.__dict__.items()}, open(f, 'w'))
    @classmethod
    def load(cls, f):
        s = json.load(open(f)); o = cls.__new__(cls)
        for k, v in s.items(): setattr(o, k, np.array(v) if isinstance(v, list) else v)
        return o
if __name__ == '__main__':   # self-test on a shifted sphere
    c = CMA(20, sigma=0.6, lam=12)
    for g in range(60):
        X = c.ask(); c.tell(X, [float(((x - 0.3) ** 2).sum()) for x in X])
    print('m', np.round(c.m[:5], 3), 'sigma', round(c.sigma, 4))
