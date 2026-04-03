# Scan 239 — HDF5 Data Structure Analysis

> Scott's investigative findings on how ME7 (XRF) data is stored, verified against the actual files and the `mictools` codebase. Date: 2026-04-02.

---

## Data Location

```
/Volumes/data1/isn/2026-1/2026-1-Harder/Raw/Scan_0239/ME7/
```

> [!CAUTION]
> This data volume is **read-only** — never modify files in `2026-1-Harder`. It is our raw data archive.

---

## File Layout

| Property | Value |
|----------|-------|
| Number of `.h5` files | **22** |
| Files 1–21 data shape | `(12, 7, 4096)` |
| File 22 (last) data shape | `(2, 7, 4096)` |
| Total frames across all files | **254** (21×12 + 2) |
| HDF5 dataset path | `entry/data/data` |
| Data type | `uint32` |

---

## The Three Dimensions — Explained

### D0 — Vertical (Y) spatial positions
- **Size:** 12 per file (2 in last file)
- Each entry along D0 is one **trigger event** corresponding to a spatial position in the **vertical / slow-scan (Y)** direction.
- `mictools` calls this `file_len` and uses it as `ny`.
- Each file contains all the Y positions for one X line.

### D1 — Detector Elements (7 channels) ⚠️ NOT replicates
- **Size:** 7
- These are the **7 individual detector elements** of the Xspress3 multi-element fluorescence detector (hence "ME7" = **M**ulti-**E**lement **7**).
- Each element is a separate silicon drift detector (SDD) that independently measures XRF from the sample.
- The HDF5 metadata confirms this: there are per-channel attributes `CHAN1DTFactor` through `CHAN7DTFactor` (dead-time correction factors), `CHAN1DTPercent` through `CHAN7DTPercent`, and 8 SCAs per channel.
- **Pedro's code in `data_proc.py` (line 162) selects only channel index 1:** `xrf_data_sum = xrf_data_all[:,1,:]`
- Typical usage: sum or average across elements for better statistics, or use individual elements for dead-time-sensitive analysis.

**Counts per element (frame 0, file 1, excluding last bin):**

| Element | Total Counts |
|---------|-------------|
| Ch 0 | 70,330 |
| Ch 1 | 66,546 |
| Ch 2 | 66,985 |
| Ch 3 | 64,691 |
| Ch 4 | 68,055 |
| Ch 5 | 67,683 |
| Ch 6 | 66,407 |

The similar count totals with different per-bin values confirm these are independent detector elements viewing the same sample spot.

### D2 — XRF Energy Spectrum
- **Size:** 4096 channels
- Each entry is a **spectral bin (channel)**.
- **Energy calibration:** channel ÷ 100 = energy in keV (per Pedro).
  - Channel range 0–4095 → 0 – 40.95 keV
- **Known bug:** The **last channel (index 4095)** always contains an anomalously high value (e.g., 5,475 in frame 0). This appears to be an overflow/accumulator bin from the detector electronics. **Always exclude the last bin** in analysis.

---

## Spatial Mapping Summary

```
                      ┌─────── 22 files ───────┐
                      │  (horizontal / X axis)  │
                      │                         │
              ┌───────┤  File 1    File 2  ...  File 22
 12 frames    │       │  (12,7,   (12,7,       (2,7,
 per file     │ D0    │   4096)    4096)         4096)
 (Y axis)     │       │
              └───────┘
                        Each frame has 7 detector
                        elements × 4096 spectral bins
```

- **`mictools` scan shape:** `get_scan_info` returns `shape = (12, 22)` → **(ny=12, nx=22)**
- This is a **22 × 12 pixel** spatial scan (X × Y)
- Each file = **one horizontal column** of the image (all Y positions at one X)
- Each frame within a file = **one vertical pixel** (one Y position)

> [!NOTE]
> The last file has only 2 frames instead of 12. This means the scan may have been slightly truncated, or the last X-position had fewer Y-steps. The `mictools` functions handle this by using `file_len` from the *first* file to define the grid.

---

## Additional Metadata in Each File

Each file also contains per-frame metadata at `entry/instrument/NDAttributes/`:

| Attribute | Description |
|-----------|-------------|
| `NDArrayTimeStamp` | Timestamp per frame (for time-based trigger alignment) |
| `CHAN{1-7}DTFactor` | Dead-time correction factor per detector element |
| `CHAN{1-7}DTPercent` | Dead-time percentage per element |
| `CHAN{1-7}SCA{0-7}` | 8 Single-Channel Analyzer windows per element |
| `RingCurrent` | Synchrotron ring current at time of frame |
| `ArrayCounter` | Frame counter |

---

## How `mictools` Uses This Data

| Function | What it does with D1 |
|----------|---------------------|
| `data_proc.load_xspress3()` | Loads all data as `(N_total, 7, 4096)` |
| `data_proc.process_xps3_data()` | Selects **only channel 1** (`[:,1,:]`) for processing |
| `process_data.process_roi_file()` | Operates on `entry/data/data` via ROI slicing on D1×D2 plane |

> [!TIP]
> For better statistics, consider summing across all 7 detector elements instead of using just channel 1. This would increase counts ~7× and improve signal-to-noise. Be sure to apply dead-time corrections per element first if count rates are high.

---

## Open Questions

- [ ] Why does `data_proc.py` only use channel 1 instead of summing all 7? Ask Pedro if there's a dead-time or geometric reason.
- [ ] What is the anomalous last-bin value? Likely an overflow counter — confirm with detector manual or Pedro.
- [ ] The last file (file 22) has only 2 frames instead of 12 — was this scan truncated, or is this expected?
