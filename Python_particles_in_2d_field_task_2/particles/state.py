import math
from collections import defaultdict

import numpy as np

from particles.utils import expand_types


def get_current_data(filename):
    """Получаем данные о течении из файла"""
    data = np.genfromtxt(filename, delimiter=';', skip_header=True)
    data[data == -999] = np.nan
    lonlat, current_velocity = data[:, 1::-1], data[:, 2:]
    return lonlat, current_velocity


def get_velocity(current_velocity, speed_params, W):
    """Возвращает скорость частицы"""
    assert current_velocity.shape[0] == speed_params.shape[0]
    velocity = (speed_params @ W.T + current_velocity) / (1 + speed_params)
    velocity *= 0.01  # переведем из см/с в м/с
    return velocity


def init_state_1(num_points, current_velocity_func, point_types, bounds=None, weights=None, random_state=None, **kwargs):
    """Инициализация состояния системы"""
    x_min, y_min, x_max, y_max = bounds
    x_delta = x_max - x_min
    xmin_, xmax_ = x_min + 0.2 * x_delta, x_min + 0.9 * x_delta
    y_delta = y_max - y_min
    ymin_, ymax_ = y_min + 0.4 * y_delta, y_min + 0.6 * y_delta
    n = np.ceil(np.sqrt(num_points)).astype(int)
    xm, ym = np.meshgrid(np.linspace(xmin_, xmax_, n), np.linspace(ymin_, ymax_, n))
    xy_init = np.vstack([xm.ravel(), ym.ravel()]).T
    random_state.shuffle(xy_init)  # перемешаем, чтобы точки чередовались по типу
    xy_init = xy_init[:num_points]  # отбросим лишние
    types_df = expand_types(point_types)
    speed_params = types_df.speed_param.values.reshape(-1, 1)
    types = types_df.index.values.reshape(-1, 1)
    velocity_init = get_velocity(current_velocity_func(xy_init), speed_params, weights)
    return np.hstack([xy_init, velocity_init, types])


def get_state_1(states, iteration, current_velocity_func, point_types, step, weights=None, **kwargs):
    """Возвращае текущее состояние по предыдущему"""
    state_prev = states[iteration-1, :, :]
    xy_prev = state_prev[:, :2]
    velocity_prev = state_prev[:, 2:4]
    xy_cur = xy_prev + step * velocity_prev
    types = state_prev[:, 4].reshape(-1, 1)
    speed_params = expand_types(point_types, types).speed_param.values.reshape(-1, 1)
    velocity_cur = get_velocity(current_velocity_func(xy_cur), speed_params, weights)
    states_cur = np.hstack([xy_cur, velocity_cur, types])
    states[iteration, :, :] = states_cur
    return states


def get_state_2(states, iteration, current_velocity_func, point_types, step,
                weights=None, fragmentator=None, **kwargs):
    """Возвращае текущее состояние по предыдущему"""
    state_prev = states[iteration-1, :, :]
    xy_prev = state_prev[:, :2]
    velocity_prev = state_prev[:, 2:4]
    xy_cur = xy_prev + step * velocity_prev
    types = state_prev[:, 4].reshape(-1, 1)
    speed_params = expand_types(point_types, types).speed_param.values.reshape(-1, 1)
    velocity_cur = get_velocity(current_velocity_func(xy_cur), speed_params, weights)
    states_cur = np.hstack([xy_cur, velocity_cur, types])
    states[iteration, :, :] = states_cur
    states = fragmentator.run(states, iteration, point_types)
    return states


class ParticleFragmentator(object):
    def __init__(self, continent, step):
        self.counter = defaultdict(float)
        self.continent = continent
        self.step = step

    def count_point_is_near_continent(self, xy):
        # Для каждой точки проверим попадает ли она в прибрежную зону
        is_near = self.continent.is_near(xy)
        for point_ind in range(xy.shape[0]):
            if is_near[point_ind]:
                # Запоминаем время пребывания в прибрежной зоне
                self.counter[point_ind] += 1 * self.step
            else:
                # Сбрасываем время пребывания в прибрежной зоне
                self.counter[point_ind] = 0.0

    def fragment(self, states, iteration, point_types):
        state = states[iteration, :, :].copy()
        new_states = states.copy()
        for point_ind in range(state.shape[0]):
            hours = self.counter[point_ind] / 3600
            point_type = state[point_ind, 4]
            if point_type == 1:
                num_new_points = round(0.21 * math.exp(0.2 * hours))
            elif point_type == 1:
                num_new_points = round(5.22 * hours**2 - 70.18 * hours + 262.51)
            elif point_type == 1:
                num_new_points = round(0.63 * hours + 5.12)
            else:
                num_new_points = 0
            if num_new_points > 0:
                parent_point_state = state[point_ind, :].copy()
                new_points_state = parent_point_state
                new_point_type = point_type + 10
                new_points_state[4] = new_point_type  # Новый тип частицы

                num_iterations, num_points, vector_length = states.shape

                new_states = np.ones([num_iterations, num_points + num_new_points, vector_length], dtype=float) * np.nan
                new_states[:iteration+1, 0:num_points, :] = states[:iteration+1, :, :]
                new_states[iteration, num_points:, :] = new_points_state
                point_types.loc[new_point_type, 'number'] += num_new_points
        return new_states

    def run(self,  states, iteration, point_types):
        self.count_point_is_near_continent(states[iteration, :, 0:2])
        states = self.fragment(states, iteration,  point_types)
        return states


def run(init_state_func,
        get_state_func,
        current_velocity_func,
        point_types,
        num_iter,
        step,
        **kwargs
        ):
    """ Запустим расчет"""
    # states - массив [NUM_ITER х NUM_PARTICLES х 5]
    # по последней оси размерностью 5 храним X, Y, Vx, Vy, point_type
    # точки расположены в виде прямоугольника

    num_points = point_types.number.sum()
    states = np.ones([num_iter, num_points, 5], dtype=float) * np.nan
    states[0, :, :] = init_state_func(
        num_points,
        current_velocity_func,
        point_types=point_types,
        **kwargs
    )

    for iteration in range(1, num_iter):
        states = get_state_func(
            states,
            iteration,
            current_velocity_func,
            point_types=point_types,
            step=step,
            **kwargs
        )
    return states
