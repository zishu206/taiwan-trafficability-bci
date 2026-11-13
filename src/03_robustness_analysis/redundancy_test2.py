# -*- coding: utf-8 -*-
import numpy as np
import rasterio
old = r'C:\Users\莫名的wsr\Doubao\chats\2026-11-12\new-chat'
base = np.load(old + r'\bci_full.npy')
mask = np.load(old + r'\west_rmask.npy')
wgt = np.array([0.2335,0.1313,0.0758,0.0426,0.0529,0.0630,0.0153,0.0257,0.1811,0.0906,0.0262,0.0144,0.0476], dtype=np.float64)
with rasterio.open(r'C:\Users\莫名的wsr\Desktop\gee\TaiXi_13indicators_30m.tif') as ds:
    arr = ds.read().astype(np.float32)
m = mask
# 研究区像元矩阵 13×N
X = arr[:, m]
X = np.where(np.isnan(X), 0.0, X)
b0 = base[m].astype(np.float64)
brk = (0.606, 0.672)
def grade_vec(b):
    g = np.zeros(len(b), np.int8); g[(b >= brk[0]) & (b < brk[1])] = 1; g[b >= brk[1]] = 2; return g
def kappa(a, b):
    po = (a == b).mean(); ea = sum((a == k).mean() * (b == k).mean() for k in range(3)); return (po-ea)/(1-ea)
def pearson(a, b):
    ac = a-a.mean(); bc = b-b.mean(); return (ac*bc).sum()/np.sqrt((ac*ac).sum()*(bc*bc).sum())
def spearman_sample(a, b, n=100000, seed=42):
    rng = np.random.default_rng(seed); idx = rng.choice(len(a), n, replace=False)
    ra = np.argsort(np.argsort(a[idx])); rb = np.argsort(np.argsort(b[idx])); return pearson(ra, rb)
g0 = grade_vec(b0)
def run(drop=None, merge=False):
    if merge:
        comp = (X[4] + X[5])/2
        keep = [k for k in range(13) if k not in (4,5)]
        return X[keep].T @ wgt[keep] + comp*(wgt[4]+wgt[5])
    keep = [k for k in range(13) if k != drop]
    w = wgt[keep]/wgt[keep].sum()
    return X[keep].T @ w
for name, b in [('drop_NAI', run(drop=4)), ('drop_NSI', run(drop=5)), ('merged', run(merge=True))]:
    r = pearson(b0, b); rho = spearman_sample(b0, b); mad = np.abs(b0-b).mean()
    g = grade_vec(b); k = kappa(g0, g); chg = (g != g0).mean()
    vals, cnt = np.unique(g, return_counts=True)
    area = {int(v): round(100*c/len(g), 2) for v, c in zip(vals, cnt)}
    print('%-9s r %.4f rho %.4f MAD %.4f Kappa %.4f chg %.4f area %s' % (name, r, rho, mad, k, chg, area))
vals, cnt = np.unique(g0, return_counts=True)
print('baseline area', {int(v): round(100*c/len(g0), 2) for v, c in zip(vals, cnt)})
