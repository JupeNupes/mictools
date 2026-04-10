# XRF Line Reference — MoS₂ on Si₃N₄ with Metal Contacts

> Reference table of X-ray fluorescence emission lines and absorption edges for all elements in the sample. Excitation energy: **20.2 keV**.

---

## Sample Structure

| Component | Composition | Elements | Notes |
|-----------|------------|----------|-------|
| Active layer | MoS₂ | Mo, S | Clear area not covered by contacts |
| Contacts | Au, Cu, or Pt (TBD) | Au/Cu/Pt | Metallic, partially overlapping on either side |
| Window/Substrate | Si₃N₄ (2 µm) | Si, N | Thin membrane window |

### Priority Elements
1. **Mo** — primary target
2. **S** — from MoS₂ (overlaps with Mo L-lines)
3. **Si** — from window
4. **N** — from window (very low energy, may not be detectable)
5. **Contact metal** (Au/Cu/Pt) — useful for locating active device area

---

## Absorption Edges (below 20.2 keV)

Only shells with edges below the excitation energy (20.2 keV) will produce fluorescence.

| Element | Z | K edge (keV) | L₁ (keV) | L₂ (keV) | L₃ (keV) | M₅ (keV) |
|---------|---|-------------|-----------|-----------|-----------|-----------|
| **N**  | 7  | 0.410 | — | — | — | — |
| **Si** | 14 | 1.839 | 0.149 | 0.099 | 0.099 | — |
| **S**  | 16 | 2.472 | 0.230 | 0.163 | 0.162 | — |
| **Cu** | 29 | 8.979 | 1.097 | 0.952 | 0.933 | — |
| **Mo** | 42 | **20.000** ✅ | 2.866 | 2.625 | 2.520 | — |
| **Pt** | 78 | 78.395 ⛔ | 13.880 | 13.273 | 11.564 | 2.122 |
| **Au** | 79 | 80.725 ⛔ | 14.353 | 13.734 | 11.919 | 2.206 |

> [!IMPORTANT]
> **Mo K-edge (20.000 keV) IS excited.** Beam at 20.2 keV is 200 eV above the edge — Mo Kα and Kβ **will be present**.
>
> **Au and Pt K-edges (~80 and ~78 keV) are NOT accessible.** Only their L- and M-series will appear.
>
> **Cu K-edge (8.979 keV) is well below 20.2 keV** — Cu K-lines will be strongly excited if Cu is present.

---

## Emission Lines — By Element

### Molybdenum (Mo, Z=42) — PRIMARY TARGET

#### K-series (excited — beam at 20.2 keV > Mo K-edge at 20.0 keV)

| Line | Energy (keV) | Energy (eV) | Channel | Relative Intensity | Overlaps? |
|------|-------------|-------------|---------|---------------------|-----------|
| **Kα₁** | **17.479** | 17,479 | **1748** | Very strong | ✅ **Clean — no overlaps** |
| **Kα₂** | **17.374** | 17,374 | **1737** | Strong | ✅ **Clean — no overlaps** |
| **Kβ₁** | **19.608** | 19,608 | **1961** | Medium | ✅ **Clean — no overlaps** |
| Kβ₂ | 19.776 | 19,776 | 1978 | Weak | ✅ Clean |
| Kβ₃ | 19.590 | 19,590 | 1959 | Weak | ✅ Clean |

#### L-series (also excited at 20.2 keV)

| Line | Energy (keV) | Energy (eV) | Channel | Relative Intensity | Overlaps? |
|------|-------------|-------------|---------|---------------------|-----------|
| Ll | 2.016 | 2,016 | 202 | Weak | ✅ Clean |
| Lα₁ | 2.293 | 2,293 | 229 | Strong | ⚠️ **S Kα at 2.308 — SEVERE** |
| Lα₂ | 2.290 | 2,290 | 229 | Medium | ⚠️ **S Kα overlap** |
| Lβ₁ | 2.395 | 2,395 | 240 | Medium | 🟡 Near S Kβ |
| Lβ₃ | 2.454 | 2,454 | 245 | Weak | 🔴 ~10 eV from S Kβ |
| Lβ₄ | 2.459 | 2,459 | 246 | Weak | 🔴 ~5 eV from S Kβ |
| Lβ₂ | 2.518 | 2,518 | 252 | Weak | 🟢 Clear of S |
| Lγ₁ | 2.623 | 2,623 | 262 | Weak | 🟢 Clear of S |
| Lγ₃ | 2.834 | 2,834 | 283 | Weak | 🟢 Clear of S |

---

### Sulfur (S, Z=16) — from MoS₂

