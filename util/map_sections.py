import hlt
from hlt import Position

def get_section_values(me, game_map):
    section_values = []
    for i in range(0, 8):
        section_values.append([0, 0, 0, 0, 0, 0, 0, 0])

    for x in range(0, 8):
        for y in range(0, 8):
            start_x = x * game_map.width / 8
            start_y = y * game_map.height / 8
            end_x = (x + 1) * game_map.width / 8
            end_y = (y + 1) * game_map.height / 8
            for section_x in range(int(start_x), int(end_x)):
                for section_y in range(int(start_y), int(end_y)):
                    section_values[x][y] += 1.0 * (game_map[Position(section_x, section_y)].halite_amount) / (game_map.calculate_distance(me.shipyard.position, Position(section_x, section_y)) + 1)**(0.5)
    return section_values

def max_dest(section_values, sections_exploring, width, height):
    max = 0
    for x in range(0, 8):
        for y in range(0, 8):
            if sections_exploring[x][y] == -1 and section_values > max:
                max_x = x
                max_y = y
    return Position(x * width, y * height), x, y
