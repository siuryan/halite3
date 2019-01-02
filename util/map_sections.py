import hlt
from hlt import Position
import random

def get_section_values(ship, game_map):
    section_values = []
    for i in range(0, 8):
        section_values.append([0, 0, 0, 0, 0, 0, 0, 0])

    for x in range(-4, 4):
        for y in range(-4, 4):
            start_x = x * game_map.width / 8 + ship.position.x
            start_y = y * game_map.height / 8 + ship.position.y
            end_x = (x + 1) * game_map.width / 8 + ship.position.x
            end_y = (y + 1) * game_map.height / 8 + ship.position.y
            for section_x in range(int(start_x), int(end_x)):
                for section_y in range(int(start_y), int(end_y)):
                    if x > 0 and y > 0 and ship.id % 4 == 0:
                        section_values[x][y] += 10
                    elif x < 0 and y > 0 and ship.id % 4 == 1:
                        section_values[x][y] += 10
                    elif x < 0 and y < 0 and ship.id % 4 == 2:
                        section_values[x][y] += 10
                    elif x > 0 and y < 0 and ship.id % 4 == 3:
                        section_values[x][y] += 10
                    section_values[x][y] += 1.0 * (game_map[Position(section_x, section_y)].halite_amount) / (game_map.calculate_distance(ship.position, Position(section_x, section_y)) + 1)**2
    return section_values

def max_dest(section_values, sections_exploring, width, height, shipyard_position):
    max = 0
    for x in range(0, 8):
        for y in range(0, 8):
            if sections_exploring[x][y] == -1 and section_values[x][y] > max:
                max_x = x
                max_y = y
                max = section_values[x][y]
    ret_position = Position(max_x * width / 8 + random.randint(-4, 4), max_y * width / 8 + random.randint(-4, 4))
    if ret_position.x == shipyard_position.x:
        ret_position.x += random.randint(1, 5)
    if ret_position.y == shipyard_position.y:
        ret_position.y += random.randint(1, 5)
    return ret_position, max_x, max_y