| Line | Energy (keV) | Energy (eV) | Channel | Overlaps? |
|------|-------------|-------------|---------|-----------|
| Kα₂ | 2.307 | 2,306.6 | 231 | ⚠️ **Mo Lα — SEVERE** |
| Kα₁ | 2.308 | 2,307.8 | 231 | ⚠️ **Mo Lα — SEVERE** |
| Kβ₁ | 2.464 | 2,464.0 | 246 | 🔴 Buried in Mo Lβ₃/₄ |

---

### Silicon (Si, Z=14) — from Si₃N₄ window

| Line | Energy (keV) | Energy (eV) | Channel | Overlaps? |
|------|-------------|-------------|---------|-----------|
| Kα | 1.740 | 1,740 | 174 | 🟢 Clean — isolated region |
| Kβ | 1.836 | 1,836 | 184 | 🟢 Clean |

> [!NOTE]
> Si K-lines at ~1.74 keV are in a relatively clean region. They sit below the Mo L / S K tangle (2.0+ keV) and above the very low energy lines. Should be detectable but may be attenuated by air path to the detector.

---

### Nitrogen (N, Z=7) — from Si₃N₄ window

| Line | Energy (keV) | Energy (eV) | Channel | Notes |
|------|-------------|-------------|---------|-------|
| Kα | 0.392 | 392 | 39 | ⚠️ Very low energy — likely fully absorbed |

> [!WARNING]
> N Kα at 0.392 keV (channel 39) is almost certainly **not detectable** with the ME7 Xspress3 detector. Soft X-rays at this energy are absorbed by air, detector windows, and any intervening material. Don't expect to see nitrogen in your spectra.

---

### Copper (Cu, Z=29) — CONTACT CANDIDATE

| Line | Energy (keV) | Energy (eV) | Channel | Overlaps? |
|------|-------------|-------------|---------|-----------|
| Lα | 0.930 | 930 | 93 | Low energy — weak |
| **Kα₁** | **8.048** | 8,048 | **805** | 🟢 **Clean — strong, distinctive** |
| **Kα₂** | **8.028** | 8,028 | **803** | 🟢 Clean |
| **Kβ₁** | **8.905** | 8,905 | **891** | 🟢 Clean |

> [!TIP]
> Cu has the most distinctive fingerprint of the three candidates — strong K-lines in a clean region (~8.0 keV) where neither Mo, S, Si, Au, nor Pt have lines. If you see a peak around **channel 805**, it's Cu.

---

### Gold (Au, Z=79) — CONTACT CANDIDATE

| Line | Energy (keV) | Energy (eV) | Channel | Overlaps? |
|------|-------------|-------------|---------|-----------|
| Mα | 2.120 | 2,120 | 212 | 🟡 Near Mo Ll (2.016) — may blend |
| Mβ | 2.204 | 2,204 | 220 | 🟡 Near Mo Lα region |
| **Lα₂** | **9.628** | 9,628 | **963** | 🟢 **Clean** |
| **Lα₁** | **9.713** | 9,713 | **971** | 🟢 **Clean — best Au fingerprint** |
| Lβ₁ | 11.443 | 11,443 | 1144 | 🟡 Near Pt Lβ₁ if both present |
| Lβ₂ | 11.585 | 11,585 | 1159 | 🟢 Clean |
| Lγ₁ | 13.382 | 13,382 | 1338 | 🟢 Clean |
| Lγ₂ | 13.710 | 13,710 | 1371 | 🟢 Clean |

> [!TIP]
> **Au Lα₁ at 9.71 keV (channel ~971)** is the signature line to look for. It's in a clean spectral region and is strong. If you see a clear peak there, the contacts are gold.

---

### Platinum (Pt, Z=78) — CONTACT CANDIDATE

| Line | Energy (keV) | Energy (eV) | Channel | Overlaps? |
|------|-------------|-------------|---------|-----------|
| Mα | 2.122 | 2,122 | 212 | 🟡 Near Mo Ll — may blend; also barely distinguishable from Au Mα |
| **Lα₂** | **9.362** | 9,362 | **936** | 🟢 **Clean** |
| **Lα₁** | **9.442** | 9,442 | **944** | 🟢 **Clean — best Pt fingerprint** |
| Lβ₁ | 11.071 | 11,071 | 1107 | 🟢 Clean |
| Lβ₂ | 11.251 | 11,251 | 1125 | 🟡 Near Au Lβ₁ if both present |
| Lβ₃ | 11.451 | 11,451 | 1145 | 🟡 Near Au Lβ₁ |
| Lγ₁ | 12.942 | 12,942 | 1294 | 🟢 Clean |

