from functools import partial

import pyproj
import numpy as np
import pandas as pd
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
from shapely import ops
from shapely.geometry import Point, MultiPolygon, Polygon

WGS84_CRS = pyproj.Proj(init="EPSG:4326")


def transform_geometry(geometry, from_proj, to_proj):
    """Изменение проекции для геометрии shapely"""
    if not isinstance(from_proj, pyproj.Proj):
        from_proj = pyproj.Proj(from_proj)
    if not isinstance(to_proj, pyproj.Proj):
        to_proj = pyproj.Proj(to_proj)
    project = partial(
        pyproj.transform,
        from_proj,
        to_proj,
    )
    return ops.transform(project, geometry)


def transform_states(states, from_crs, to_crs):
    states.copy()
    for iteration in range(states.shape[0]):
        states[iteration, :, 0], states[iteration, :, 1] = pyproj.transform(
            from_crs,
            to_crs,
            states[iteration, :, 0],
            states[iteration, :, 1]
        )
    return states


def type_colors(types):
    scalar_map = mpl.cm.ScalarMappable(
        cmap='jet',
        norm=mpl.colors.Normalize(
            vmin=types.min(),
            vmax=types.max()
        )
    )
    return types.apply(lambda type_: scalar_map.to_rgba(type_))


def get_point_types(filename):
    """Типы точек из файла"""
    point_types = pd.read_excel(filename)
    point_types.columns = ['type', 'number', 'speed_param']
    point_types['color'] = type_colors(point_types.type)
    point_types.set_index('type', inplace=True)
    return point_types


def expand_types(point_types, types_array=None):
    if types_array is None:
        types_array = np.hstack([np.ones(row.number, dtype=int) * p_type for p_type, row in point_types.iterrows()])
    types_array = types_array.ravel()
    return point_types.loc[types_array]


class Continent(object):
    def __init__(self, bounds_lonlat, buffer, local_crs):
        self.buffer = buffer
        self.local_crs = local_crs
        m = Basemap(
            llcrnrlon=bounds_lonlat[0],
            llcrnrlat=bounds_lonlat[1],
            urcrnrlon=bounds_lonlat[2],
            urcrnrlat=bounds_lonlat[3],
            epsg="4326",
            resolution='h',
        )
        continent = MultiPolygon([Polygon(zip(*xy)) for xy in m.coastpolygons])
        self.continent = transform_geometry(continent, WGS84_CRS, local_crs)
        self.continent_buffer = self.continent.buffer(self.buffer)

    def is_near(self, xy):
        return np.array([self.continent_buffer.contains(Point(coords)) for coords in xy])
