# -*- coding: utf-8 -*-
"""
阶段2：15 指标 Pearson 相关矩阵 + p 值 + VIF 共线性检验（修正版）
修正点：
  1) 有效像元 = 所有波段 finite 且 非全0（排除研究区外 0/NaN 填充）；
  2) NLI 当前为 0.5 常数占位、无变异，不参与相关与 VIF，对其余 14 个真实指标计算。
"""
import os
import numpy as np
import pandas as pd
import rasterio
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor

TIF = r'C:\Users\莫名的wsr\Desktop\gee\TaiXi_15indicators_30m_merged.tif'
OUTDIR = r'C:\Users\莫名的wsr\Desktop\gee\collinearity'
os.makedirs(OUTDIR, exist_ok=True)
N_SAMPLE = 30000
STEP = 10
SEED = 42
DROP = ['NLI']  # 常数占位，暂不参与统计

# ---------- 1. 分块读取，收集真实陆地像元 ----------
rows = []
with rasterio.open(TIF) as src:
    all_bands = list(src.descriptions)
    n = src.count
    for ji, window in src.block_windows(1):
        data = src.read(window=window)
        wh, ww = window.height, window.width
        finite = np.all(np.isfinite(data), axis=0)
        nonzero = np.any(np.abs(data) > 1e-9, axis=0)
        valid = finite & nonzero
        for yy in range(0, wh, STEP):
            for xx in range(0, ww, STEP):
                if valid[yy, xx]:
                    rows.append(data[:, yy, xx])
print('规则抽稀得到真实陆地像元:', len(rows), flush=True)
allpts = np.asarray(rows, dtype=np.float64)

rng = np.random.default_rng(SEED)
if allpts.shape[0] > N_SAMPLE:
    allpts = allpts[rng.choice(allpts.shape[0], N_SAMPLE, replace=False)]
print('最终样本数:', allpts.shape[0], flush=True)
df = pd.DataFrame(allpts, columns=all_bands)

# ---------- 2. 剔除常数占位 NLI ----------
dfa = df.drop(columns=DROP)
bands = list(dfa.columns)
n = len(bands)
print('参与检验指标 (%d):' % n, bands, flush=True)

# ---------- 3. Pearson 相关与 p 值 ----------
corr = dfa.corr(method='pearson')
pmat = pd.DataFrame(np.ones((n, n)), index=bands, columns=bands)
for i in range(n):
    for j in range(i + 1, n):
        r, p = stats.pearsonr(dfa.iloc[:, i], dfa.iloc[:, j])
        pmat.iloc[i, j] = p
        pmat.iloc[j, i] = p

# ---------- 4. VIF ----------
X = dfa.values
vif_vals = [variance_inflation_factor(X, i) for i in range(n)]
vif = pd.DataFrame({'indicator': bands, 'VIF': vif_vals})

# ---------- 5. 保存 ----------
corr.to_csv(os.path.join(OUTDIR, 'pearson_correlation.csv'),
            float_format='%.4f', encoding='utf-8-sig')
pmat.to_csv(os.path.join(OUTDIR, 'pearson_pvalues.csv'),
            float_format='%.4e', encoding='utf-8-sig')
vif.to_csv(os.path.join(OUTDIR, 'vif.csv'), index=False,
           float_format='%.4f', encoding='utf-8-sig')

# ---------- 6. 热力图 ----------
fig, ax = plt.subplots(figsize=(10.5, 9))
im = ax.imshow(corr.values, cmap='RdBu_r', vmin=-1, vmax=1)
ax.set_xticks(range(n)); ax.set_xticklabels(bands, rotation=45, ha='right')
ax.set_yticks(range(n)); ax.set_yticklabels(bands)
for i in range(n):
    for j in range(n):
        ax.text(j, i, '%.2f' % corr.values[i, j], ha='center', va='center',
                color='white' if abs(corr.values[i, j]) > 0.55 else 'black',
                fontsize=8)
cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label('Pearson r')
ax.set_title('Pearson correlation matrix of 14 indicators (n=%d)' % dfa.shape[0])
plt.tight_layout()
fig.savefig(os.path.join(OUTDIR, 'pearson_heatmap.png'), dpi=300)
plt.close(fig)

# ---------- 7. 结论 ----------
lines = ['说明：NLI 为 0.5 常数占位、无变异，暂不参与相关与 VIF；以下为 14 个真实指标。',
         '样本数 n = %d（随机种子 %d，规则抽稀后随机采样）' % (dfa.shape[0], SEED), '',
         '高相关指标对 (|r| >= 0.80):']
pairs = [(bands[i], bands[j], corr.values[i, j], pmat.values[i, j])
         for i in range(n) for j in range(i + 1, n) if abs(corr.values[i, j]) >= 0.80]
lines += (['  %s - %s : r=%.3f, p=%.2e' % (a, b, r, p) for a, b, r, p in pairs]
          if pairs else ['  无'])
lines.append('')
lines.append('中等相关对 (0.60 <= |r| < 0.80):')
mid = [(bands[i], bands[j], corr.values[i, j])
       for i in range(n) for j in range(i + 1, n)
       if 0.60 <= abs(corr.values[i, j]) < 0.80]
lines += (['  %s - %s : r=%.3f' % (a, b, r) for a, b, r in mid]
          if mid else ['  无'])
lines += ['', '方差膨胀因子 VIF:']
for _, rr in vif.iterrows():
    flag = '  <-- 严重共线性(>10)' if rr.VIF > 10 else ('  <-- 关注(>5)' if rr.VIF > 5 else '')
    lines.append('  %-5s %.3f%s' % (rr.indicator, rr.VIF, flag))
with open(os.path.join(OUTDIR, 'conclusion.txt'), 'w', encoding='utf-8') as fp:
    fp.write('\n'.join(lines))
print('ALL DONE ->', OUTDIR, flush=True)
