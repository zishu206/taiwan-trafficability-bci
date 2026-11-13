# -*- coding: utf-8 -*-
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
old = r'C:\Users\莫名的wsr\Doubao\chats\2026-11-12\new-chat'
bci = np.load(old + r'\bci_full.npy')
wr = np.load(old + r'\west_rmask.npy')
import rasterio
with rasterio.open(r'C:\Users\莫名的wsr\Desktop\gee\TaiXi_13indicators_30m.tif') as ds:
    nli = ds.read(1)
g6 = wr & (np.abs(nli - 0.32) < 0.01)
b = bci[g6]
ball = bci[wr]
fig, ax = plt.subplots(figsize=(8.2, 5.0), dpi=200)
ax.hist(ball, bins=80, density=True, alpha=0.45, color='steelblue', label='All study-area pixels')
ax.hist(b, bins=80, density=True, alpha=0.60, color='darkorange', label='G6 modern alluvium (soft soil)')
ax.axvline(0.606, color='k', ls='--', lw=1.4)
ax.axvline(0.672, color='k', ls='--', lw=1.4)
ax.text(0.606, ax.get_ylim()[1]*0.96, ' 0.606', fontsize=10)
ax.text(0.672, ax.get_ylim()[1]*0.86, ' 0.672', fontsize=10)
ax.set_xlabel('Bearing capacity index (BCI)', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.set_title('BCI compression of soft-soil (G6) pixels by linear weighted averaging', fontsize=12)
ax.legend(fontsize=10)
ax.grid(alpha=0.25)
plt.tight_layout()
out = r'C:\Users\莫名的wsr\Doubao\chats\2026-11-13\new-chat\softsoil_compression.png'
plt.saveout = None
plt.savefig(out, dpi=200)
print('saved', out)
