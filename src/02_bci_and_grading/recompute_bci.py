# -*- coding: utf-8 -*-
import numpy as np, rasterio
from rasterio.windows import Window
SRC = r'C:\Users\莫名的wsr\Desktop\gee\TaiXi_13indicators_30m.tif'
OUT = r'C:\Users\莫名的wsr\Doubao\chats\2026-11-12\new-chat\BCI_recomputed.tif'
# 波段顺序: NLI,NBD,NCLAY,NSAL,NAI,NSI,NCUR,NDW,NWDI,NSAR,NLST,NVFI,NLULC
w = np.array([0.2335,0.1313,0.0758,0.0426,0.0529,0.0630,0.0153,0.0257,
              0.1811,0.0906,0.0262,0.0144,0.0476], dtype='float32')
T = 512
with rasterio.open(SRC) as src:
    meta = src.meta.copy()
    meta.update(count=2, compress='lzw', tiled=True, blockxsize=T, blockyysize=T,
                BIGTIFF='YES', interleave='pixel', descriptions=('BCI','grade'))
    counts = np.zeros(3, dtype='int64')
    total_valid = 0
    with rasterio.open(OUT, 'w', **meta) as dst:
        for y in range(0, src.height, T):
            for x in range(0, src.width, T):
                win = Window(x, y, min(T, src.width-x), min(T, src.height-y))
                d = src.read(window=win)  # 13,h,w
                valid = np.isfinite(d).all(axis=0)
                bci = np.where(valid, np.tensordot(w, d, axes=1), np.nan).astype('float32')
                grade = np.full(bci.shape, -1, dtype='float32')
                grade[valid & (bci < 0.606)] = 0
                grade[valid & (bci >= 0.606) & (bci < 0.672)] = 1
                grade[valid & (bci >= 0.672)] = 2
                for k in range(3):
                    counts[k] += int(((grade == k) & valid).sum())
                total_valid += int(valid.sum())
                dst.write(bci, 1, window=win)
                dst.write(grade, 2, window=win)
print('valid', total_valid)
print('grade counts (I low, II med, III high):', counts)
print('proportions %:', np.round(100*counts/counts.sum(), 2))
