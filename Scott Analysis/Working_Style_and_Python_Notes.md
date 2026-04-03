# Working Style — Scott's Preferences

> How Scott wants to work with the AI assistant going forward.

---

## Collaboration Mode: **Guided / Tutor**

- **Scott writes the code.** He wants to handle inputs, outputs, syntax, and structure himself.
- **AI provides hints and guidance**, not complete solutions (unless explicitly asked for this type of help).
- **AI should talk openly about which functions to call** — don't hide function names, module paths, or the general approach. Just let Scott handle the actual writing.
- **AI should explain concepts** when they come up naturally — data types, syntax patterns, why something works the way it does.

### What TO do:
- ✅ Name the functions Scott should look at (e.g., "you'll want `np.sum()` with the `axis` argument")
- ✅ Explain what arguments a function expects and what it returns
- ✅ Point out relevant patterns already in the `mictools` codebase he can reference
- ✅ Explain errors when he hits them — what they mean and where to look
- ✅ Suggest the general structure/order of operations
- ✅ Share Python idioms and best practices as they come up

### What NOT to do:
- ❌ Don't write complete code blocks unless asked
- ❌ Don't silently fix his code — explain what's wrong and let him fix it
- ❌ Don't skip over "obvious" things — he's learning the syntax

---

## Python Teaching Notes

### Scott's Background
- Very new to Python specifically
- Strong scientific/analytical background (synchrotron beamline work, XRF/XRD)
- Good at investigative work — figured out HDF5 data structure on his own
- Comfortable with the concepts, just needs to map them to Python syntax

### Key Concepts to Reinforce as They Come Up

#### Data Types
- **NumPy arrays** vs **Python lists** — arrays support element-wise math, lists don't
- **Shape and axes** — critical for XRF data. `(12, 7, 4096)` means axis 0 = frames, axis 1 = channels, axis 2 = spectrum
- **Slicing** — `array[start:stop]` is exclusive of stop, `array[0, :, 200:400]` grabs a slice
- **DataFrames** (pandas) — like a spreadsheet with named columns

#### Common Patterns in This Project
- `h5py.File(path, 'r')` + `with` statement for safe file access
- `np.sum(data, axis=N)` for collapsing dimensions
- `plt.plot(x, y)` and `plt.imshow(data)` for quick visualization
- Indexing: `data[frame_index, channel_index, spectral_bin]`

#### Gotchas for New Python Users
- **Indentation matters** — it defines code blocks (no braces like C/MATLAB)
- **0-indexed** — first element is `[0]`, not `[1]`
- **Slice notation** — `a[0:10]` gives elements 0 through 9 (10 is excluded)
- **Integer division** — `//` gives integer result, `/` gives float
- **Print for debugging** — `print(variable)`, `print(type(variable))`, `print(array.shape)` are your friends
- **f-strings** — `f"Scan {scanno:04d}"` is how mictools formats scan numbers

#### Useful "Check What You Have" Commands
- `type(x)` — what kind of object is x?
- `x.shape` — dimensions of a numpy array
- `x.dtype` — data type of array elements
- `len(x)` — length of a list or first dimension of array
- `dir(x)` — list all methods/attributes of an object
- `x.keys()` — for dictionaries and HDF5 groups

---

## Context for Current Work

- Working with ISN beamline data in `/Volumes/data1/isn/2026-1/2026-1-Harder/`
- **That data folder is READ-ONLY** — never modify it
- Analysis code goes in `mictools/Scott Analysis/`
- Pedro's processing tools are in `mictools/mictools/` — key modules: `load_data.py`, `process_data.py`, `data_proc.py`
- Python environment is at `mictools/.venv/` — run with `.venv/bin/python3`
- ME7 detector data shape: `(N_frames, 7_channels, 4096_spectrum)`
- Energy calibration: channel ÷ 100 = keV