> [!TIP]
> **Pt Lα₁ at 9.44 keV (channel ~944)** is the signature line. It's ~270 eV lower than Au Lα₁ (9.71 keV), which is **resolvable** with the ~150 eV detector resolution. You can distinguish Au from Pt by whether the peak is at channel ~944 or ~971.

---

## How to Identify the Contact Metal

Look in the **9–10 keV region** (channels 900–1000) of your spectrum:

| If you see a peak at... | Channel | It's probably... |
|------------------------|---------|-----------------|
| ~8.05 keV | ~805 | **Cu** (Kα) |
| ~9.44 keV | ~944 | **Pt** (Lα₁) |
| ~9.71 keV | ~971 | **Au** (Lα₁) |
| Both ~9.44 and ~9.71 | ~944 + ~971 | **Both Pt and Au** (e.g., Pt adhesion layer + Au) |

Additional confirmation lines:

| Metal | Confirmation line | Channel |
|-------|------------------|---------|
| Cu | Kβ₁ at 8.91 keV | ~891 |
| Pt | Lβ₁ at 11.07 keV | ~1107 |
| Au | Lβ₁ at 11.44 keV | ~1144 |

---

## Recommended ROIs for Analysis

### Primary elements (Mo, S, Si)

| ROI | Channels | Energy range (keV) | What it measures |
|-----|----------|-------------------|-----------------|
| **Mo Kα** (pure Mo) | **1730–1760** | 17.3–17.6 | ✅ **Mo only — no overlaps** |
| Mo+S blend | 225–235 | 2.25–2.35 | Mo Lα + S Kα (inseparable) |
| Si Kα | 170–185 | 1.70–1.85 | Si from window |
| Mo Kβ | 1950–1985 | 19.5–19.85 | Mo (backup, weaker) |

### Contact metal identification

| ROI | Channels | Energy range (keV) | What it measures |
|-----|----------|-------------------|-----------------|
| Cu Kα | 795–815 | 7.95–8.15 | Cu (if present) |
| Pt Lα | 935–955 | 9.35–9.55 | Pt (if present) |
| Au Lα | 960–980 | 9.60–9.80 | Au (if present) |

---

## Known Overlap Pairs — Summary

| Overlap | Energy gap | Severity |
|---------|-----------|----------|
| **Mo Lα ↔ S Kα** | 15 eV | 🔴 **Critical — unresolvable** |
| Mo Lβ₃/₄ ↔ S Kβ | 5–10 eV | 🔴 Unresolvable |
| Au Mα ↔ Pt Mα | ~2 eV | 🔴 Identical (but both weak) |
| Pt Lα ↔ Au Lα | ~270 eV | 🟢 **Resolvable** |
| Pt Lβ₃ ↔ Au Lβ₁ | ~8 eV | 🔴 Overlapping (if both present) |

---

## Detector Channel Quick Reference

Energy = channel ÷ 100 (keV). ME7 detector: 4096 channels, 7 elements.

| Energy (keV) | Channel | What's there |
|-------------|---------|-------------|
| 0.39 | 39 | N Kα (not detectable) |
| 1.74 | 174 | **Si Kα** |
| 2.02 | 202 | Mo Ll |
| 2.12 | 212 | Au Mα / Pt Mα (weak, blended) |
| 2.29–2.31 | 229–231 | **Mo Lα + S Kα (blended)** |
| 2.45–2.46 | 245–246 | Mo Lβ₃/₄ + S Kβ (blended) |
| 8.04 | 804 | **Cu Kα** (if Cu contacts) |
| 8.91 | 891 | Cu Kβ (if Cu contacts) |
| 9.44 | 944 | **Pt Lα** (if Pt contacts) |
| 9.71 | 971 | **Au Lα** (if Au contacts) |
| 11.07 | 1107 | Pt Lβ₁ (if Pt) |
| 11.44 | 1144 | Au Lβ₁ (if Au) |
| 12.94 | 1294 | Pt Lγ₁ (if Pt) |
| 13.38 | 1338 | Au Lγ₁ (if Au) |
| **17.48** | **1748** | **Mo Kα ✅** |
| **19.61** | **1961** | **Mo Kβ ✅** |

---

## Mo vs S — Complete Cross-Reference for CXRO Booklet

### Molybdenum (Mo, Z=42) — All Lines Below 20.2 keV

