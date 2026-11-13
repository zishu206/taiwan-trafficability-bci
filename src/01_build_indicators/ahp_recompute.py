# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

RI = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12}

def ahp(M):
    M = np.asarray(M, float)
    n = M.shape[0]
    gm = np.prod(M, axis=1) ** (1 / n)
    w = gm / gm.sum()
    lam = np.mean((M @ w) / w)
    ci = (lam - n) / (n - 1) if n > 2 else 0.0
    cr = ci / RI[n] if RI[n] > 0 else 0.0
    return w, lam, ci, cr

# 原 B3 4x4（NWDI, NSHI, NTWI, NSAR）
B3_old = [[1, 1/2, 1, 2],
          [2, 1, 2, 4],
          [1, 1/2, 1, 3],
          [1/2, 1/4, 1/3, 1]]
# 新 B3 2x2（NWDI, NSAR）：NWDI 对 NSAR 为 2
B3_new = [[1, 2], [1/2, 1]]
w3, lam3, ci3, cr3 = ahp(B3_new)

# 其余组（沿用原文）
B1 = [[1, 2, 3, 5], [1/2, 1, 2, 3], [1/3, 1/2, 1, 2], [1/5, 1/3, 1/2, 1]]
B2 = [[1, 1, 3, 2], [1, 1, 4, 3], [1/3, 1/4, 1, 1/2], [1/2, 1/3, 2, 1]]
B4 = [[1, 2, 1/2], [1/2, 1, 1/3], [2, 3, 1]]
w1, l1, _, c1 = ahp(B1)
w2, l2, _, c2 = ahp(B2)
w4, l4, _, c4 = ahp(B4)

# 组间
BG = [[1, 3, 2, 5], [1/3, 1, 1/2, 2], [1/2, 2, 1, 3], [1/5, 1/2, 1/3, 1]]
wg, lg, _, cg = ahp(BG)

groups = [
    ('B1', ['NLI','NBD','NCLAY','NSAL'], w1),
    ('B2', ['NAI','NSI','NCUR','NDW'], w2),
    ('B3', ['NWDI','NSAR'], w3),
    ('B4', ['NLST','NVFI','NLULC'], w4),
]
out = []
out.append('B3 new local weights: NWDI=%.4f NSAR=%.4f lambda=%.4f CR=%.4f'
           % (w3[0], w3[1], lam3, cr3))
out.append('group weights: B1=%.4f B2=%.4f B3=%.4f B4=%.4f' % tuple(wg))
out.append('')
rows = []
for gi, (gname, names, w) in enumerate(groups):
    gw = wg[gi]
    for nm, lw in zip(names, w):
        rows.append((nm, gw * lw))
total = sum(r[1] for r in rows)
order = sorted(rows, key=lambda x: -x[1])
rank = {nm: i + 1 for i, (nm, _) in enumerate(order)}
for nm, val in rows:
    out.append('%-6s global=%.4f rank=%d' % (nm, val, rank[nm]))
out.append('sum=%.4f  count=%d' % (total, len(rows)))
out.append('')
out.append('CR: group=%.4f B1=%.4f B2=%.4f B3=%.4f B4=%.4f'
           % (cg, c1, c2, cr3, c4))
p = r'C:\Users\莫名的wsr\Desktop\gee\ahp_recompute_report.txt'
open(p, 'w', encoding='utf-8').write('\n'.join(out))
print('done')
