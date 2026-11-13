# -*- coding: utf-8 -*-
import os
import numpy as np
import rasterio
from scipy import stats

TIF = r'C:\Users\莫名的wsr\Desktop\gee\TaiXi_15indicators_30m_merged.tif'
OUT = r'C:\Users\莫名的wsr\Desktop\gee\full_qa_report.txt'
DROP = ['NDWI', 'TWI']
lines = []
with rasterio.open(TIF) as src:
    bands = list(src.descriptions)
    lines.append('%-6s %-7s %6s %6s %6s %6s %6s %7s %7s %s'
                 % ('band', 'keep?', 'valid%', 'min', 'p25', 'median', 'p75', 'max', 'skew', 'issue'))
    for b in range(1, src.count + 1):
        a = src.read(b, out_shape=(src.height // 20, src.width // 20))
        a = a[np.isfinite(a)]
        name = bands[b - 1]
        keep = 'DROP' if name in DROP else 'keep'
        valid_pct = 100 * np.isfinite(src.read(b, out_shape=(src.height // 20, src.width // 20))).mean()
        qs = np.percentile(a, [25, 50, 75])
        sk = stats.skew(a)
        issues = []
        if a.std() < 0.02:
            issues.append('near-constant')
        if a.min() < -1e-4:
            issues.append('below0 %.3f' % a.min())
        if a.max() > 1 + 1e-4:
            issues.append('above1 %.3f' % a.max())
        if abs(sk) > 1.5:
            issues.append('high-skew')
        lines.append('%-6s %-7s %5.1f%% %6.3f %6.3f %6.3f %6.3f %7.3f %7.2f %s'
                     % (name, keep, valid_pct, a.min(), qs[0], qs[1], qs[2], a.max(),
                        sk, '; '.join(issues) if issues else 'OK'))
open(OUT, 'w', encoding='utf-8').write('\n'.join(lines))
print('ok')
