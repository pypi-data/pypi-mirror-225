from __future__ import annotations

import pygame;
from math import atan2, pi
from abc import ABC, abstractmethod
from os.path import exists as file_exists;
from typing import overload
from pygame.surface import Surface
from pygame.locals import (RLEACCEL);

from dna_engine.game import Game
from dna_engine.world import World
from dna_engine.tilemaps.tile import Tile

class Actor(ABC):
    """
    The base class from which all user-defined Actors should derive.
    - All derived Actor classes must implement the Update() method.
    - Can be positioned, scaled, rotated etc.
    - Can check for collisions with other Actor sub-classes via a variety of built-in methods.

    :param ABC: The Python Abstract Base Class.
    :type ABC: type[ABC]
    """
    def __init__(self) -> None:
        """
        The constructor for this Actor class.
        """
        self.__sprite = pygame.Surface((64,64)).convert_alpha()
        self.__sprite.fill((255,255,255, 255))
        self.__rect = self.__sprite.get_rect()
        self.__raw_image = self.__sprite
        self.__game = None
        self.__position = pygame.Vector2(0, 0)
        self.__rotation = 0
        self.__scale = 1.0
        self.__visible = True

    @abstractmethod
    def _update(self, delta_time : float) -> None:
        """
        Called automatically once per frame. Useful for functionality which should be performed for as long as this Actor exists. 

        :param delta_time: The amount of time, in fractions of a second, that has elapsed since the last frame of the game.
        :type delta_time: float
        """
        pass


    def _render(self, render_target : Surface) -> None:
        """
        Called automatically once per frame. Draws the sprite or coloured rectangle set to this Actor. Can be overwritten for custom functionality.

        :param render_target: The canvas that will be drawn to.
        :type render_target: Surface
        """
        if self.__visible is True and self.is_offscreen() is False:
            render_target.blit(self.__sprite, self.__rect)


    def _once_added(self) -> None:
        """
        Called automatically once this Actor has been added to the World. Should be overwritten for initialisation that requires access to the World.
        """
        pass


    def get_world(self) -> World:
        """
        Gets the World instance responsible for this Actor.

        :return: A World object containing the World which is handling this Actor.
        :rtype: World
        """
        return self.__world


    def get_bounds(self) -> pygame.Rect:
        """
        Gets the bounding rectangle for this Actor. The bounds are based on the size and shape of this Actor's image.

        ***Note:*** If bounds appear larger than a given image, please ensure your image has been cropped appropriately.

        :return: A rectangle object representing the bounds around this Actor.
        :rtype: pygame.Rect
        """
        return self.__rect


    def get_x(self) -> float:
        """
        Gets the current on-screen x-axis (horizontal) position of this Actor.

        :return: A floating-point value representing the horizontal location of this Actor.
        :rtype: float
        """
        return self.__position[0]
        #return self.__rect.centerx


    def get_y(self) -> float:
        """
        Gets the current on-screen y-axis (vertical) position of this Actor.

        :return: A floating-point value representing the vertical location of this Actor.
        :rtype: float
        """
        return self.__position[1]
        #return self.__rect.centery
    

    def get_width(self) -> float:
        """
        Gets the width of this Actor's image.

        :return: A floating-point value representing the pixel width of this Actor.
        :rtype: float
        """
        return self.__rect.width
    

    def get_height(self) -> float:
        """
        Gets the height of this Actor's image.

        :return: A floating-point value representing the pixel height of this Actor.
        :rtype: float
        """
        return self.__rect.height


    def get_one_intersecting_object(self, other : type[Actor]) -> Actor:
        """
        Check for overlap with a given Actor sub-class. Uses the rectangular bounds of the object for detection.

        :param other: The Actor sub-class that will be checked for.
        :type other: type[Actor]

        :return: The object of the given Actor sub-class which overlaps this Actor, if one is found. Otherwise returns 'None'.
        :rtype: Actor
        """
        for actor in self.__world._World__get_all_actors():
            if actor is not self and type(actor) is other:
                if(actor.__rect.colliderect(self.__rect)):
                    return actor
        
        return None


    def get_one_object_at_offset(self, other : type[Actor], x_offset : float, y_offset : float) -> Actor:
        """
        Checks to see if the center of the Actor (plus a given offset) exists within a given Actor sub-class. Uses the rectangular bounds of the object for detection.

        :param other: The Actor sub-class that will be checked for.
        :type other: type[Actor]
        
        :param x_offset: The number of pixels to offset horizontally from the center of this Actor.
        :type x_offset: float

        :param y_offset: The number of pixels to offset vertically from the center of this Actor.
        :type y_offset: float

        :return: The object of the given Actor sub-class which contains this Actor's center point (plus offset), if one is found. Otherwise returns 'None'.
        :rtype: Actor
        """
        for actor in self.__world._World__get_all_actors():
            if actor is not self and type(actor) is other:
                if(actor.__rect.collidepoint(self.__rect.centerx + x_offset, self.__rect.centery + y_offset)):
                    return actor
        
        return None


    def is_touching(self, other : type[Actor]) -> bool:
        """
        Determines whether or not this Actor overlaps another Actor, of the given Actor sub-class.

        :param other: The Actor sub-class that will be checked for.
        :type other: type[Actor]

        :return: A boolean value containing 'True' if an overlap is detected. Otherwise returns 'False'.
        :rtype: bool
        """
        for actor in self.__world._World__get_all_actors():
            if actor is not self and type(actor) is other:
                if(actor.__rect.colliderect(self.__rect)):
                    return True
                
        return False

    def get_one_intersecting_tile(self, tile_type : type[Tile]) -> Tile:
        """
        Check for overlap with a given Tile sub-class. Uses the rectangular bounds of the object for detection.

        :param tile_type: The Tile sub-class that will be checked for.
        :type tile_type: type[Tile]

        :return: The object of the given Tile sub-class which overlaps this Actor, if one is found. Otherwise returns 'None'.
        :rtype: Tile
        """
        if self.__world._World__get_tile_map() is not None:
            hits = self.get_world()._World__get_tile_map()._TileMap__get_tiles_overlapping_in_area(tile_type, self.__rect)
            return next(iter(hits), None)
        
        return None


    def get_one_tile_at_offset(self, tile_type : type[Tile], x_offset : int, y_offset : int) -> Tile:
        """
        Checks to see if the center of the Actor (plus a given offset) exists within a given Tile sub-class. Uses the rectangular bounds of the object for detection.

        :param tile_type: The Tile sub-class that will be checked for.
        :type tile_type: type[Tile]

        :param x_offset: The number of pixels to offset horizontally from the center of this Actor.
        :type x_offset: int
        
        :param y_offset: The number of pixels to offset vertically from the center of this Actor.
        :type y_offset: int

        :return: The object of the given Tile sub-class which contains this Actor's center point (plus offset), if one is found. Otherwise returns 'None'.
        :rtype: Tile
        """
        if self.get_world()._World__get_tile_map() is not None:
            bounds = self.get_bounds()
            hit = self.get_world()._World__get_tile_map()._TileMap__get_tile_on_screen(bounds.centerx + x_offset, bounds.centery + y_offset)
            return hit
        
        return None
    

    @overload
    def move(self, move_by : pygame.Vector2) -> None:
        """
        [Overload] Moves this Actor by the given amount.

        :param move_by: The x and y-axis co-ordinates this Actor should move by.
        :type move_by: pygame.Vector2
        """
        self.move(move_by[0], move_by[1])


    @overload
    def move(self, move_by_x : int, move_by_y : int) -> None:
        """
        [Overload] Moves this Actor by the given amount.

        :param move_by_x: The x-axis (horizontal) number of pixels to move by.
        :type move_by_x: int
        :param move_by_y: The y-axis (vertical) number of pixels to move by.
        :type move_by_y: int
        """
        self.move(float(move_by_x), float(move_by_y))


    def move(self, move_by_x : float, move_by_y : float) -> None:
        """
        Moves this Actor by the given amount.

        :param move_by_x: The x-axis (horizontal) number of pixels to move by.
        :type move_by_x: float

        :param move_by_y: The y-axis (vertical) number of pixels to move by.
        :type move_by_y: float
        """
        self.__rect.move_ip(move_by_x, move_by_y);
        self.__position = self.__rect.center
    

    @overload
    def set_position(self, new_x : int, new_y : int) -> None:
        """
        [Overload] Sets the on-screen location of this Actor to the given co-ordinates.

        :param new_x: The horizontal (x-axis) co-ordinate of the desired new location.
        :type new_x: int
        :param new_y: The vertical (y-axis) co-ordinate of the desired new location.
        :type new_y: int
        """
        self.set_position(float(new_x), float(new_y))
    

    @overload
    def set_position(self, new_position : pygame.Vector2) -> None:
        """
        [Overload] Sets the on-screen location of this Actor to the given co-ordinates.

        :param new_position: The x and y-axis co-ordinates this Actor should be set to.
        :type new_position: pygame.Vector2
        """
        self.set_position(new_position[0], new_position[1])
    

    def set_position(self, new_x : float, new_y : float) -> None:
        """
        Sets the on-screen location of this Actor to the given co-ordinates.

        :param new_x: The horizontal (x-axis) co-ordinate of the desired new location.
        :type new_x: float

        :param new_y: The vertical (y-axis) co-ordinate of the desired new location.
        :type new_y: float
        """
        self.__position = pygame.Vector2(new_x, new_y)
        self.__rect.center = self.__position
    

    def get_position(self) -> pygame.Vector2:
        """
        Gets the current on-screen position of this Actor.

        :return: A vector containing the x and y-axis co-ordinates of this Actor.
        :rtype: pygame.Vector2
        """
        return pygame.Vector2(self.__rect.center)


    def set_scale(self, new_scale: float) -> None:
        """
        Sets this Actor's scale factor. Double size would be 2.0f, half size would be 0.5f.

        :param new_scale: The new scale factor that should be applied to this Actor's image.
        :type new_scale: float
        """
        self.__scale = new_scale
        self.__generate_sprite()


    def get_scale(self) -> float:
        """
        Gets this Actor's current scale factor.

        :return: A floating-point value representing this Actor's image scaling factor.
        :rtype: float
        """
        return self.__scale


    def set_rotation(self, rotation : float) -> None:
        """
        Sets the rotation of this Actor, between -360 and 360 degrees.

        :param rotation: The desired new rotation, in degrees.
        :type rotation: float
        """
        if rotation <= -360 or rotation >= 360:
            rotation = 0
        self.__rotation = -rotation
        self.__generate_sprite()


    def get_rotation(self) -> float:
        """
        Gets this Actor's current rotation, in degrees.

        :return: A floating-point value representing this Actor's current rotation.
        :rtype: float
        """
        return -self.__rotation


    def rotate(self, rotate_by : float) -> None:
        """
        Rotates this Actor by the given number of degrees.

        :param rotate_by: The amount this Actor should be rotated by, in degrees.
        :type rotate_by: float
        """
        self.__rotation -= rotate_by
        if self.__rotation <= -360 or self.__rotation >= 360:
            self.__rotation = 0
        self.__generate_sprite()

    @overload
    def look_at(self, look_at_object : Actor) -> None:
        """
        [Overload] Rotates this Actor to face a specific location on-screen.

        :param look_at_object: The Actor which this Actor should face towards.
        :type look_at_object: Actor
        """
        self.look_at(look_at_object.get_position())


    def look_at(self, look_at_position : pygame.Vector2) -> None:
        """
        Rotates this Actor to face a specific location on-screen.

        :param look_at_position: The location on-screen that this Actor should face.
        :type look_at_position: pygame.Vector2
        """
        direction = look_at_position - self.get_position();
        self.set_rotation(90 + (float)(atan2(direction.y, direction.x) * (180 / pi)));


    def flip_vertically(self, flipped : bool) -> None:
        """
        Flips this Actor's image vertically, based on the provided boolean value.

        :param flipped: Determines whether or not this Actor should be flipped vertically.
        :type flipped: bool
        """
        self.__sprite = pygame.transform.flip(self.__raw_image, False, flipped)
        self.__sprite = pygame.transform.rotozoom(self.__sprite, self.__rotation, self.__scale)
        self.__rect = self.__sprite.get_rect(center=self.__rect.center)


    def flip_horizontally(self, flipped : bool) -> None:
        """
        Flips this Actor's image horizontally, based on the provided boolean value.

        :param flipped: Determines whether or not this Actor should be flipped horizontally.
        :type flipped: bool
        """
        self.__sprite = pygame.transform.flip(self.__raw_image, flipped, False)
        self.__sprite = pygame.transform.rotozoom(self.__sprite, self.__rotation, self.__scale)
        self.__rect = self.__sprite.get_rect(center=self.__rect.center)


    def __generate_sprite(self):
        self.__sprite = pygame.transform.rotozoom(self.__raw_image, self.__rotation, self.__scale)
        self.__rect = self.__sprite.get_rect(center=self.__rect.center)
        self.__rect.center = self.__position


    def is_visible(self) -> bool:
        """
        Checks whether this Actor is visible or not.

        ***Note:*** Invisible Actors will still be updated, just not drawn to the screen.

        :return: A boolean value representing whether this Actor is visible or not.
        :rtype: bool
        """
        return self.__visible
    

    def set_visible(self, visible : bool) -> None:
        """
        Sets whether or not this Actor should be drawn to the screen.

        :param visible: This Actor will be drawn if 'True', and will not be drawn if 'False'.
        :type visible: bool
        """
        self.__visible = visible


    def set_image(self, filepath : str) -> None:
        """
        Sets this Actor's image to a new image, using the provided filepath and filename (filetype suffix required).

        :param filepath: The name and filetype of the desired image. A filepath is also required for the containing directory.
        :type filepath: str

        :raises FileNotFoundError: Thrown if the provided file cannot be found.
        """
        try:
            self.__raw_image = Game._Game__get_texture(filepath)
            self.__raw_image.set_colorkey((255,255,255), RLEACCEL)
            self.__rect = self.__raw_image.get_rect()
        except FileNotFoundError as err:
            raise FileNotFoundError(err)

        self.__generate_sprite()


    def set_image_rect(self, width : int, height : int, colour : pygame.Color) -> None:
        """
        Sets this Actor's image to a new coloured rectangle.

        :param width: The width, in pixels, of the desired rectangle shape.
        :type width: int

        :param height: The height, in pixels, of the desired rectangle shape.
        :type height: int

        :param colour: The colour of the desired rectangle shape.
        :type colour: pygame.Color
        """
        self.__raw_image = pygame.Surface((width, height)).convert_alpha()
        self.__raw_image.fill(colour)
        self.__generate_sprite()


    def is_offscreen(self) -> bool:
        """
        Checks to see if this Actor is fully offscreen.

        :return: Returns 'True' if this actor is fully offscreen. Otherwise, returns 'False'.
        :rtype: bool
        """
        if(self.__rect.right < 0):
            return True;
        if(self.__rect.left > self.get_world().get_width()):
            return True;
        if(self.__rect.bottom < 0):
            return True;
        if(self.__rect.top > self.get_world().get_height()):
            return True;
        return False;


    def is_at_screen_edge(self) -> bool:
        """
        Checks to see if any edge of this Actor is touching any edge of the game window.

        :return: Returns 'True' if an edge collision is detected. Otherwise, returns 'False'.
        :rtype: bool
        """
        if(self.__rect.left < 0):
            return True;
        if(self.__rect.right > self.get_world().get_width()):
            return True;
        if(self.__rect.top < 0):
            return True;
        if(self.__rect.bottom > self.get_world().get_height()):
            return True;
        return False;
    

    @property
    def Game(self) -> Game:
        """
        Gets the main Game instance.

        :return: The Game object responsible for handling this game project.
        :rtype: Game
        """
        return Game._Game__instance


    def __set_world(self, world) -> None:
        self.__world = world
