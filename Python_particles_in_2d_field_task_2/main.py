import os
os.environ['PROJ_LIB'] = '/home/etsu/miniconda2/envs/particles/share/proj'

import logging
import pandas as pd
from scipy.interpolate import LinearNDInterpolator
from pyproj import transform, Proj

from particles.save import save_animation, save_csv
from particles.state import *
from particles.utils import transform_states, get_point_types, type_colors, Continent

# Настроим логгирование
logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

# Зададим константы
NUM_ITER = 24*2
STEP = 3600  # с
SEED = 42

Uw, Vw = 100, 100  # см/с
W = np.array([Uw, Vw]).reshape(2, 1)

# Системы координат
WGS84_CRS = Proj(init="EPSG:4326")
LOCAL_CRS = Proj(init="EPSG:2463")


CONTINENT_BUFFER = 5000  # м


def main_1():
    logger.debug(
        '\n#############################\n'
        'Параметры:\n'
        '  Число итераций:\t{}\n'
        '  Шаг итерации, сек:\t{}\n'
        '#############################'.format(NUM_ITER, STEP)
    )
    logger.debug('Готовим данные для модели')
    lonlat, current_velocity = get_current_data('6.csv')
    # Конвертируем в метры
    xy = np.vstack(transform(WGS84_CRS, LOCAL_CRS, lonlat[:, 0], lonlat[:, 1])).T
    # Получим границы данных
    bounds = np.hstack([xy.min(axis=0), xy.max(axis=0)])
    bounds_lonlat = np.hstack([lonlat.min(axis=0), lonlat.max(axis=0)])
    # Создадим функцию интерполяции данных
    interpolate_current_velocity = LinearNDInterpolator(xy, current_velocity)
    # Получим типы точек
    point_types = get_point_types('Particles 1.xlsx')

    logger.debug('Запускаем симуляцию')
    states = run(
        init_state_func=init_state_1,
        get_state_func=get_state_1,
        current_velocity_func=interpolate_current_velocity,
        point_types=point_types,
        num_iter=NUM_ITER,
        step=STEP,
        bounds=bounds,
        weights=W,
        random_state=np.random.RandomState(SEED),
    )

    # Конвертируем в градусы
    states = transform_states(states, LOCAL_CRS, WGS84_CRS)

    logger.debug('Сохраняем анимацию')
    save_animation('out1.mp4', lonlat, current_velocity, states, point_types, NUM_ITER, STEP)

    logger.debug('Сохраняем результаты в файл')
    save_csv('out1.csv', states, point_types, bounds_lonlat)


def main_2():
    logger.debug(
        '\n#############################\n'
        'Параметры:\n'
        '  Число итераций:\t{}\n'
        '  Шаг итерации, сек:\t{}\n'
        '  Ширина прибрежной зоны, м:\t{}\n'
        '#############################'.format(NUM_ITER, STEP, CONTINENT_BUFFER)
    )
    logger.debug('Готовим данные для модели')
    lonlat, current_velocity = get_current_data('6.csv')
    # Конвертируем в метры
    xy = np.vstack(transform(WGS84_CRS, LOCAL_CRS, lonlat[:, 0], lonlat[:, 1])).T
    # Получим границы данных
    bounds = np.hstack([xy.min(axis=0), xy.max(axis=0)])
    bounds_lonlat = np.hstack([lonlat.min(axis=0), lonlat.max(axis=0)])
    # Создадим функцию интерполяции данных
    interpolate_current_velocity = LinearNDInterpolator(xy, current_velocity)
    # Получим типы точек
    point_types = get_point_types('Particles 2.xlsx')
    # Добавим новые типы и сгенерируем заново цвета
    new_point_types = point_types.copy()
    new_point_types.index += 10
    new_point_types.number = 0
    point_types = pd.concat([point_types, new_point_types], axis='rows')
    point_types.reset_index(inplace=True)
    point_types.color = type_colors(point_types.reset_index().type).values
    point_types.set_index('type', inplace=True)

    logger.debug('Запускаем симуляцию')
    fragmentator = ParticleFragmentator(Continent(bounds_lonlat, CONTINENT_BUFFER, LOCAL_CRS), STEP)
    states = run(
        init_state_func=init_state_1,
        get_state_func=get_state_2,
        current_velocity_func=interpolate_current_velocity,
        point_types=point_types,
        num_iter=NUM_ITER,
        step=STEP,
        bounds=bounds,
        weights=W,
        random_state=np.random.RandomState(SEED),
        fragmentator=fragmentator,
    )

    # Конвертируем в градусы
    states = transform_states(states, LOCAL_CRS, WGS84_CRS)

    logger.debug('Сохраняем анимацию')
    save_animation('out2.mp4', lonlat, current_velocity, states, point_types, NUM_ITER, STEP)

    logger.debug('Сохраняем результаты в файл')
    save_csv('out2.csv', states, point_types, bounds_lonlat)


if __name__ == '__main__':
    # logger.info('Блок 1')
    # main_1()

    logger.info('Блок 2')
    main_2()

    # logger.info('Блок 3')
    # main_3()
