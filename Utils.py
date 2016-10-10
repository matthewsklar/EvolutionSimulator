# Width of the screen
app_width = 1800

# Height of the screen
app_height = 900

# Width of the tile board
board_width = app_height

# Height of the tile board
board_height = app_height

# Amount of rows and columns of tiles
tiles_per_row = 100

# Amount of tiles on the board (must be a square number)
tile_num = tiles_per_row ** 2

# Width and height of a tile
tile_width = board_width / tiles_per_row


def rgb_to_hex(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)
