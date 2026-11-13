# -*- coding: utf-8 -*-
import numpy as np, rasterio
from rasterio.transform import xy
P = r'C:\Users\莫名的wsr\Desktop\gee\TaiXi_13indicators_30m.tif'
ds = rasterio.open(P)
# 经纬度网格（按行/列中心）
cols = np.arange(ds.width); rows = np.arange(ds.height)
lon = ds.transform.c + (cols + 0.5) * ds.transform.a
lat = ds.transform.f + (rows + 0.5) * ds.transform.e
# 分块读第一波段判断陆地
T = 1024
land = np.zeros((ds.height, ds.width), dtype=bool)
for y in range(0, ds.height, T):
    for x in range(0, ds.width, T):
        w = rasterio.windows.Window(x, y, min(T, ds.width-x), min(T, ds.height-y))
        d = ds.read(window=w)
        land[y:y+w.height, x:x+w.width] = np.isfinite(d).all(axis=0)
# 研究区：陆地 & 经度<=121
west = lon <= 121.0
mask = land & west[None, :]
n = int(mask.sum())
# 像元面积（按纬度近似，m2）
res_deg = abs(ds.transform.a)
# 用每个像元纬度算面积开销大，先整体近似
lat_idx = np.where(mask)[0]
mean_lat = np.mean(lat[lat_idx])
dy = 111320 * res_deg
dx = 111320 * res_deg * np.cos(np.radians(mean_lat))
area = n * dx * dy
print('研究区像元', n, '平均纬度 %.3f' % mean_lat)
print('估算面积 km2 %.1f' % (area/1e6))
np.save(r'C:\Users\莫名的wsr\Doubao\chats\2026-11-12\new-chat\west_mask.npy', mask)
