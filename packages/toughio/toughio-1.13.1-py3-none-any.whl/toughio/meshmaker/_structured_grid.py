import numpy as np

from .._mesh._mesh import CellBlock, Mesh

__all__ = [
    "structured_grid",
]


def structured_grid(dx, dy, dz=None, origin=None, layer=False, material="dfalt"):
    """
    Generate 2D or 3D non-uniform structured grid.

    Parameters
    ----------
    dx : array_like
        Grid spacing along X axis.
    dy : array_like
        Grid spacing along Y axis.
    dz : array_like or None, optional, default None
        Grid spacing along Z axis. If `None`, generate 2D grid.
    origin : array_like or None, optional, default None
        Origin point coordinate.
    layer : bool, optional, default False
        If `True`, mesh will be generated by layers.
    material : str, optional, default 'dfalt'
        Default material name.

    Returns
    -------
    toughio.Mesh
        Output non-uniform structured mesh.

    """
    if not isinstance(dx, (list, tuple, np.ndarray)):
        raise TypeError()
    if not isinstance(dy, (list, tuple, np.ndarray)):
        raise TypeError()
    if not (dz is None or isinstance(dz, (list, tuple, np.ndarray))):
        raise TypeError()
    if not isinstance(material, str):
        raise TypeError()

    order = "F" if layer else "C"
    if dz is None:
        ndim = 2
        points, cells = _grid_2d(dx, dy, order)
    else:
        ndim = 3
        points, cells = _grid_3d(dx, dy, dz, order)

    if not (
        origin is None
        or (isinstance(origin, (list, tuple, np.ndarray)) and len(origin) == ndim)
    ):
        raise ValueError()
    origin = (
        np.asarray(origin)
        if origin is not None
        else (np.zeros(ndim) if ndim == 2 else np.array([0.0, 0.0, -np.sum(dz)]))
    )
    points += origin

    points = points if ndim == 3 else np.column_stack((points, np.zeros(len(points))))

    mesh = Mesh(points, cells)
    mesh.add_cell_data("material", np.ones(mesh.n_cells, dtype=np.int64))
    mesh.add_material(material, 1)

    return mesh


def _grid_3d(dx, dy, dz, order):
    """Generate 3D structured grid."""

    # Internal functions
    def meshgrid(x, y, z, indexing="ij", order=order):
        X, Y, Z = np.meshgrid(x, y, z, indexing=indexing)
        return X.ravel(order), Y.ravel(order), Z.ravel(order)

    def mesh_vertices(i, j, k):
        return [
            [i, j, k],
            [i + 1, j, k],
            [i + 1, j + 1, k],
            [i, j + 1, k],
            [i, j, k + 1],
            [i + 1, j, k + 1],
            [i + 1, j + 1, k + 1],
            [i, j + 1, k + 1],
        ]

    # Grid
    nx, ny, nz = len(dx), len(dy), len(dz)
    xyz_shape = [nx + 1, ny + 1, nz + 1]
    ijk_shape = [nx, ny, nz]
    X, Y, Z = meshgrid(*[np.cumsum(np.r_[0, ar]) for ar in [dx, dy, dz]])
    I, J, K = meshgrid(*[np.arange(n) for n in ijk_shape])

    # Points and cells
    points = [[x, y, z] for x, y, z in zip(X, Y, Z)]
    cells = [
        [
            np.ravel_multi_index(vertex, xyz_shape, order=order)
            for vertex in mesh_vertices(i, j, k)
        ]
        for i, j, k in zip(I, J, K)
    ]

    # Reorder cells from top to bottom
    if order == "F":
        cells = cells[::-1]

    n1 = nz if order == "F" else nx * ny
    n2 = nx * ny if order == "F" else nz
    for i in range(n1):
        i1 = i * n2
        i2 = i1 + n2
        cells[i1:i2] = cells[i2 - 1 : i1 - 1 : -1] if i > 0 else cells[i2 - 1 :: -1]

    return (
        np.array(points, dtype=float),
        [CellBlock("hexahedron", np.array(cells))],
    )


def _grid_2d(dx, dy, order):
    """Generate 2D structured grid."""

    # Internal functions
    def meshgrid(x, y, indexing="ij", order=order):
        X, Y = np.meshgrid(x, y, indexing=indexing)
        return X.ravel(order), Y.ravel(order)

    def mesh_vertices(i, j):
        return [
            [i, j],
            [i + 1, j],
            [i + 1, j + 1],
            [i, j + 1],
        ]

    # Grid
    nx, ny = len(dx), len(dy)
    xy_shape = [nx + 1, ny + 1]
    ij_shape = [nx, ny]
    X, Y = meshgrid(*[np.cumsum(np.r_[0, ar]) for ar in [dx, dy]])
    I, J = meshgrid(*[np.arange(n) for n in ij_shape])

    # Points and cells
    points = [[x, y] for x, y in zip(X, Y)]
    cells = [
        [
            np.ravel_multi_index(vertex, xy_shape, order=order)
            for vertex in mesh_vertices(i, j)
        ]
        for i, j in zip(I, J)
    ]

    return np.array(points, dtype=float), [CellBlock("quad", np.array(cells))]
