import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
import itertools
from enum import Enum


class Cell(Enum):
    empty = 0
    road = 1
    car = 2
    green = 3
    red = 4


def is_clear_crossroads(field, n):
    indexes = [n // 2 - 2, n // 2 - 1, n // 2, n // 2 + 1]
    cells = list(itertools.product(indexes, repeat=2))
    return all([field[*cell] != Cell.car.value for cell in cells])


def change_field(field, new_field, vertical_tl, horizontal_tl, next_green_vertical_tl, n):
    below_horisontal = n // 2 + 1
    above_horisontal = n // 2 - 2
    right_vertical = n // 2 + 1
    left_vertical = n // 2 - 2

    moved_cars = set()
    crossroads = list(itertools.product([n // 2, n // 2 - 1], repeat=2))

    for pos in crossroads:
        i, j = pos
        if field[i, j] == Cell.car.value and pos not in moved_cars and vertical_tl:
            if j == n // 2:
                i_ahead = (i - 1) % n
            elif j == n // 2 - 1:
                i_ahead = (i + 1) % n
            if field[i_ahead, j] != Cell.car.value:
                new_field[i_ahead, j] = Cell.car.value
                new_field[i, j] = Cell.road.value
                moved_cars.add(pos)
        elif field[i, j] == Cell.car.value and pos not in moved_cars and horizontal_tl:
            if i == n // 2:
                j_ahead = (j + 1) % n
            elif i == n // 2 - 1:
                j_ahead = (j - 1) % n
            if field[i, j_ahead] != Cell.car.value:
                new_field[i, j_ahead] = Cell.car.value
                new_field[i, j] = Cell.road.value
                moved_cars.add(pos)
        elif field[i, j] == Cell.car.value and pos not in moved_cars and not vertical_tl and not horizontal_tl and not next_green_vertical_tl:
            if j == n // 2:
                i_ahead = (i - 1) % n
            elif j == n // 2 - 1:
                i_ahead = (i + 1) % n
            if field[i_ahead, j] != Cell.car.value:
                new_field[i_ahead, j] = Cell.car.value
                new_field[i, j] = Cell.road.value
                moved_cars.add(pos)
        elif field[i, j] == Cell.car.value and pos not in moved_cars and not vertical_tl and not horizontal_tl and next_green_vertical_tl:
            if i == n // 2:
                j_ahead = (j + 1) % n
            elif i == n // 2 - 1:
                j_ahead = (j - 1) % n
            if field[i, j_ahead] != Cell.car.value:
                new_field[i, j_ahead] = Cell.car.value
                new_field[i, j] = Cell.road.value
                moved_cars.add(pos)

    for i in range(n):
        j = n // 2
        i_ahead = (i - 1) % n
        pos = (i, j)
        if pos not in crossroads and pos not in moved_cars and field[i, j] == Cell.car.value and field[i_ahead, j] != Cell.car.value and \
                (i_ahead != below_horisontal or (i_ahead == below_horisontal and vertical_tl)):
            new_field[i_ahead, j] = Cell.car.value
            new_field[i, j] = Cell.road.value
            moved_cars.add((i, j))

    for i in range(n):
        j = n // 2 - 1
        i_ahead = (i + 1) % n
        pos = (i, j)

        if pos not in crossroads and pos not in moved_cars and field[i, j] == Cell.car.value and field[i_ahead, j] != Cell.car.value and \
                (i_ahead != above_horisontal or (i_ahead == above_horisontal and vertical_tl)):
            new_field[i_ahead, j] = Cell.car.value
            new_field[i, j] = Cell.road.value
            moved_cars.add((i, j))

    for j in range(n):
        i = n // 2 - 1
        j_ahead = (j - 1) % n
        pos = (i, j)

        if pos not in crossroads and pos not in moved_cars and field[i, j] == Cell.car.value and field[i, j_ahead] != Cell.car.value and \
                (j_ahead != right_vertical or (j_ahead == right_vertical and horizontal_tl)):
            new_field[i, j_ahead] = Cell.car.value
            new_field[i, j] = Cell.road.value
            moved_cars.add((i, j))

    for j in range(n):
        i = n // 2
        j_ahead = (j + 1) % n
        pos = (i, j)

        if pos not in crossroads and pos not in moved_cars and field[i, j] == Cell.car.value and field[i, j_ahead] != Cell.car.value and \
                (j_ahead != left_vertical or (j_ahead == left_vertical and horizontal_tl)):
            new_field[i, j_ahead] = Cell.car.value
            new_field[i, j] = Cell.road.value
            moved_cars.add((i, j))

    if vertical_tl:
        new_field[n // 2 - 4, n // 2 - 3] = Cell.green.value
        new_field[n // 2 + 3, n//2 + 2] = Cell.green.value
    else:
        new_field[n // 2 - 4, n // 2 - 3] = Cell.red.value
        new_field[n // 2 + 3, n//2 + 2] = Cell.red.value

    if horizontal_tl:
        new_field[n // 2 + 2, n // 2 - 4] = Cell.green.value
        new_field[n // 2 - 3, n // 2 + 3] = Cell.green.value
    else:
        new_field[n // 2 + 2, n // 2 - 4] = Cell.red.value
        new_field[n // 2 - 3, n // 2 + 3] = Cell.red.value

    return new_field


def main():
    np.random.seed(42)
    n = 50
    tl_steps_to_change = 20
    tl_step = 0
    density = 0.15
    time = 500
    pause = 0.0001
    vertical_tl = True
    next_green_vertical_tl = False
    horizontal_tl = not vertical_tl
    await_tl = ''

    indexes = [n // 2 - 2, n // 2 - 1, n // 2, n // 2 + 1]
    cells = set(itertools.product(indexes, repeat=2))
    field = np.array([[Cell.empty.value if (i != n//2-1 and i != n//2) else Cell.road.value for i in range(n)]
                      if (j != n//2-1 and j != n//2) else [Cell.road.value for _ in range(n)] for j in range(n)])
    road_cells_cnt = 4 * n - 4
    cnt_of_cars = round(road_cells_cnt * density)

    x, y = np.where(field == Cell.road.value)
    positions = np.array(tuple(zip(x, y)))
    positions = [position
                 for position in positions if tuple(position) not in cells]
    cnt = [i for i in range(len(positions))]
    cars = np.random.choice(cnt, cnt_of_cars)
    for car in cars:
        x, y = positions[car]
        field[x, y] = Cell.car.value

    if vertical_tl:
        field[n // 2 - 4, n // 2 - 3] = Cell.green.value
        field[n // 2 + 3, n//2 + 2] = Cell.green.value
    else:
        field[n // 2 - 4, n // 2 - 3] = Cell.red.value
        field[n // 2 + 3, n//2 + 2] = Cell.red.value

    if horizontal_tl:
        field[n // 2 + 2, n // 2 - 4] = Cell.green.value
        field[n // 2 - 3, n // 2 + 3] = Cell.green.value
    else:
        field[n // 2 + 2, n // 2 - 4] = Cell.red.value
        field[n // 2 - 3, n // 2 + 3] = Cell.red.value

    new_field = field.copy()

    colors = ['honeydew', 'silver', 'black', 'green', 'red']
    cmap = mcolors.ListedColormap(colors)
    plt.ion()
    fig, ax = plt.subplots(figsize=(12, 12))
    img = ax.matshow(field, cmap=cmap)

    for _ in range(time):
        field = new_field.copy()

        img.set_data(field)
        ax.set_title(
            f'Traffic lights CA model | time: {tl_step}')
        fig.canvas.draw()
        plt.pause(pause)

        new_field = change_field(
            field, new_field, vertical_tl, horizontal_tl, next_green_vertical_tl, n)

        is_clear = is_clear_crossroads(new_field, n)
        tl_step += 1

        if tl_step % tl_steps_to_change == 0 and horizontal_tl:
            horizontal_tl = False
            next_green_vertical_tl = True
            await_tl = "vertical_tl"
        elif tl_step % tl_steps_to_change == 0 and vertical_tl:
            vertical_tl = False
            next_green_vertical_tl = False
            await_tl = "horizontal_tl"

        if await_tl == "vertical_tl" and is_clear:
            vertical_tl = True
            await_tl = ''
        elif await_tl == "horizontal_tl" and is_clear:
            horizontal_tl = True
            await_tl = ''

    plt.ioff()
    plt.show()


if __name__ == '__main__':
    main()
