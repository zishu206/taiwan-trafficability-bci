# -*- coding: utf-8 -*-
import numpy as np, rasterio
from scipy.ndimage import convolve
wd = r'C:\Users\莫名的wsr\Doubao\chats\2026-11-12\new-chat'
grade = np.load(wd + r'\grade_full.npy')   # 0/1/2, 研究区外 -1
rmask = np.load(wd + r'\west_rmask.npy')
P = r'C:\Users\莫名的wsr\Desktop\gee\TaiXi_13indicators_30m.tif'
ds = rasterio.open(P)
res = abs(ds.transform.a)
yy, xx = np.indices((ds.height, ds.width))
lat = ds.transform.f + (yy + 0.5) * ds.transform.e
cell_area = (111320*res) * (111320*res*np.cos(np.radians(lat)))

kernel = np.ones((3, 3), dtype='int32')
counts = np.zeros((3, ds.height, ds.width), dtype='int32')
for k in range(3):
    binary = ((grade == k) & rmask).astype('int32')
    counts[k] = convolve(binary, kernel, mode='constant', cval=0)
# 众数：窗口内最大计数的等级
new_grade = np.argmax(counts, axis=0).astype('int8')
# 平局处理：若最高计数有并列，保留原等级（保守）
maxc = counts.max(axis=0)
tie = ((counts == maxc[None]).sum(axis=0) > 1)
new_grade[tie] = grade[tie]
# 仅研究区内有效；研究区外置 -1
new_grade[~rmask] = -1

def stats(g, tag):
    m = rmask
    tot = cell_area[m].sum()
    print('---', tag, '总面积 %.0f' % (tot/1e6))
    for k, name in [(0,'Low'),(1,'Medium'),(2,'High')]:
        sel = m & (g == k)
        a = cell_area[sel].sum()
        print('  %s n=%d %.0f km2 %.2f pct' % (name, sel.sum(), a/1e6, 100*a/tot))
stats(grade, '滤波前')
stats(new_grade, '滤波后')
# 像元变化比例
changed = rmask & (new_grade != grade)
print('变化像元 %d (%.2f pct)' % (changed.sum(), 100*changed.sum()/rmask.sum()))
np.save(wd + r'\grade_majority.npy', new_grade)
