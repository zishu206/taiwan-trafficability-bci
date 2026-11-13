# -*- coding: utf-8 -*-
import numpy as np
import rasterio
TIF = r'C:\Users\莫名的wsr\Desktop\gee\TaiXi_13indicators_30m.tif'
mask = np.load(r'C:\Users\莫名的wsr\Doubao\chats\2026-11-12\new-chat\west_rmask.npy')
with rasterio.open(TIF) as ds:
    nli = ds.read(1)
    bands = {name: ds.read(bi) for name, bi in [
        ('BD', 2), ('CLAY', 3), ('RELIEF', 5), ('SLOPE', 6), ('WDENS', 9), ('SAR', 10)]}
n = nli[mask]
g6 = mask & (np.abs(nli - 0.32) < 0.01)
g1 = mask & (np.abs(nli - 0.90) < 0.01)
print('G6软土 n=%d  G1硬岩 n=%d' % (g6.sum(), g1.sum()))
for name, arr in bands.items():
    print('%-7s G6均值=%.3f  G1均值=%.3f' % (name, arr[g6].mean(), arr[g1].mean()))
