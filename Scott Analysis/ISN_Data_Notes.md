# ISN Data Processing Notes

> Summary of key information exchanged between Scott and Pedro regarding the In Situ Nanoprobe (ISN) data collected at 19-ID.

---

## Overview

Pedro maintains the [`mictools`](https://github.com/pdrmrcd/mictools/) repository — a set of data processing tools for ISN beamline data. The data consists of spatially-resolved **XRF spectra** and **XRD patterns** collected via fly-scanning.

---

## ⚠️ Critical Concept: Why You Can't Just "Pick a Pixel"

> [!IMPORTANT]
> The 2D spatial images (e.g., the 22×12 maps) are **not raw data**. They are the **output of an interpolation step**. Asking for "the spectrum at pixel (x=2, y=3)" is **not physically meaningful** because that pixel's value was computed by interpolating from nearby raw measurements that were collected at slightly different, irregular positions.

### The ISN Sampling Scheme

The ISN hardware was designed for **time-based triggering fly-scans**:

1. **Motors move continuously** along a raster trajectory (they don't step-and-settle).
2. **Triggers are sent at regular time intervals** — not at precise spatial positions.
3. Each trigger fires **simultaneously** on all detectors (XRF, XRD, interferometer), capturing one frame from each.
4. The **motors are not perfectly precise** — the actual trajectory deviates from the ideal straight-line raster. Small variations and drifts occur.
5. The **interferometer** (SOCKETSERVER data) records the actual sample position at each trigger event. This is the ground-truth position data.

**Result:** The raw data is a set of (spectrum, position) pairs where the positions are **irregularly spaced** — not on a nice grid.

### The Interpolation Step

To produce the clean 2D spatial maps, `mictools` uses `scipy.interpolate.griddata` to interpolate the irregularly-sampled data onto a regular grid:

```
Raw data:
  Trigger 1 → (x₁, y₁) → spectrum₁, XRD₁
  Trigger 2 → (x₂, y₂) → spectrum₂, XRD₂
  ...
  Trigger N → (xₙ, yₙ) → spectrumₙ, XRDₙ

    ↓  griddata interpolation  ↓

Regular 2D grid:
  Pixel (0,0) → interpolated value (weighted blend of nearby raw measurements)
  Pixel (0,1) → interpolated value
  ...
```

### Where Interpolation Happens in the Code

| Function | File | What it does |
|----------|------|-------------|
| `mesh_detector_data()` | `process_data.py` L261–294 | Main interpolation pipeline — merges position + detector data, calls `griddata` with both `linear` and `nearest` methods, fills NaN gaps |
| `process_xps3_data()` | `data_proc.py` L155–227 | Alternative path — also uses `griddata` for XRF element maps |

**Key detail from `mesh_detector_data()`:**
- Uses **`method='linear'`** (smooth, NaN outside convex hull) as primary interpolation
- Falls back to **`method='nearest'`** to fill gaps outside the convex hull
- The final image is a hybrid: `Z = where(isnan(Z_linear), Z_nearest, Z_linear)`

### Implications for Point Analysis

> [!CAUTION]
> If you want to extract the raw spectrum/XRD at a specific spatial location, you **cannot** simply index into the interpolated image. You need to:
> 1. Know which raw trigger events contributed to that interpolated pixel
> 2. Retrieve the original raw spectra from those triggers
> 3. Optionally weight them the same way `griddata` did

This is a **currently missing capability** in `mictools`. See [Proposed Feature: Interpolation Provenance Tracker](#proposed-feature-interpolation-provenance-tracker) below.

---

## Data Location & File Types

| File Type | Contents |
|-----------|----------|
| HDF5 (`.h5`) — scan files | Scan metadata, motor positions, fluorescence data |
| HDF5 (`.h5`) — large detector files | Diffraction (XRD) data |
| RAW files | Fluorescence (XRF) spectra |
| SOCKETSERVER folders | Interferometer position data for fly-scans |

---

## Key Questions & Answers

### 1. Scan Metadata

#### a) Positioner / Motor Feedback Data
- **Location in HDF5:** `entry > instrument > bluesky > streams > baseline`
- Contains all motor metadata at the **beginning** and **end** of each scan.
- For **fly-scans**, the per-trigger position data is saved to the **SOCKETSERVER folders** (interferometer files).
- A function in `mictools` converts those interferometer files into sample positions.

#### b) Scan Dimensions (e.g., 40 × 120 pixels)
- Use the function **`get_scan_info`** from `mictools` to retrieve scan dimensions.

---

### 2. Fluorescence (XRF) Spectra

- Found in the **RAW files**.
- **Energy calibration:** Divide the x-axis (channel number) by **100** to convert to **keV**.
  - e.g., channel 600 → 6.00 keV

---

### 3. Diffraction (XRD) Data

- Contained in the **large `.h5` detector files** associated with each scan.

---

### 4. Spatial Correlation of Spectra to Sample Position

- The beamline uses **time-based triggering**: each trigger event is associated with one detector frame for both diffraction and fluorescence.
- The interferometer data (from SOCKETSERVER) gives the sample position per trigger, which can then be mapped to the corresponding detector frame.
- `mictools` provides plotting functions that combine position data with spectral/diffraction data.

---

## Full Data Pipeline — From Triggers to 2D Image

```
┌─────────────────────────────────────────────────────────────────┐
│                    HARDWARE (during scan)                        │
│                                                                 │
│   Motors move continuously → Triggers fire at regular Δt        │
│                                                                 │
│   Each trigger simultaneously captures:                         │
│     • XRF spectrum (ME7 detector, 7 elements × 4096 channels)   │
│     • XRD frame (diffraction detector)                          │
│     • Interferometer position (x, y, z at that instant)         │
│     • Timestamp                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RAW DATA (on disk)                            │
│                                                                 │
│   ME7/scan_NNNN_XXXXX.h5  →  XRF spectra (12 triggers/file)    │
│   XRD/scan_NNNN_XXXXX.h5  →  XRD frames                        │
│   SOCKETSERVER/            →  Interferometer positions           │
│   bluesky/                 →  Scan metadata, baseline motors    │
└─────────────────────────────────────────────────────────────────┘
                              │
                    load_data.py functions
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│               PROCESSED DATA (1D list per trigger)              │
│                                                                 │
│   process_position_data()  →  DataFrame: Trigger, X_pos, Y_pos │
│   process_detector_data()  →  DataFrame: Timestamp, Intensity,  │
│                                COM_Y, COM_X (from ROI)          │
│                                                                 │
│   At this stage: data is a LIST of (position, value) pairs      │
│   with IRREGULAR spatial sampling.                              │
│                                                                 │
│   >>> This is the last stage where raw trigger indices exist <<< │
└─────────────────────────────────────────────────────────────────┘
                              │
                    mesh_detector_data()
                    scipy.interpolate.griddata
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              INTERPOLATED 2D IMAGE  (regular grid)              │
│                                                                 │
│   X, Y, Z = mesh_detector_data(...)                             │
│                                                                 │
│   Z is a (ny × nx) array on a regular grid.                     │
│   Each pixel is a WEIGHTED BLEND of nearby raw measurements.    │
│                                                                 │
│   >>> Raw trigger provenance is LOST at this stage <<<          │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key `mictools` Modules

| Module | Purpose |
|--------|---------|
| `load_data.py` | Loading scan data from HDF5 and raw files |
| `process_data.py` | Processing based on **ROIs** (regions of interest) — supports intensity-in-ROI and center-of-mass calculations; also contains `mesh_detector_data()` for interpolation |
| `plot_data.py` | Plotting / visualization utilities |
| `data_proc.py` | Additional data processing functions (alternative XRF pipeline) |
| `peak_modelling.py` | Peak fitting / modelling |
| `config.py` | Path configuration (`set_path` / `get_path`) |
| `roi_utils.py` | ROI class definition |

### Recommended Starting Points
Pedro recommends starting with:
1. **`load_data`** — for reading in data
2. **`process_data`** — for ROI-based analysis (intensity in ROI, center of mass, extensible to custom operations)

---

## Proposed Feature: Interpolation Provenance Tracker

> [!TIP]
> Pedro has expressed interest in this feature for inclusion in `mictools` if Scott implements it.

### The Problem
Once `griddata` interpolates the raw measurements onto a regular grid, there is **no record** of which raw triggers (and therefore which raw spectra/XRD frames) contributed to each output pixel, or with what weights.

### The Goal
At interpolation time, record for each output grid pixel:
- **Which raw trigger indices** were used
- **What weights** were applied (the interpolation coefficients)

This would allow looking up a pixel in the interpolated image and retrieving the **actual raw spectra** that contributed to it.

### Implementation Approach (Scott's plan)
Modify the interpolation step in `mesh_detector_data()` to:
1. For each output grid point, identify the enclosing Delaunay simplex (triangle for 2D linear interpolation)
2. Record the 3 vertex indices (= raw trigger indices) and their barycentric weights
3. Store these as parallel arrays alongside the interpolated image

### Key Technical Details
- `scipy.interpolate.griddata` with `method='linear'` internally builds a **Delaunay triangulation** of the input points.
- For any query point inside a triangle, it computes **barycentric coordinates** (3 weights that sum to 1) from the triangle's 3 vertices.
- The interpolated value = w₁·v₁ + w₂·v₂ + w₃·v₃ where (w₁, w₂, w₃) are barycentric coords and (v₁, v₂, v₃) are the raw data values at the 3 vertices.
- For `method='nearest'` (used to fill NaN gaps outside convex hull), each output pixel maps to exactly 1 raw trigger.

### Status
- [ ] Not yet implemented
- Pedro says this is "in the plans for future development"
- Pedro has agreed to include Scott's implementation as a feature in `mictools` if shared

---

## Quick Reference

| Item | Value / Location |
|------|-----------------|
| XRF energy calibration | channel ÷ 100 = keV |
| Motor metadata path (HDF5) | `entry/instrument/bluesky/streams/baseline` |
| Fly-scan positions | SOCKETSERVER folders (interferometer data) |
| Triggering scheme | Time-based (1 trigger = 1 frame for XRF + XRD) |
| Scan dimensions function | `get_scan_info()` |
| Interpolation method | `scipy.interpolate.griddata` (linear + nearest fallback) |
| Interpolation function | `mesh_detector_data()` in `process_data.py` |
| Repository | [github.com/pdrmrcd/mictools](https://github.com/pdrmrcd/mictools/) |
