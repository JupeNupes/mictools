"""
verify_griddata_equivalence.py
==============================
Proof that our Delaunay-based interpolation (which also yields provenance data)
produces results IDENTICAL to scipy.interpolate.griddata.

WHY THIS MATTERS
----------------
griddata is a convenience wrapper. It builds a Delaunay triangulation internally,
computes barycentric coordinates, and returns the interpolated values — but throws
away all the bookkeeping (which raw points contributed, with what weights).

We need that bookkeeping to track which raw trigger spectra contribute to each
pixel in the interpolated ISN image. So we "open the wrapper" and call the same
underlying routines directly — Delaunay triangulation + barycentric math — which
lets us capture the provenance while producing the exact same interpolated values.

This script tests both interpolation methods used in mesh_detector_data():
  1) method='linear'   — Delaunay triangulation + barycentric weighting
  2) method='nearest'  — closest-point lookup via KDTree

Author: Scott (with AI assist)
Date:   2026-04-02
"""

import numpy as np
from scipy.interpolate import griddata
from scipy.spatial import Delaunay, cKDTree


# =============================================================================
# TEST SETUP — Synthetic irregular points and a regular output grid
# =============================================================================
# Mimic the ISN case: irregularly sampled input positions → regular grid output.
# Use enough points that the triangulation is non-trivial.

rng = np.random.default_rng(42)  # fixed seed for reproducibility

N_raw = 200                       # number of "raw trigger" measurements
pts = rng.uniform(0, 10, (N_raw, 2))  # irregular (x, y) positions
values = np.sin(pts[:, 0]) * np.cos(pts[:, 1])  # some smooth test function

# Regular output grid (like the ISN interpolated image)
nx, ny = 30, 25
x_grid = np.linspace(pts[:, 0].min(), pts[:, 0].max(), nx)
y_grid = np.linspace(pts[:, 1].min(), pts[:, 1].max(), ny)
X, Y = np.meshgrid(x_grid, y_grid)
xi_flat = np.c_[X.ravel(), Y.ravel()]  # (ny*nx, 2) query points


# =============================================================================
# REFERENCE: scipy.interpolate.griddata (the function we're replacing)
# =============================================================================
Z_griddata_linear  = griddata(pts, values, (X, Y), method='linear')
Z_griddata_nearest = griddata(pts, values, (X, Y), method='nearest')


# =============================================================================
# OUR METHOD: Delaunay + barycentric coordinates (linear interpolation)
# =============================================================================
# This is the SAME math griddata does internally, but we keep the bookkeeping.

tri = Delaunay(pts)                        # Step 1: triangulate the raw points
simplex_indices = tri.find_simplex(xi_flat)  # Step 2: which triangle is each grid pt in?

# Identify valid (inside convex hull) vs invalid (outside) points
valid_mask = simplex_indices >= 0
si = simplex_indices[valid_mask]     # simplex indices for valid points
q  = xi_flat[valid_mask]             # query coordinates for valid points

# Step 3: Compute barycentric coordinates (the interpolation weights).
#   tri.transform[si, :2]  is a (2x2) affine matrix for each simplex
#   tri.transform[si, 2]   is the "origin vertex" of that simplex
#   The barycentric coords of the first 2 vertices are:
#       b = transform[:2] @ (query_point - origin_vertex)
#   The 3rd coordinate is 1 - b[0] - b[1] (they must sum to 1).
T = tri.transform[si, :2]                          # (M, 2, 2)
r = q - tri.transform[si, 2]                       # (M, 2)
b = np.einsum('ijk,ik->ij', T, r)                  # (M, 2) — first 2 bary coords
bary_weights = np.c_[b, 1.0 - b.sum(axis=1)]       # (M, 3) — all 3 bary coords

# Step 4: Get the 3 raw-point indices forming each triangle
bary_vertices = tri.simplices[si]                   # (M, 3) — indices into pts[]

# Step 5: Compute interpolated value = weighted sum of vertex values
Z_ours_linear_flat = np.full(xi_flat.shape[0], np.nan)
Z_ours_linear_flat[valid_mask] = np.sum(
    bary_weights * values[bary_vertices], axis=1
)
Z_ours_linear = Z_ours_linear_flat.reshape(X.shape)


