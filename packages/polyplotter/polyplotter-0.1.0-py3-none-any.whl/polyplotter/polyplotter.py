import numpy as np
import shapely
from matplotlib import pyplot as plt
from shapely import wkt
from shapely.geometry import GeometryCollection, MultiPolygon, Polygon


def plotpoly(obj, verbose=False, invert_y=True):
    """Delegate plotting to the appropriate function based on the object type."""
    plot_funcs = {
        np.ndarray: plot_ndarray_poly,
        Polygon: plot_shapely_poly,
        MultiPolygon: plot_shapely_multipoly,
        GeometryCollection: plot_shapely_geometry_collection,
        dict: plot_dict,
        list: plot_list,
        str: plot_str,
        tuple: plot_tuple,
    }

    plot_func = plot_funcs.get(type(obj))

    if plot_func:
        if verbose:
            print(f"{type(obj).__name__} detected")
        plot_func(obj, verbose, invert_y)
    else:
        print(f"type {type(obj)} not expected")
        print(f"{obj=}")


def plot_ndarray_poly(arr: np.ndarray, verbose=False, invert_y=True):
    """Plot polygon from a numpy array."""
    try:
        poly = Polygon(arr)
    except Exception:
        poly = Polygon(np.concatenate(arr, axis=0))
    plot_shapely_poly(poly, invert_y)


def plot_shapely_poly(poly, verbose=False, invert_y=True):
    """Plot a shapely Polygon."""
    if invert_y:
        plt.gca().invert_yaxis()
    plt.plot(*poly.exterior.xy)
    plt.show()


def plot_shapely_multipoly(multipoly, verbose=False, invert_y=True):
    """Plot a shapely MultiPolygon."""
    if invert_y:
        plt.gca().invert_yaxis()
    for geom in multipoly.geoms:
        plt.plot(*geom.exterior.xy)

    plt.gca().axis("equal")
    plt.show()


def plot_shapely_geometry_collection(gc, verbose=False, invert_y=True):
    """Plot a shapely GeometryCollection."""
    for geom in gc.geoms:
        print("Need to plot this")


def plot_dict(obj, verbose=False, invert_y=True):
    """Plot polygons from dictionary values."""
    for _, v in obj.items():
        plotpoly(v, verbose, invert_y)


def plot_list(obj, verbose=False, invert_y=True):
    """Plot polygons from list elements."""
    try:
        for item in obj:
            plot_shapely_poly(item, invert_y)
    except TypeError:
        for item in obj:
            plotpoly(item, invert_y)


def plot_str(obj, verbose=False, invert_y=True):
    """Plot polygon from WKT string."""
    try:
        poly = wkt.loads(obj)
        plot_shapely_poly(poly, invert_y)
    except wkt.WKTReadingError as e:
        raise ValueError(f"String not wkt: {obj=}") from e


def plot_tuple(obj, verbose=False, invert_y=True):
    """Plot polygon from tuple."""
    plt.plot(*obj)
    plt.show()
