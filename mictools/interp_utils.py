import numpy as np
from scipy.interpolate import griddata
from scipy.spatial import Delaunay, cKDTree

def griddata_with_provenance(points, values, xi, method='linear', fill_value=np.nan, return_provenance=False):
    """
    A drop-in replacement for scipy.interpolate.griddata that optionally returns
    the provenance of the interpolation (the raw trigger indices and weights that
    contributed to each interpolated pixel).

    Parameters:
    -----------
    points : ndarray of floats, shape (n, D)
        Data point coordinates.
    values : ndarray of float or complex, shape (n,)
        Data values.
    xi : 2-D ndarray of floats, shape (m, D) or tuple of ndarrays broadcastable to same shape
        Points at which to interpolate data.
    method : {'linear', 'nearest'}
        Method of interpolation.
    fill_value : float, optional
        Value used to fill in for requested points outside of the convex hull.
    return_provenance : bool, optional
        If True, returns a tuple of (interpolated_values, provenance_indices, provenance_weights).
        If False (default), behaves identically to scipy's griddata and returns just the interpolated_values.

    Returns:
    --------
    Z : ndarray
        Array of interpolated values.
    provenance_indices : ndarray of ints (only if return_provenance=True)
        Shape (m, 3). The indices of the raw points that contributed to the pixel.
    provenance_weights : ndarray of floats (only if return_provenance=True)
        Shape (m, 3). The weights (barycentric coordinates) of the contributing points.
    """
    
    # Fast path: if provenance is not requested, just use scipy's griddata directly
    if not return_provenance:
        return griddata(points, values, xi, method=method, fill_value=fill_value)
    
    # Prepare query points into a flat array of shape (N, 2)
    if isinstance(xi, tuple):
        query_pts = np.c_[xi[0].ravel(), xi[1].ravel()]
        out_shape = xi[0].shape
    else:
        query_pts = xi
        out_shape = xi.shape[:-1] if xi.ndim > 1 else (xi.shape[0],)

    num_pixels = query_pts.shape[0]
    provenance_indices = np.full((num_pixels, 3), -1, dtype=int)
    provenance_weights = np.zeros((num_pixels, 3), dtype=float)

    if method == 'linear':
        tri = Delaunay(points)
        simplex_indices = tri.find_simplex(query_pts)
        
        valid_mask = simplex_indices >= 0
        si = simplex_indices[valid_mask]
        q = query_pts[valid_mask]
        
        # Calculate barycentric weights
        if len(si) > 0:
            T = tri.transform[si, :2]
            r = q - tri.transform[si, 2]
            b = np.einsum('ijk,ik->ij', T, r)
            bary_weights = np.c_[b, 1.0 - b.sum(axis=1)]
            
            bary_vertices = tri.simplices[si]
            
            # Store in the flat provenance arrays
            provenance_indices[valid_mask] = bary_vertices
            provenance_weights[valid_mask] = bary_weights
            
            # Calculate interpolated value
            Z_flat = np.full(num_pixels, fill_value, dtype=float)
            Z_flat[valid_mask] = np.sum(bary_weights * values[bary_vertices], axis=1)
        else:
            Z_flat = np.full(num_pixels, fill_value, dtype=float)
            
    elif method == 'nearest':
        tree = cKDTree(points)
        distances, nearest_idx = tree.query(query_pts)
        
        # Provenance for nearest is just the single closest point with weight 1.0
        provenance_indices[:, 0] = nearest_idx
        provenance_weights[:, 0] = 1.0
        
        Z_flat = values[nearest_idx]
        
    else:
        raise ValueError("Only 'linear' and 'nearest' methods are supported with provenance.")

    # Reshape
    Z = Z_flat.reshape(out_shape)
    provenance_indices = provenance_indices.reshape(out_shape + (3,))
    provenance_weights = provenance_weights.reshape(out_shape + (3,))
    
    return Z, provenance_indices, provenance_weights
