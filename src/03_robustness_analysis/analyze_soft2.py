# -*- coding: utf-8 -*-
import numpy as np
import rasterio
old = r'C:\Users\莫名的wsr\Doubao\chats\2026-11-12\new-chat'
wr = np.load(old + r'\west_rmask.npy')
bci = np.load(old + r'\bci_full.npy')
names = ['NLI','BD','CLAY','SAL','RELIEF','SLOPE','CURV','DISTW','WDENS','SAR','LST','NDVI','LULC']
wgt = np.array([0.2335,0.1313,0.0758,0.0426,0.0529,0.0630,0.0153,0.0257,0.1811,0.0906,0.0262,0.0144,0.0476])
with rasterio.open(r'C:\Users\莫名的wsr\Desktop\gee\TaiXi_13indicators_30m.tif') as ds:
    arr = ds.read()  # 13,H,W
g6 = wr & (np.abs(arr[0] - 0.32) < 0.01)
print('G6各指标均值（归一化0-1）与加权贡献:')
contrib = np.zeros(13)
for k in range(13):
    band = arr[k]
    m = np.nanmean(band[g6])
    contrib[k] = m * wgt[k]
    print('%-7s weight %.4f  mean %.3f  contrib %.4f' % (names[k], wgt[k], m, contrib[k]))
print('加权贡献和（=BCI均值）', round(contrib.sum(), 4))
# 全区各指标均值对照
print('全研究区各指标均值:')
for k in range(13):
    print('%-7s %.3f' % (names[k], np.nanmean(arr[k][wr])))
# 均值回归：G6的NLI贡献 vs 其余指标贡献
print('G6 NLI贡献 %.4f，其余12项贡献和 %.4f' % (contrib[0], contrib[1:].sum()))
# 仅NLI判定的软土占比 vs BCI低区
print('G6占研究区 %.2f%%，但G6中仅 %.2f%% 落入Low区' % (100*g6.sum()/wr.sum(), 20.85))
