from pygame.rect import Rect
from pygame.surface import Surface
from typing import final

from dna_engine.tilemaps.tile import Tile

@final
class TileMap:
    def __init__(self, world, grid_width : int, grid_height : int, pixels_apart: int) -> None:
        self.__world = world
        self.__pixel_difference = max(0, pixels_apart)
        self.__tiles = [[None for i in range(max(0, grid_height))] for j in range(max(0, grid_width))]
        self.__tile_width = (self.__world.get_width() / grid_width) - pixels_apart
        self.__tile_height = (self.__world.get_height() / grid_height) - pixels_apart


    def __add_tile(self, tile : Tile, grid_x : int, grid_y : int) -> None:
        if grid_x >= 0 and grid_y >= 0 and grid_x < len(self.__tiles) and grid_y < len(self.__tiles[grid_x]):
            self.__tiles[grid_x][grid_y] = tile
            tile._Tile__set_dimensions(self.__tile_width, self.__tile_height)
            tile.set_position((self.__pixel_difference / 2) + grid_x * (self.__tile_width + self.__pixel_difference), (self.__pixel_difference / 2) + grid_y * (self.__tile_height + self.__pixel_difference))


    def __remove_tile(self, tile : Tile) -> None:
        for i in range(0, len(self.__tiles)):
            for j in range(0, len(self.__tiles[i])):
                if self.__tiles[i][j] is not None and self.__tiles[i][j] == tile:
                    self.__tiles[i][j] = None
                    return
                    

    def __get_tile_in_grid(self, grid_x : int, grid_y : int) -> Tile:
        return self.__tiles[grid_x][grid_y]
    

    def __get_tile_on_screen(self, screen_x : float, screen_y : float) -> Tile:
        return self.__tiles[int(screen_x / (self.__tile_width + self.__pixel_difference))][int(screen_y / (self.__tile_height + self.__pixel_difference))]
    

    def __get_grid_position_from_screen_position(self, screen_x : float, screen_y : float) -> tuple[float, float]:
        return [int(screen_x / (self.__tile_width + self.__pixel_difference)), int(screen_y / (self.__tile_height + self.__pixel_difference))]


    def __get_tiles_overlapping_in_area(self, tile_type : type[Tile], bounds : Rect) -> list[Tile]:
        top_left = self.__get_grid_position_from_screen_position(bounds.x, bounds.y)
        bottom_right = self.__get_grid_position_from_screen_position(bounds.bottomright[0], bounds.bottomright[1])
        tiles_found = []
        for i in range(top_left[0], bottom_right[0] + 1):
            for j in range(top_left[1], bottom_right[1] + 1):
                if i < len(self.__tiles) and j < len(self.__tiles[i]):
                    if self.__tiles[i][j] is not None and type(self.__tiles[i][j]) is tile_type:
                        tiles_found.append(self.__tiles[i][j])

        return tiles_found



    def __update(self, delta_time : float) -> None:
        for i in range(0, len(self.__tiles)):
            for j in range(0, len(self.__tiles[i])):
                if self.__tiles[i][j] is not None:
                    self.__tiles[i][j].update(delta_time)
    
    def __render(self, render_target : Surface) -> None:
        for i in range(0, len(self.__tiles)):
            for j in range(0, len(self.__tiles[i])):
                if self.__tiles[i][j] is not None:
                    self.__tiles[i][j].render(render_target)
        
