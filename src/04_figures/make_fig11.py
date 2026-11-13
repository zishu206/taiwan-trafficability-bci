# -*- coding: utf-8 -*-
import numpy as np, rasterio
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
plt.rcParams['font.sans-serif'] = ['Arial','DejaVu Sans']; plt.rcParams['axes.unicode_minus']=False
wd = r'C:\Users\莫名的wsr\Doubao\chats\2026-11-12\new-chat'
g1 = np.load(wd + r'\grade_majority.npy')
rmask = np.load(wd + r'\west_rmask.npy')
P = r'C:\Users\莫名的wsr\Desktop\gee\TaiXi_13indicators_30m.tif'
ds = rasterio.open(P)
bnd = ds.bounds
extent = [bnd.left, bnd.right, bnd.bottom, bnd.top]
cmap = ListedColormap(['#d55e00','#f0e442','#0072b2']); cmap.set_bad('#d9d9d9')
gg = g1.astype(float); gg[~rmask] = np.nan
mg = np.ma.array(gg, mask=~rmask)
fig, ax = plt.subplots(figsize=(8.2, 12.6))
ax.imshow(mg, extent=extent, origin='upper', cmap=cmap, vmin=0, vmax=2, interpolation='nearest')
ax.set_xlabel('Longitude/\u00b0E', fontsize=12); ax.set_ylabel('Latitude/\u00b0N', fontsize=12)
ax.set_xticks([119.5, 120.0, 120.5, 121.0]); ax.set_yticks([22.0,22.5,23.0,23.5,24.0,24.5])
ax.tick_params(labelsize=11)
ax.grid(alpha=0.25, ls='--', lw=0.5)
ax.text(120.18, 24.62, 'Western Taiwan, China', fontsize=12, fontweight='bold', color='#1a1a1a')
# 浊水溪口
ax.annotate('Zhuoshui River estuary', xy=(120.22, 23.82), xytext=(119.55, 23.45),
            fontsize=11, color='#333', arrowprops=dict(arrowstyle='->', color='#333', lw=0.9))
# 简洁箭头指北针
ax.annotate('N', xy=(0.95, 0.975), xytext=(0.95, 0.905), xycoords='axes fraction',
            ha='center', fontsize=13, fontweight='bold',
            arrowprops=dict(arrowstyle='-|>', color='black', lw=1.4))
# 比例尺 20 km（黑白相间，带边框）
from matplotlib.patches import Rectangle
km20 = 20 / (111.0 * np.cos(np.radians(23.5)))
x0, y0 = 119.45, 22.08
h = 0.045
ax.add_patch(Rectangle((x0, y0), km20/2, h, facecolor='black', edgecolor='black', lw=0.8))
ax.add_patch(Rectangle((x0+km20/2, y0), km20/2, h, facecolor='white', edgecolor='black', lw=0.8))
ax.text(x0, y0-0.055, '0', fontsize=9, ha='center')
ax.text(x0+km20/2, y0-0.055, '10', fontsize=9, ha='center')
ax.text(x0+km20, y0-0.055, '20 km', fontsize=9, ha='center')
# 图例
leg = [Patch(facecolor='#0072b2', label='High (Grade III, heavy passable)'),
       Patch(facecolor='#f0e442', label='Medium (Grade II, light passable)'),
       Patch(facecolor='#d55e00', label='Low (Grade I, immobilization)')]
ax.legend(handles=leg, loc='lower center', bbox_to_anchor=(0.5, -0.13),
          ncol=3, frameon=True, fontsize=10.5)
fig.tight_layout()
out = wd + r'\fig11_bci_final.png'
fig.savefig(out, dpi=600, bbox_inches='tight', facecolor='white')
from PIL import Image
im = Image.open(out); print('saved', out, im.size, im.info.get('dpi'))
