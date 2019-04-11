import os
os.environ['PROJ_LIB'] = '/home/etsu/miniconda2/envs/particles/share/proj'
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.interpolate import LinearNDInterpolator
from pyproj import transform, Proj


# Зададим константы
NUM_PARTICLES = 100
NUM_ITER = 24*7
STEP = 3600  # sec
SEED = 42

Uw, Vw = 100, 100  # см/с
W = np.array([Uw, Vw])

# Системы координат
WGS84_CRS = Proj(init="EPSG:4326")
LOCAL_CRS = Proj(init="EPSG:2463")


def init_state(xy, speed_param, get_current_velocity):
    """Инициализация состояния системы"""
    velocity = get_velocity(get_current_velocity(xy), speed_param)
    return np.hstack([xy, velocity])


def get_state(state_prev, step, speed_param, get_current_velocity):
    """Возвращае текущее состояние по предыдущему"""
    xy_prev = state_prev[:, :2]
    velocity_prev = state_prev[:, 2:]
    xy_cur = xy_prev + step*velocity_prev
    velocity_cur = get_velocity(get_current_velocity(xy_cur), speed_param)
    states_cur = np.hstack([xy_cur, velocity_cur])
    return states_cur


def get_velocity(current_velocity, speed_param):
    """Возвращает скорость частицы"""
    C = current_velocity
    velocity = (C + speed_param * W) / (1 + speed_param)
    velocity *= 0.01  # переведем из см/с в м/с
    return velocity


def to_wgs84_states(p_type_states):
    p_type_states = p_type_states.copy()
    for states in p_type_states.values():
        for iteration in range(states.shape[0]):
            states[iteration, :, 0], states[iteration, :, 1] = transform(
                LOCAL_CRS,
                WGS84_CRS,
                states[iteration, :, 0],
                states[iteration, :, 1]
            )
    return p_type_states


def get_current_data(filename):
    """Получаем данные из файла"""
    data = np.genfromtxt(filename, delimiter=';', skip_header=True)
    data[data == -999] = np.nan
    lonlat, current_velocity = data[:, 1::-1], data[:, 2:]
    return lonlat, current_velocity


def get_point_types(filename):
    """Типы точек из файла"""
    point_types = pd.read_excel(filename)
    point_types.columns = ['type', 'number', 'speed_param']
    # присвоим каждому типу свой цвет
    scalar_map = mpl.cm.ScalarMappable(
        cmap='jet',
        norm=mpl.colors.Normalize(
            vmin=point_types.type.min(),
            vmax=point_types.type.max()
        )
    )
    point_types['color'] = point_types.type.apply(lambda type_: scalar_map.to_rgba(type_))
    point_types.set_index('type', inplace=True)
    return point_types


def get_init_positions(bounds, point_types):
    # точки расположены в виде прямоугольника
    x_min, y_min, x_max, y_max = bounds
    rs = np.random.RandomState(SEED)
    x_delta = x_max - x_min
    xmin_, xmax_ = x_min + 0.2 * x_delta, x_min + 0.4 * x_delta
    y_delta = y_max - y_min
    ymin_, ymax_ = y_min + 0.4 * y_delta, y_min + 0.6 * y_delta
    n = np.ceil(np.sqrt(point_types.number.sum())).astype(int)
    xm, ym = np.meshgrid(np.linspace(xmin_, xmax_, n), np.linspace(ymin_, ymax_, n))
    xy_init = np.vstack([xm.ravel(), ym.ravel()]).T
    rs.shuffle(xy_init)  # перемешаем, чтобы точки чередовались по типу
    return xy_init


def run(xy_init, point_types, get_current_velocity):
    """ Запустим расчет"""
    p_type_states = {}
    for i, (p_type, row) in enumerate(point_types.iterrows()):
        num_points = row.number
        speed_param = row.speed_param
        states = np.ones([NUM_ITER, num_points, 4], dtype=float) * np.nan
        states[0, :, :] = init_state(xy_init[i * num_points: (i + 1) * num_points], speed_param, get_current_velocity)
        for n in range(1, NUM_ITER):
            states[n, :, :] = get_state(states[n - 1, :, :], STEP, speed_param, get_current_velocity)
        p_type_states[p_type] = states
    return p_type_states


def animate(filename, bounds_lonlat, lonlat, current_velocity, point_types, p_type_states):
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
    for p_type, states in p_type_states.items():
        color = point_types.loc[p_type, 'color']
        for i in range(states.shape[1]):
            lines.append(ax.plot([], [], color=color, linestyle='', marker='o')[0])

    # инициализация линий для анимации
    def init():
        for line in lines:
            line.set_data([], [])
        return lines

    # обновлении линий на каждой итерации
    def update(frame):
        ax.set_title('{}, час'.format(frame * STEP // 3600))
        line_idx = 0
        for p_type, states in p_type_states.items():
            for i in range(states.shape[1]):
                x = states[frame:frame + 1, i, 0]
                y = states[frame:frame + 1, i, 1]
                lines[line_idx].set_data(x, y)
                line_idx += 1
        return lines

    # cоздадим и сохраним анимацию
    ani = animation.FuncAnimation(
        fig,
        update,
        frames=NUM_ITER - 1,
        init_func=init,
        interval=100,
    )
    ani.save(filename, writer=animation.FFMpegFileWriter(bitrate=-1))
    print('Created %s' % filename)


def states_to_csv(filename, p_type_states, bounds_lonlat):
    # выведем все данные в файл
    all_points = []
    point_idx = 0
    for p_type, states in p_type_states.items():
        for i in range(states.shape[1]):
            df = pd.DataFrame(states[:, i, :], columns=['lon', 'lat', 'u', 'v'])
            df['point'] = point_idx
            df['point_type'] = p_type
            df.index.name = 'num_iter'
            df.reset_index(inplace=True)
            all_points.append(df)
            point_idx += 1

    df = pd.concat(all_points, axis='rows')
    df.loc[(df.lon < bounds_lonlat[0]) | (df.lon > bounds_lonlat[2]), 'lat'] = -999
    df.loc[(df.lat < bounds_lonlat[1]) | (df.lat > bounds_lonlat[3]), 'lon'] = -999
    df.u *= 100
    df.v *= 100
    df.to_csv(filename, index=False)
    print('Created %s' % filename)


def main():
    # Получим данные
    lonlat, current_velocity = get_current_data('6.csv')

    # Конвертируем в метры
    xy = np.vstack(transform(WGS84_CRS, LOCAL_CRS, lonlat[:, 0], lonlat[:, 1])).T

    # Получим гранницы данных
    bounds = np.hstack([xy.min(axis=0), xy.max(axis=0)])
    bounds_lonlat = np.hstack([lonlat.min(axis=0), lonlat.max(axis=0)])

    # Создадим функцию интерполяции данных
    get_current_velocity = LinearNDInterpolator(xy, current_velocity)

    # Получим типы точек
    point_types = get_point_types('Particles 1.xlsx')

    # Начальные позиции точек
    xy_init = get_init_positions(bounds, point_types)

    # Запустим расчет
    p_type_states = run(xy_init, point_types, get_current_velocity)

    # Конвертируем в градусы
    p_type_states = to_wgs84_states(p_type_states)

    # Сохраним анимацию
    animate('out.mp4', bounds_lonlat, lonlat, current_velocity, point_types, p_type_states)

    # Сохраним результаты в файл
    states_to_csv('out.csv', p_type_states, bounds_lonlat)


if __name__ == '__main__':
    main()
