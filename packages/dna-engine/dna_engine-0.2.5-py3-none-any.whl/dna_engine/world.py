from abc import ABC, abstractmethod

from pygame.surface import Surface
import dna_engine as dna

from dna_engine.tilemaps.tile import Tile
from dna_engine.tilemaps import TileMap
from dna_engine.background import Background as Background


class World(ABC):
    """
    The base class from which all user-defined Worlds should derive.
	- All derived World classes must implement the Start() method. 
	- Handles the updating and rendering of Actors automatically.
	- Supports simple TileMap functionality.
    """
    def __init__(self) -> None:
        self.__actors = []
        self.__text = []
        self.__game = None
        self.__background = None
        self.__tile_map = None
        
    @abstractmethod
    def _start(self) -> None:
        """
        Called automatically before the World begins. Should be overwritten to set up any derived World classes.
        """
        pass

    def _end(self) -> None:
        """
        Called automatically just before the World ends. Can be overwritten for custom clean-up functionality.
        """
        self.__actors.clear()
        self.__actors = None

        self.__text.clear()
        self.__text = None

        self.__tile_map = None

        self.__background = None


    def _update(self, delta_time : float) -> None:
        """
        Called automatically once per frame. Updates all associated Actors and Text objects. Can be overwritten for custom functionality.
        
        **Note:** When overriding in a derived class, please ensure base.Update() is still called. 
        
        :param delta_time: The amount of time, in fractions of a second, that has elapsed since the last frame of the game.
        :type delta_time: float
        """
        if self.__tile_map is not None:
            self.__tile_map._TileMap__update(delta_time)

        if self.__actors is not None:
            for actor in self.__actors:
                actor._update(delta_time)
        
        if self.__text is not None:
            for text in self.__text:
                text._update(delta_time)


    def _render(self, render_target : Surface) -> None:
        """
        Called automatically once per frame. Draws all associated Actors and Text objects. Can be overwritten for custom functionality.

        **Note:** When overriding in a derived class, please ensure base.Render() is still called.

        :param render_target: _description_
        :type render_target: Surface
        """
        if self.__background is not None:
            self.__background._Background__render(render_target)

        if self.__tile_map is not None:
            self.__tile_map._TileMap__render(render_target)

        for actor in self.__actors:
            if actor.is_visible() is True:
                actor._render(render_target)

        for text in self.__text:
            text._render(render_target)

    
    def __get_all_actors(self) -> None:
        return self.__actors
    

    def _create_tile_map(self, vertical_spaces : int, horizontal_spaces : int, pixel_gap = 0) -> None:
        """
        Creates an empty TileMap with the parameters provided.

        **Note:** Must be called before add_tile() can be used.

        :param vertical_spaces: The number of horizontal tile slots that should be created in this TileMap.
        :type vertical_spaces: int
        
        :param horizontal_spaces: The number of vertical tile slots that should be created in this TileMap.
        :type horizontal_spaces: int
        
        :param pixel_gap: The number of pixels that should be placed between each tile vertically and horizontally., defaults to 0
        :type pixel_gap: int, optional
        """
        self.__tile_map = TileMap(self, vertical_spaces, horizontal_spaces, pixel_gap)


    def add_tile(self, tile : Tile, grid_x : int, grid_y : int) -> None:
        """
        Adds a Tile object to this World's TileMap.

        **Note:** Please remember to call create_tile_map() before using this method.

        :param tile: The Tile object to be added to this World's TileMap.
        :type tile: Tile
        
        :param grid_x: The horizontal grid index to place this new Tile.
        :type grid_x: int
        
        :param grid_y: The vertical grid index to place this new Tile.
        :type grid_y: int
        
        :raises NotImplementedError: Thrown if create_tile_map() has not been called for initialisation.
        """
        try:
            self.__tile_map._TileMap__add_tile(tile, grid_x, grid_y)
        except:
            raise NotImplementedError("tile_map has not been created. Please ensure create_tile_map() has been called first.")

    
    def remove_tile(self, tile : Tile) -> None:
        """
        Removes a Tile object from this World.

        :param tile: The Tile object to be removed.
        :type tile: Tile
        :raises NotImplementedError: Thrown if create_tile_map() has not been called for initialisation.
        """
        try:
            self.__tile_map._TileMap__remove_tile(tile)
        except NotImplementedError:
            raise NotImplementedError("tile_map has not been created. Please ensure create_tile_map() has been called first.")
    
    def get_tile_at_grid_position(self, grid_x : int, grid_y : int) -> Tile:
        """
        Gets the Tile object at the given grid index, if one exists.

        :param grid_x: The horizontal grid index to check for a Tile.
        :type grid_x: int

        :param grid_y: The vertical grid index to check for a Tile.
        :type grid_y: int

        :raises NotImplementedError: Thrown if create_tile_map() has not been called for initialisation.
        
        :return: A Tile object at the given index, if one exists. Otherwise, returns 'null'.
        :rtype: Tile
        """
        try:
            return self.__tile_map.__get_tile_in_grid(grid_x, grid_y)
        except NotImplementedError:
            raise NotImplementedError("tile_map has not been created. Please ensure create_tile_map() has been called first.")


    def __get_tile_map(self) -> 'TileMap':
        try:
            return self.__tile_map
        except NotImplementedError:
            raise NotImplementedError("tile_map has not been created. Please ensure create_tile_map() has been called first.")
        


    def add_actor(self, new_actor : 'Actor', x : float, y : float) -> None:
        """
        Adds an Actor object to this World.

        :param new_actor: The Actor instance that should be added.
        :type new_actor: Actor
        
        :param x: The x-axis (horizontal) location to spawn this Actor.
        :type x: float
        
        :param y: The y-axis (vertical) location to spawn this Actor.
        :type y: float
        """
        self.__actors.append(new_actor)
        new_actor.set_position(x, y)
        new_actor._Actor__set_world(self)
        new_actor._once_added()
        

    def remove_actor(self, actor : 'Actor') -> None:
        """
        Removes an Actor object from this World.

        :param actor: The Actor that should be removed.
        :type actor: Actor
        """
        self.__actors.remove(actor)


    def add_text(self, new_text : 'Text', x : float, y : float) -> None:
        """
        Adds a Text object to this World.

        :param new_text: The Text instance that should be added.
        :type new_text: Text
        
        :param x: The x-axis (horizontal) location to spawn this Text.
        :type x: float
        
        :param y: The y-axis (vertical) location to spawn this Text.
        :type y: float
        """
        self.__text.append(new_text)
        new_text.set_position(x, y)
        new_text._Text__set_world(self)


    def remove_text(self, text : 'Text') -> None:
        """
        Removes a Text object from this World.

        :param text: The Text object to be removed.
        :type text: Text
        """
        self.__text.remove(text)


    def draw_text(self, message : str, x : float, y : float) -> None:
        """
        Draws a string to the desired x and y axis co-ordinates.

        :param message: The string of characters that should be displayed.
        :type message: str
        
        :param x: The x-axis (horizontal) location to draw this Text.
        :type x: float
        
        :param y: The y-axis (vertical) location to draw this Text.
        :type y: float
        """
        
        # If a piece of Text already exists at this location, use that text object instead of creating a new one.
        for text in self.__text:
            if text.get_x() == x and text.get_y() == y:
                text.set_message(message)
                return
            
        # Otherwise, create a new Text object
        self.add_text(dna.Text(message), x, y)


    def get_background(self) -> Background:
        """
        Gets the Background for this World.

        :return: The Background object used by this World, if one exists. Otherwise returns 'null'.
        :rtype: dna.Background
        """
        return self.__background


    def set_background(self, background_name : str) -> None:
        """
        Sets the Background image for this World.

        :param background_name: The filepath, file name and filetype of the desired image.
        :type background_name: str
        """
        self.__background = Background(self, background_name)


    def get_width(self) -> float:
        """
        Gets the pixel width of this World.

        :return: A floating-point value representing the width of this World.
        :rtype: float
        """
        return self.Game._Game__get_window_width()


    def get_height(self) -> float:
        """
        Gets the pixel height of this World.

        :return: A floating-point value representing the height of this World.
        :rtype: float
        """
        return self.Game._Game__get_window_height()
    

    @property
    def Game(self) -> dna.game.Game:
        """
        Gets the main Game instance.

        :return: The Game object responsible for handling this game project.
        :rtype: Game
        """
        return dna.Game._Game__instance