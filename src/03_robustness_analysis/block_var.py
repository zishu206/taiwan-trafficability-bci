# -*- coding: utf-8 -*-
import numpy as np
import rasterio
old = r'C:\Users\莫名的wsr\Doubao\chats\2026-11-12\new-chat'
mask = np.load(old + r'\west_rmask.npy')
with rasterio.open(r'C:\Users\莫名的wsr\Desktop\gee\TaiXi_13indicators_30m.tif') as ds:
    bd = ds.read(2); clay = ds.read(3); ndvi = ds.read(12); sar = ds.read(10)
# 取一个内部均匀窗口，按9×9切块统计块内标准差
y0, y1, x0, x1 = 3050, 3950, 4800, 5700
def block_cv(band):
    sub = band[y0:y1, x0:x1]
    h = (sub.shape[0]//9)*9; w = (sub.shape[1]//9)*9
    sub = sub[:h, :w]
    blocks = sub.reshape(h//9, 9, w//9, 9)
    within = blocks.var(axis=(1, 3)).mean()
    total = sub.var()
    return np.sqrt(within), np.sqrt(total), round(100*within/total, 2)
for name, band in [('NBD(250m)', bd), ('NCLAY(250m)', clay), ('NDVI(30m)', ndvi), ('SAR(10m->30m)', sar)]:
    sw, st, pct = block_cv(band)
    print('%-13s 块内标准差 %.4f 整体标准差 %.4f 块内方差占比 %s%%' % (name, sw, st, pct))
