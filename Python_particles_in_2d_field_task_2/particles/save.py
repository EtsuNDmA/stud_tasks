import logging

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable

from particles.utils import expand_types

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)


def save_animation(filename, lonlat, current_velocity, states, point_types, num_iter, step):
    bounds_lonlat = np.hstack([lonlat.min(axis=0), lonlat.max(axis=0)])
    # создаем рисунок
    fig, ax = plt.subplots(figsize=(12, 6))

    # добавляем континенты
    m = Basemap(
        llcrnrlon=bounds_lonlat[0] - 0.03,
        llcrnrlat=bounds_lonlat[1] - 0.03,
        urcrnrlon=bounds_lonlat[2] + 0.03,
        urcrnrlat=bounds_lonlat[3] + 0.03,
        epsg="4326",
        resolution='h',
    )
    m.drawcoastlines()
    m.fillcontinents()
    m.drawmapboundary()

    # добавляем поле скоростей
    q = ax.quiver(
        lonlat[::10, 0],
        lonlat[::10, 1],
        current_velocity[::10, 0],
        current_velocity[::10, 1],
        np.linalg.norm(current_velocity, axis=1),
        scale=200,
        scale_units='width',
        cmap='winter',
    )

    # добавляем colorbar
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    plt.colorbar(q, cax=cax, label='Скорость, м/с')
    lines = []
    colors = expand_types(point_types).color
    for point_ind in range(states.shape[1]):
        color = colors.iloc[point_ind]
        lines.append(ax.plot([], [], color=color, linestyle='', marker='o')[0])

    # инициализация линий для анимации
    def init():
        for line in lines:
            line.set_data([], [])
        return lines

    # обновлении линий на каждой итерации
    def update(frame):
        ax.set_title('{}, час'.format(frame * step // 3600))

        for point_ind, line in enumerate(lines):
            x, y = states[frame, point_ind, :2]
            line.set_data(x, y)
        return lines

    # cоздадим и сохраним анимацию
    ani = animation.FuncAnimation(
        fig,
        update,
        frames=num_iter - 1,
        init_func=init,
        interval=100,
    )
    ani.save(filename, writer=animation.FFMpegFileWriter(bitrate=-1))
    logger.debug('Создан файл %s' % filename)


def save_csv(filename, states, point_types, bounds_lonlat):
    # выведем все данные в файл
    all_points = []
    for point_ind in range(states.shape[1]):
        df = pd.DataFrame(states[:, point_ind, :], columns=['lon', 'lat', 'u', 'v', 'point_type'])
        df['point'] = point_ind
        df.index.name = 'num_iter'
        df.reset_index(inplace=True)
        all_points.append(df)

    df = pd.concat(all_points, axis='rows')
    df.loc[(df.lon < bounds_lonlat[0]) | (df.lon > bounds_lonlat[2]), 'lat'] = -999
    df.loc[(df.lat < bounds_lonlat[1]) | (df.lat > bounds_lonlat[3]), 'lon'] = -999
    df.u *= 100
    df.v *= 100
    df.to_csv(filename, index=False)
    logger.debug('Создан файл %s' % filename)
