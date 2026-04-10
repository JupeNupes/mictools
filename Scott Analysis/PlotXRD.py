# %%
import h5py
import numpy as np
import matplotlib.pyplot as plt
from glob import glob

# %%
# Get all XRD files for Scan 423, sorted
files = sorted(glob('/Volumes/data1/isn/2026-1/2026-1-Harder/Raw/Scan_0423/XRD/scan_0423_*.h5'))
print(f"Found {len(files)} files")

# Accumulate sum: open one file at a time, sum its frames, add to total
summed_image = None

for i, filepath in enumerate(files):
    with h5py.File(filepath, 'r') as f:
        # Sum all frames (axis 0) in this file → (1062, 1028), then discard
        file_sum = np.sum(f['entry/data/data'][:], axis=0, dtype=np.int64)

    if summed_image is None:
        summed_image = file_sum
    else:
        summed_image += file_sum

    print(f"  Processed file {i+1}/{len(files)}")

print(f"Final summed image shape: {summed_image.shape}")

# %%
# Plot the summed diffraction pattern
plt.figure(figsize=(8, 8))
plt.imshow(np.log10(summed_image + 1), cmap='inferno')
plt.colorbar(label='log10(Counts + 1)')
plt.title('Summed XRD Pattern — Scan 423')
plt.xlabel('X pixel')
plt.ylabel('Y pixel')
plt.savefig('/Users/scott/Documents/Postdoc/Code/mictools/Scott Analysis/Summed_XRD_Scan423.svg')
plt.show()
