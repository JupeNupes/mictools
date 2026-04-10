# Pedro's Workflow Notes

> Important context and code examples provided directly by Pedro for running `mictools` processing pipelines.

## Core Concepts

"at the moment, the key operations are in the `load_data` and `process_data`. The idea for the `process_data` is that everything is based on ROIs (regions of interest). Currently, there are capabilities for doing intensity in roi and center of mass. If you need something more sophisticated you can follow the same recipe."
— Pedro

## Jupyter Notebook Example

Pedro supplied a screenshot showing exactly how to use the `mictools` package to set a path, define an ROI, and generate a plot using the built-in wrappers. 

While the example calculates the Center of Mass X-coordinate (`COM_X`) for a Diamond ROI on the `xrd` detector, the logic applies perfectly to extracting `Intensity` for XRF elements on the `me7` detector.

```python
# Cell 1
from mictools.config import *
from mictools.peak_modelling import *
from mictools.roi_utils import Roi
from mictools.process_data import *
from mictools.plot_data import *

# Set the base directory containing the HDF5 scans
set_path('/gdata/dm/19ID/2026-1/2026-1-Harder/data')

# Cell 2
# Define Region of Interest: (y_start, y_end, x_start, x_end, name)
diamond_roi = Roi(881, 922, 498, 555, name='Diamond ROI 1')

# Cell 3
# Plot the 2D interpolated flyscan map automatically
plot_flyscan(885, 'xrd', diamond_roi, roi_type='COM_X')
```

### Adapting to Molybdenum XRF
To adapt the above code for our Molybdenum XRF scans:
- **Scan Number:** Change `885` to our target scan (e.g., `99`).
- **Detector:** Use `'me7'` instead of `'xrd'`.
- **ROI Dimensions:** Use detector elements `y=0` to `7`, and spectral channels `x=1730` to `1760` (for pure Mo Kα).
- **ROI Type:** Use `'Intensity'` instead of `'COM_X'` since we want XRF counts, not a diffraction peak center of mass.
