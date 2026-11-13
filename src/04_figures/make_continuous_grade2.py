# -*- coding: utf-8 -*-
import numpy as np, rasterio
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
plt.rcParams['font.sans-serif'] = ['Arial','DejaVu Sans']; plt.rcParams['axes.unicode_minus']=False
old = r'C:\Users\莫名的wsr\Doubao\chats\2026-11-12\new-chat'
bci = np.load(old + r'\bci_full.npy')
g1 = np.load(old + r'\grade_majority.npy')
rmask = np.load(old + r'\west_rmask.npy')
with rasterio.open(r'C:\Users\莫名的wsr\Desktop\gee\TaiXi_13indicators_30m.tif') as ds:
    bnd = ds.bounds
extent = [bnd.left, bnd.right, bnd.bottom, bnd.top]
band = ((np.abs(bci-0.606)<0.01) | (np.abs(bci-0.672)<0.01)) & rmask
# 3倍降采样
f = 3
H, W = bci.shape
h, w = H//f, W//f
def crop(a): return a[:h*f, :w*f].reshape(h, f, w, f)
bc = crop(np.where(rmask, bci, np.nan))
bcs = np.nanmean(bc, axis=(1, 3))
rm = crop(rmask.astype(float)).mean(axis=(1,3)) > 0.5
gc = crop(g1.astype(float))
# 众数
gs = np.zeros((h, w))
for k in range(3):
    pass
gcount = np.zeros((h, w, 3))
for k in range(3):
    gcount[:, :, k] = (gc == k).sum(axis=(1, 3))
gs = gcount.argmax(axis=2).astype(float)
bd2 = crop(band.astype(float)).max(axis=(1,3)) > 0
bcs[~rm] = np.nan; gs[~rm] = np.nan
cmap = ListedColormap(['#d55e00','#f0e442','#0072b2'])
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.6, 12.4))
im1 = ax1.imshow(np.ma.array(bcs, mask=~rm), extent=extent, origin='upper',
                 cmap='YlOrRd', vmin=0.35, vmax=0.80, interpolation='nearest')
ax1.set_title('(a) Continuous BCI (no hard grade boundaries)', fontsize=13, fontweight='bold')
cb = fig.colorbar(im1, ax=ax1, fraction=0.046, pad=0.03); cb.set_label('Bearing capacity index', fontsize=11)
ax2.imshow(np.ma.array(gs, mask=~rm), extent=extent, origin='upper',
           cmap=cmap, vmin=0, vmax=2, interpolation='nearest')
ax2.imshow(np.where(bd2, 1.0, np.nan), extent=extent, origin='upper',
           cmap='Greys', alpha=0.45, interpolation='nearest')
ax2.set_title('(b) Three-grade map with breakpoint uncertainty band (±0.01)', fontsize=13, fontweight='bold')
for ax in (ax1, ax2):
    ax.set_xlabel('Longitude/\u00b0E', fontsize=12); ax.set_ylabel('Latitude/\u00b0N', fontsize=12)
    ax.set_xticks([119.5,120.0,120.5,121.0]); ax.set_yticks([22.0,22.5,23.0,23.5,24.0,24.5])
    ax.tick_params(labelsize=11); ax.grid(alpha=0.25, ls='--', lw=0.5)
    ax.annotate('N', xy=(0.95,0.975), xytext=(0.95,0.905), xycoords='axes fraction',
                ha='center', fontsize=13, fontweight='bold',
                arrowprops=dict(arrowstyle='-|>', color='black', lw=1.4))
ax2.annotate('Uncertainty band', xy=(120.5,23.6), xytext=(119.5,22.7),
             fontsize=10, color='#222', arrowprops=dict(arrowstyle='->', color='#222', lw=0.9))
leg = [Patch(facecolor='#0072b2', label='High (Grade III)'),
       Patch(facecolor='#f0e442', label='Medium (Grade II)'),
       Patch(facecolor='#d55e00', label='Low (Grade I)'),
       Patch(facecolor='grey', alpha=0.45, label='Within ±0.01 of a breakpoint')]
ax2.legend(handles=leg, loc='lower center', bbox_to_anchor=(0.5,-0.13), ncol=2, fontsize=10.5)
fig.tight_layout()
out = r'C:\Users\莫名的wsr\Doubao\chats\2026-11-13\new-chat\fig_bci_continuous_grade.png'
fig.savefig(out, dpi=300, bbox_inches='tight', facecolor='white')
from PIL import Image
print('saved', out, Image.open(out).size)
