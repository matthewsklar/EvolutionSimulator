import math


app_width = 1800  # Width of the screen

app_height = 900  # Height of the screen

board_width = app_height  # Width of the tile board

board_height = app_height  # Height of the tile board

tiles_per_row = 100  # Amount of rows and columns of tiles

tile_num = tiles_per_row ** 2  # Amount of tiles on the board (must be a square number)

tile_width = board_width / tiles_per_row  # Width and height of a tile

init_creature_num = 100  # Amount of creatures created when application starts

creatures = []  # List of creatures currently alive

tiles = []  # List of tiles

tile_update = []  # A list of Creatures created when the application begins

birth_food = 30  # A number representing the amount of food a Creature is born with

birth_water = 30  # A number representing the amount of water a Creature is born with

mutation_rate = .1  # A float representing the chance of a mutation on a given weight at birth


def rgb_to_hex(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)


def get_tile(x, y):
    x_tile = clamp(math.floor(x / tile_width), 0, tiles_per_row)
    y_tile = clamp(math.floor(y / tile_width), 0, tiles_per_row - 1)

    position = clamp(x_tile + y_tile * tiles_per_row, 0, tile_num - 1)

    return tiles[position]


def clamp(n, min_n, max_n):
    return max(min(max_n, n), min_n)