| Siegbahn | IUPAC Transition | Energy (eV) | Energy (keV) | Series | Channel |
|----------|-----------------|-------------|-------------|--------|---------|
| Ll       | L₃–M₁           | 2,016       | 2.016       | L      | 202 |
| Lα₂     | L₃–M₄           | 2,290       | 2.290       | L      | 229 |
| Lα₁     | L₃–M₅           | 2,293       | 2.293       | L      | 229 |
| Lβ₁     | L₂–M₄           | 2,395       | 2.395       | L      | 240 |
| Lβ₃     | L₁–M₃           | 2,454       | 2.454       | L      | 245 |
| Lβ₄     | L₁–M₂           | 2,459       | 2.459       | L      | 246 |
| Lβ₂     | L₃–N₄,₅         | 2,518       | 2.518       | L      | 252 |
| Lγ₁     | L₂–N₄           | 2,623       | 2.623       | L      | 262 |
| Lγ₃     | L₁–N₂,₃         | 2,834       | 2.834       | L      | 283 |
| Kα₂     | K–L₂             | 17,374      | 17.374      | K      | 1737 |
| Kα₁     | K–L₃             | 17,479      | 17.479      | K      | 1748 |
| Kβ₃     | K–M₂             | 19,590      | 19.590      | K      | 1959 |
| Kβ₁     | K–M₃             | 19,608      | 19.608      | K      | 1961 |
| Kβ₂     | K–N₂,₃           | 19,776      | 19.776      | K      | 1978 |

### Sulfur (S, Z=16) — All Lines Below 20.2 keV

| Siegbahn | IUPAC Transition | Energy (eV) | Energy (keV) | Series | Channel |
|----------|-----------------|-------------|-------------|--------|---------|
| Kα₂     | K–L₂             | 2,306.6     | 2.307       | K      | 231 |
| Kα₁     | K–L₃             | 2,307.8     | 2.308       | K      | 231 |
| Kβ₁     | K–M₂,₃           | 2,464.0     | 2.464       | K      | 246 |

### Side-by-Side Overlap Map

| Energy (eV) | keV | Ch | Mo Line | S Line | Overlap? |
|-------------|-----|-----|---------|--------|----------|
| 2,016 | 2.016 | 202 | Ll | — | ✅ Mo only |
| 2,290 | 2.290 | 229 | Lα₂ | — | ⚠️ See below |
| 2,293 | 2.293 | 229 | **Lα₁** | — | ⚠️ See below |
| 2,307 | 2.307 | 231 | — | **Kα₂** | ⚠️ See below |
| 2,308 | 2.308 | 231 | — | **Kα₁** | ⚠️ See below |
| 2,395 | 2.395 | 240 | Lβ₁ | — | 🟡 ~69 eV from S Kβ |
| 2,454 | 2.454 | 245 | Lβ₃ | — | 🔴 ~10 eV from S Kβ |
| 2,459 | 2.459 | 246 | Lβ₄ | — | 🔴 ~5 eV from S Kβ |
| 2,464 | 2.464 | 246 | — | **Kβ₁** | 🔴 Buried in Mo Lβ₃/₄ |
| 2,518 | 2.518 | 252 | Lβ₂ | — | 🟢 Clear of S |
| 2,623 | 2.623 | 262 | Lγ₁ | — | 🟢 Clear of S |
| 2,834 | 2.834 | 283 | Lγ₃ | — | 🟢 Clear of S |
| 17,374 | 17.374 | 1737 | **Kα₂** | — | ✅ **Mo only** |
| 17,479 | 17.479 | 1748 | **Kα₁** | — | ✅ **Mo only** |
| 19,590 | 19.590 | 1959 | Kβ₃ | — | ✅ Mo only |
| 19,608 | 19.608 | 1961 | **Kβ₁** | — | ✅ Mo only |
| 19,776 | 19.776 | 1978 | Kβ₂ | — | ✅ Mo only |

### The 2.0–2.9 keV Tangle

```
   Mo Ll  Mo Lα₂ Mo Lα₁        S Kα      Mo Lβ₁     Mo Lβ₃/₄ + S Kβ   Mo Lβ₂    Mo Lγ₁   Mo Lγ₃
    │       ││                 ││           │            │││               │          │         │
────┼───────┼┼─────────────────┼┼───────────┼────────────┼┼┼───────────────┼──────────┼─────────┼──
  2.02    2.29               2.31        2.40          2.46             2.52       2.62      2.83  keV
         ◄ 15 eV ►                                   ◄ 5-10 eV ►
         UNRESOLVABLE                                 UNRESOLVABLE
```

**For comparing Mo-only vs Mo+S maps:**
- **Mo-only ROI:** channels **1730–1760** (Mo Kα, 17.3–17.5 keV) — pure Mo
- **Mo+S blended ROI:** channels **225–235** (2.25–2.35 keV) — Mo Lα + S Kα, inseparable
- Any spatial difference between these two maps reflects the **S distribution** relative to Mo

*Sources: X-Ray Data Booklet (LBNL), NIST X-ray Transition Energies Database, CXRO*
