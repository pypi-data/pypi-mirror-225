import pygame
from pygame.surface import Surface
from pygame.rect import Rect

from multimethod import multimethod
from typing import overload
import typing

class Text():
    """
    The class which handles the rendering of text to the game screen.
	- Supports system fonts and local fonts.
	- Text can be scaled, rotated and positioned similarly to Actors.
    """
    def __init__(self, message : str, font_name : typing.Optional[str] = None, font_size = 32, is_system_font = True) -> None:
        """
        The constructor for this Text class.

        :param message: The piece of text that should be rendered by this Text object.
        :type message: str

        :param font_name: The name of the desired font. If not a system font, a filepath will also be required.
        :type font_name: str, optional

        :param font_size: The font size of the desired font. '32' by defualt.
        :type font_size: int, optional
        
        :param is_system_font: Determines whether or not the font should be found installed on the system already, or if it can be found in a folder local to the project.
        :type is_system_font: bool, optional
        """
        super().__init__()
        self.__render_surface = None
        self.__message = None;       
        self.__colour = (255, 255, 255, 255);
        self.__world = None;
        self.__game = None
        self.__position = pygame.math.Vector2()
        self.__scale = 1.0
        self.__rotation = 0
        self.__origin = pygame.math.Vector2()
        self.__rect = Rect(0, 0, 64, 64)
        self.set_font(font_name, font_size, is_system_font);
        self.set_message(message)
        self.set_origin(self.__origin)
        
        

    def set_message(self, new_message : str):
        """
        Sets a new message for this Text object to render.

        :param message: The new message string that should be displayed.
        :type message: str
        """
        if self.__message is not new_message:
            self.__message = new_message;
            x = self.get_x();
            y = self.get_y();
            self.__surface, self.__rect = self.__font.render(self.__message, self.__colour, size=int(self.__font.size * self.__scale));

            self.__rect.x = x;
            self.__rect.y = y;
            self.__generate_render()


    @overload
    def set_position(self, new_position : pygame.Vector2) -> None:
        """
        [Overload] Sets the on-screen location of this Text to the given co-ordinates.

        :param new_position: The horizontal (x-axis) and vertical (y_axis) co-ordinates of the desired new location.
        :type new_position: pygame.Vector2
        """
        self.set_position(new_position[0], new_position[1])


    @overload
    def set_position(self, new_x : int, new_y : int) -> None:
        """
        [Overload] Sets the on-screen location of this Text to the given co-ordinates.

        :param new_x: The horizontal (x-axis) co-ordinate of the desired new location.
        :type new_x: int

        :param new_y: The vertical (y-axis) co-ordinate of the desired new location.
        :type new_y: int
        """
        self.set_position(float(new_x), float(new_y))


    def set_position(self, new_x : float, new_y : float) -> None:
        """
        Sets the on-screen location of this Text to the given co-ordinates.

        :param new_x: The horizontal (x-axis) co-ordinate of the desired new location.
        :type new_x: float

        :param new_y: The vertical (y-axis) co-ordinate of the desired new location.
        :type new_y: float
        """
        self.__position = pygame.Vector2(new_x, new_y)
        self.__rect.centerx = self.__position[0] + (self.__surface.get_width() * self.__origin[0])
        self.__rect.centery = self.__position[1] + (self.__surface.get_height() * self.__origin[1])


    def get_position(self) -> pygame.Vector2:
        """
        Gets the current on-screen location of this Text.

        :return: A vector object containing the x and y axis co-ordinates of this Text.
        :rtype: pygame.math.Vector2
        """
        return self.__position
    

    def __set_world(self, world) -> None:
        self.__world = world


    def __set_game(self, game) -> None:
        self.__game = game
    

    def get_x(self) -> float:
        """
        Gets the current horizontal on-screen position of this Text.

        :return: A floating-point value representing the x-axis co-ordinate of this Text.
        :rtype: float
        """
        return self.__position[0]
    

    def get_y(self) -> float:
        """
        Gets the current vertical on-screen position of this Text.

        :return: A floating-point value representing the y-axis co-ordinate of this Text.
        :rtype: float
        """
        return self.__position[1]


    @overload
    def set_origin(self, origin_x : float, origin_y : float) -> None:
        """
        [Overload] Sets the rendering origin of this Text. Values are clamped between 0.0 and 1.0.

        :param origin_x: The horizontal fractional co-ordinate of this Text's origin point.
        :type origin_x: float
        :param origin_y: The vertical fractional co-ordinate of this Text's origin point.
        :type origin_y: float
        """
        self.set_origin(pygame.Vector2(origin_x, origin_y))


    def set_origin(self, new_origin : pygame.Vector2) -> None:
        """
        Sets the rendering origin of this Text. Values are clamped between 0.0 and 1.0.

        :param new_origin: The horizontal and vertical fractional origin point of this Text.
        :type new_origin: pygame.Vector2
        """
        # Ensure values are between 0 and 1
        new_origin[0] = max(0.0, min(new_origin[0], 1.0))
        new_origin[1] = max(0.0, min(new_origin[1], 1.0))

        # Assign origin
        self.__origin = new_origin
        self.__generate_render()


    def set_rotation(self, new_rotation : float) -> None:
        """
        Sets the rotation of this Text, between -360 and 360 degrees.

        :param new_rotation: The desired new rotation, in degrees.
        :type new_rotation: float
        """
        if new_rotation <= -360 or new_rotation > 360:
            new_rotation = 0

        self.__rotation = new_rotation
        self.__generate_render()


    def rotate(self, rotate_by : float) -> None:
        """
        Rotates this Text by the given number of degrees.

        :param rotate_by: The amount this Text should be rotated by, in degrees.
        :type rotate_by: float
        """
        self.set_rotation(self.__rotation + rotate_by)


    def get_rotation(self) -> float:
        """
        Gets this Text's current rotation, in degrees.

        :return: A floating-point value representing this Text's current rotation.
        :rtype: float
        """
        return self.__rotation


    def set_scale(self, new_scale : float):
        """
        Sets this Text's scale factor. Double size would be 2.0f, half size would be 0.5f.

        :param new_scale: The new scale factor that should be applied to this Text's font.
        :type new_scale: float
        """
        self.__scale = new_scale
        self.__generate_render()


    def get_scale(self) -> float:
        """
        Gets this Text's current scale factor.

        :return: A floating-point value representing this Text's font scaling factor.
        :rtype: float
        """
        return self.__scale
    

    def set_colour(self, r : int, g : int, b : int, a = 255) -> None:
        """
        Sets the colour used by this Text object.

        :param r: The red component, between 0 and 255.
        :type r: int

        :param g: The green component, between 0 and 255.
        :type g: int

        :param b: The blue component, between 0 and 255.
        :type b: int
        
        :param a: The alpha component, between 0 and 255.
        :type a: int, optional
        """
        r = max(0, min(r, 255))
        g = max(0, min(g, 255))
        b = max(0, min(b, 255))
        a = max(0, min(a, 255))
        self.__colour = (r, g, b, a)


    def get_colour(self) -> tuple[int, int, int, int]:
        """
        Gets the current colour of this Text object.

        :return: A tuple object representing the colour used when drawing this Text.
        :rtype: tuple[int, int, int, int]
        """
        return self.__colour


    def set_font(self, font_name : str, font_size = 32, is_system_font = True) -> None:
        """
        Sets the font used by this Text object.

        :param font_name: The font name of the desired font. If using a non-system font, please ensure a filepath is also supplied.
        :type font_name: str

        :param font_size: The font size of the desired font. '32' by default.
        :type font_size: int, optional

        :param is_system_font: Determines whether to look for this font in system fonts or in a local folder.
        :type is_system_font: bool, optional
        """
        if(font_name == None):
            font_name = "Consolas";
        
        if font_size < 0:
            font_size = 0
        
        from dna_engine import game
        self.__font = game.Game._Game__get_font(font_name, font_size, is_system_font)


    def __generate_render(self):
        # Rotate the image.
        self.__render_surface = pygame.transform.rotozoom(self.__surface, -self.__rotation, self.__scale)
        # Rotate the offset vector.
        offset = pygame.Vector2((self.__surface.get_width() / 2) - (self.__surface.get_width() * self.__origin[0]), (self.__surface.get_height() / 2) - (self.__surface.get_height() * self.__origin[1])) * self.__scale
        offset_rotated = offset.rotate(self.__rotation)
        # Create a new rect with the center of the sprite + the offset.
        self.__rect = self.__render_surface.get_rect(center=self.__position + offset_rotated)
        self.__round_position()


    def __round_position(self) -> None:
        self.__rect.center = [round(self.__rect.centerx), round(self.__rect.centery)]


    def _render(self, render_target : Surface):
        """
        Called automatically once per frame. Draws the message held by this Text using the associated font. Can be overwritten for custom functionality.

        :param render_target: The canvas that will be drawn to.
        :type render_target: Surface
        """
        render_target.blit(self.__render_surface, self.__rect);


    def _update(self, delta_time : float):
        """
        Called automatically once per frame. Useful for functionality which should be performed for as long as this Text exists.
        **Note:** Does nothing unless overriden by a derived class.

        :param delta_time: The amount of time, in fractions of a second, that has elapsed since the last frame of the game.
        :type delta_time: float
        """
        pass;

    