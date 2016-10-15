app_width = 1800  # Width of the screen

app_height = 900  # Height of the screen

board_width = app_height  # Width of the tile board

board_height = app_height  # Height of the tile board

tiles_per_row = 100  # Amount of rows and columns of tiles

tile_num = tiles_per_row ** 2  # Amount of tiles on the board (must be a square number)

tile_width = board_width / tiles_per_row  # Width and height of a tile

init_creature_num = 10  # Amount of creatures created when application starts

creatures = []

def rgb_to_hex(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)
