# %%
import h5py
import numpy as np
import matplotlib.pyplot as plt
import os

from matplotlib.ticker import MultipleLocator

# %%
path2file = '/Volumes/data1/isn/2026-1/2026-1-Harder/Raw/Scan_0423/ME7/scan_0423_00009.h5'

with h5py.File(path2file,'r') as f:
    data = f['/entry/data/data'][:]

print(data.shape)

summed_data = np.sum(data, axis=(0,1))
channels = np.arange(1, 2200)
energy_keV = channels / 100
plt.plot(energy_keV, summed_data[1:2200])

plt.title('Example XRF Spectra (Summed), Sample 3')
plt.xlabel('Energy (keV)')
plt.ylabel('Total Counts')

ax = plt.gca()
ax.xaxis.set_major_locator(MultipleLocator(5))
ax.xaxis.set_minor_locator(MultipleLocator(1))
ax.grid(which='major', linestyle='-', linewidth=0.5)
ax.grid(which='minor', linestyle=':', linewidth=0.3)

plt.savefig('/Users/scott/Documents/Postdoc/Code/mictools/Scott Analysis/Average XRF spectrum.svg')
plt.show()

