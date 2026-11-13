# -*- coding: utf-8 -*-
import numpy as np
import rasterio
TIF = r'C:\Users\莫名的wsr\Desktop\gee\TaiXi_13indicators_30m.tif'
bci = np.load(r'C:\Users\莫名的wsr\Doubao\chats\2026-11-12\new-chat\bci_full.npy')
mask = np.load(r'C:\Users\莫名的wsr\Doubao\chats\2026-11-12\new-chat\west_rmask.npy')
with rasterio.open(TIF) as ds:
    nli = ds.read(1); clay = ds.read(3); relief = ds.read(5); slope = ds.read(6)
# 饱和脆弱系数：平坦、平缓、黏土高、软土(NLI低)
S = np.clip((relief + slope + clay + (1.0 - nli)) / 4.0, 0, 1, dtype='float32')
Ss = S[mask]
print('脆弱系数S 中位=%.3f 90分位=%.3f' % (np.median(Ss), np.percentile(Ss, 90)))
b = bci[mask]
dry_grade = np.digitize(b, [0.606, 0.672])  # 0 Low,1 Medium,2 High
for delta in [0.03, 0.05, 0.08]:
    wet = b - delta * Ss
    drop = delta * Ss
    wet_grade = np.digitize(wet, [0.606, 0.672])
    trans = np.mean(wet_grade < dry_grade)
    down1 = np.mean((dry_grade - wet_grade) == 1)
    down2 = np.mean((dry_grade - wet_grade) >= 2)
    print('Delta=%.2f | BCI下降 中位=%.4f 90分位=%.4f | 降级像元=%.2f%% (降1级%.2f%%, 降2级%.2f%%)' % (
        delta, np.median(drop), np.percentile(drop, 90), 100*trans, 100*down1, 100*down2))
    wet_area = [100*np.mean(wet_grade == g) for g in range(3)]
    print('   雨季面积 Low/Med/High = %.2f/%.2f/%.2f' % tuple(wet_area))
dry_area = [100*np.mean(dry_grade == g) for g in range(3)]
print('旱季面积 Low/Med/High = %.2f/%.2f/%.2f' % tuple(dry_area))
np.save(r'C:\Users\莫名的wsr\Doubao\chats\2026-11-13\new-chat\saturate_index.npy', S)