# =============================================================================
# OUR METHOD: cKDTree (nearest-neighbor interpolation)
# =============================================================================
tree = cKDTree(pts)
distances, nearest_idx = tree.query(xi_flat)   # nearest raw point for each grid pt

Z_ours_nearest = values[nearest_idx].reshape(X.shape)


# =============================================================================
# COMPARISON
# =============================================================================
print("=" * 65)
print("VERIFICATION: griddata vs. our Delaunay-based implementation")
print("=" * 65)

# --- Linear ---
# NaN positions should match (both NaN outside convex hull)
nan_match = np.array_equal(
    np.isnan(Z_griddata_linear),
    np.isnan(Z_ours_linear)
)
# Compare numeric values where both are valid
valid_both = ~np.isnan(Z_griddata_linear) & ~np.isnan(Z_ours_linear)
if valid_both.any():
    max_diff_linear = np.max(np.abs(
        Z_griddata_linear[valid_both] - Z_ours_linear[valid_both]
    ))
else:
    max_diff_linear = 0.0

print(f"\n  LINEAR INTERPOLATION")
print(f"  {'NaN positions match:':<35} {nan_match}")
print(f"  {'Max absolute difference:':<35} {max_diff_linear:.2e}")
print(f"  {'Identical (within float eps):':<35} {max_diff_linear < 1e-14}")

# --- Nearest ---
max_diff_nearest = np.max(np.abs(Z_griddata_nearest - Z_ours_nearest))
exact_match_nearest = np.array_equal(Z_griddata_nearest, Z_ours_nearest)

print(f"\n  NEAREST-NEIGHBOR INTERPOLATION")
print(f"  {'Max absolute difference:':<35} {max_diff_nearest:.2e}")
print(f"  {'Exact match (bitwise):':<35} {exact_match_nearest}")

# --- Combined (mimicking mesh_detector_data's NaN-fill logic) ---
Z_combined_griddata = np.where(
    np.isnan(Z_griddata_linear), Z_griddata_nearest, Z_griddata_linear
)
Z_combined_ours = np.where(
    np.isnan(Z_ours_linear), Z_ours_nearest, Z_ours_linear
)
max_diff_combined = np.max(np.abs(Z_combined_griddata - Z_combined_ours))

print(f"\n  COMBINED (linear + nearest fallback, as in mesh_detector_data)")
print(f"  {'Max absolute difference:':<35} {max_diff_combined:.2e}")
print(f"  {'Identical (within float eps):':<35} {max_diff_combined < 1e-14}")

# --- Overall verdict ---
all_pass = (
    nan_match
    and max_diff_linear < 1e-14
    and exact_match_nearest
    and max_diff_combined < 1e-14
)
print(f"\n{'=' * 65}")
if all_pass:
    print("  ✅ ALL TESTS PASSED — implementations are numerically identical.")
else:
    print("  ❌ MISMATCH DETECTED — check results above.")
print(f"{'=' * 65}")


# =============================================================================
# BONUS: Show the provenance data that our method produces (griddata can't)
# =============================================================================
print("\n\nBONUS: Example provenance data for 3 grid pixels")
print("-" * 65)
# Pick 3 grid pixels that are inside the convex hull
example_flat_indices = np.where(valid_mask)[0][:3]

for fi in example_flat_indices:
    row, col = divmod(fi, nx)
    si_val = simplex_indices[fi]
    verts = tri.simplices[si_val]

    # Recompute weights for display
    b_ex = tri.transform[si_val, :2].dot(xi_flat[fi] - tri.transform[si_val, 2])
    w = np.append(b_ex, 1 - b_ex.sum())

    print(f"\n  Grid pixel [{row}, {col}]  (x={X[row,col]:.3f}, y={Y[row,col]:.3f})")
    print(f"    Interpolated value: {Z_ours_linear[row, col]:.6f}")
    print(f"    Contributing raw triggers and weights:")
    for v, wt in zip(verts, w):
        print(f"      trigger {v:>3d}  @ ({pts[v,0]:.3f}, {pts[v,1]:.3f})"
              f"  value={values[v]:+.6f}  weight={wt:.4f}")
    print(f"    Weighted sum check: {np.dot(w, values[verts]):.6f}")
