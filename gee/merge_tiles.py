# -*- coding: utf-8 -*-
# 用途：把 GEE 分块导出的 part1..part4 GeoTIFF 合并为单个 13 波段影像。
# 操作：把 4 个 part tif 放进同一个文件夹，修改下面的 INPUT_DIR，运行本脚本即可。
import glob
import os
import rasterio
from rasterio.merge import merge

# ===== 只需修改这里：4 个分块 tif 所在文件夹（替换为你本地的实际路径） =====
INPUT_DIR = r'[path-to-the-folder-with-part1..part4-tifs]'
OUTPUT_TIF = os.path.join(INPUT_DIR, 'TaiXi_13indicators_30m_merged.tif')

# 自动收集并按文件名排序（保证 part1、part2... 顺序）
files = sorted(glob.glob(os.path.join(INPUT_DIR, '*.tif')))
files = [f for f in files if 'merged' not in os.path.basename(f)]
if not files:
    raise SystemExit('未在该文件夹找到 .tif，请检查 INPUT_DIR 路径')
print('待合并文件：')
for f in files:
    print('  ', os.path.basename(f))

srcs = [rasterio.open(f) for f in files]
mosaic, out_trans = merge(srcs)

out_meta = srcs[0].meta.copy()
out_meta.update({
    'driver': 'GTiff',
    'height': mosaic.shape[1],
    'width': mosaic.shape[2],
    'transform': out_trans,
    'count': mosaic.shape[0],
    'nodata': srcs[0].nodata
})
with rasterio.open(OUTPUT_TIF, 'w', **out_meta) as dst:
    dst.write(mosaic)
    dst.descriptions = srcs[0].descriptions

for s in srcs:
    s.close()
print('合并完成 ->', OUTPUT_TIF)
