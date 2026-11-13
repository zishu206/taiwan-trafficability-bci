# -*- coding: utf-8 -*-
import numpy as np
import rasterio
old = r'C:\Users\莫名的wsr\Doubao\chats\2026-11-12\new-chat'
mask = np.load(old + r'\west_rmask.npy')
with rasterio.open(r'C:\Users\莫名的wsr\Desktop\gee\TaiXi_13indicators_30m.tif') as ds:
    bd = ds.read(2); clay = ds.read(3)
    # 像元大小
    px = ds.transform[0]
print('像元度', px)
# 250m 对应多少个 30m 像元
# 该纬度 1度≈101.9km(经度方向乘cos约0.91)；250m对应角度
deg250_lon = 250.0 / (111320 * np.cos(np.radians(23.5)))
deg250_lat = 250.0 / 110540
print('250m约等于 经度%.5f° 纬度%.5f°，即约 %.1f × %.1f 个30m像元' % (deg250_lon, deg250_lat, deg250_lon/px, deg250_lat/px))
for name, band in [('NBD', bd), ('NCLAY', clay)]:
    x = band[mask]
    uniq = np.unique(x[~np.isnan(x)])
    print('%-6s 研究区像元 %d，独立值 %d，平均每独立值对应 %.1f 像元' % (name, len(x), len(uniq), len(x)/len(uniq)))
# 检查8×8块内是否重复（最近邻特征）：取一个内部区域，看水平方向相邻相等run长度
def runlen(v):
    changes = np.where(np.diff(v) != 0)[0]
    starts = np.r_[0, changes+1]
    return np.diff(np.r_[starts, len(v)])
row = 6000
seg = bd[row, 2000:3000]
rl = runlen(seg)
print('NBD水平段长度（前20）', rl[:20])
print('NBD段长中位数', np.median(rl))
# 权重占比
print('NBD+NCLAY权重和', round(0.1313+0.0758, 4))
