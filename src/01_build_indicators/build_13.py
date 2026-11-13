# -*- coding: utf-8 -*-
import os
import numpy as np
import rasterio
from rasterio.windows import Window

SRC = r'C:\Users\莫名的wsr\Desktop\gee\TaiXi_15indicators_30m_merged.tif'
OUT = r'C:\Users\莫名的wsr\Desktop\gee\TaiXi_13indicators_30m.tif'
REPORT = r'C:\Users\莫名的wsr\Desktop\gee\build_13_report.txt'
DROP = ['NDWI', 'TWI']
TILE = 256

with rasterio.open(SRC) as src:
    old = list(src.descriptions)
    keep_idx = [i for i, n in enumerate(old) if n not in DROP]
    new_names = [old[i] for i in keep_idx]
    meta = src.meta.copy()
    meta.update({'driver': 'GTiff', 'count': len(new_names), 'compress': 'lzw',
                 'tiled': True, 'blockxsize': TILE, 'blockysize': TILE,
                 'BIGTIFF': 'YES', 'interleave': 'pixel'})
    with rasterio.open(OUT, 'w', **meta) as dst:
        dst.descriptions = tuple(new_names)
        for y in range(0, src.height, TILE):
            for x in range(0, src.width, TILE):
                w = Window(x, y, min(TILE, src.width - x), min(TILE, src.height - y))
                d = src.read(window=w)[keep_idx]
                d = np.clip(d, 0.0, 1.0)
                dst.write(d, window=w)

with rasterio.open(OUT) as chk:
    lines = ['new bands (%d): %s' % (chk.count, chk.descriptions),
             'profile: %s' % repr(chk.profile)]
    for b in range(1, chk.count + 1):
        a = chk.read(b, out_shape=(chk.height // 30, chk.width // 30))
        a = a[np.isfinite(a)]
        lines.append('%-6s min=%.3f max=%.3f mean=%.3f'
                     % (chk.descriptions[b-1], a.min(), a.max(), a.mean()))
open(REPORT, 'w', encoding='utf-8').write('\n'.join(lines))
print('done')
