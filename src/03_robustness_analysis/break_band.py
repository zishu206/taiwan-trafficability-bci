# -*- coding: utf-8 -*-
import numpy as np
old = r'C:\Users\莫名的wsr\Doubao\chats\2026-11-12\new-chat'
bci = np.load(old + r'\bci_full.npy')
mask = np.load(old + r'\west_rmask.npy')
b = bci[mask]
n = len(b)
for d in [0.005, 0.01, 0.02]:
    near1 = (np.abs(b - 0.606) < d)
    near2 = (np.abs(b - 0.672) < d)
    either = near1 | near2
    print('±%.3f: 断点1带 %5.2f%%  断点2带 %5.2f%%  合计 %5.2f%%' % (d, 100*near1.mean(), 100*near2.mean(), 100*either.mean()))
# 各等级像元到最近断点的距离分布（衡量分级稳健性）
print('BCI在两断点之间(中区)占比 %.2f%%' % (100*((b>=0.606)&(b<0.672)).mean()))
# 距离最近断点小于0.02的像元，即高敏感分级像元
dist = np.minimum(np.abs(b-0.606), np.abs(b-0.672))
print('距最近断点<0.02的像元（分级高敏感） %.2f%%' % (100*(dist<0.02).mean()))
