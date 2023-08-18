import pygame 
from pygame.surface import Surface
from pygame.locals import (RLEACCEL);

class Background():
    """
    The class which represents the background elements of a game World.
	- Can be scrolled.
	- Supports repeating textures in both horizonal and vertical directions.
    """
    def __init__(self, world : 'World', image_name : str):
        """
        The constructor for the Background class. For internal use only.

        :param world: A reference to the World that this Background belongs to.
        :type world: World

        :param image_name: The name and type of the image file to be used for this Background.
        :type image_name: str
        """
        super().__init__();
        self.__scroll_x = 0
        self.__scroll_y = 0
        self.__tiles = 0
        self.__world = world
        self.__sprite = None

        if(image_name is not None):
            self.__set_image(image_name);
            self.__sprite = pygame.transform.scale(self.__sprite, (world.get_width(), world.get_height()))

        if(self.__rect is not None):
            self.__rect.x, self.__rect.y = (0,0);
    
        self.__calculate_tiles()


    def __set_image(self, filepath : str) -> None:
        try:
            from dna_engine import game
            self.__sprite = game.Game._Game__get_texture(filepath)
            self.__sprite.set_colorkey((255,255,255), RLEACCEL)
            self.__rect = self.__sprite.get_rect()
        except FileNotFoundError as err:
            raise FileNotFoundError(err)


    def __calculate_tiles(self) -> None:
        #self.tiles = math.ceil(self.__world.get_width() / self._sprite.get_rect().width) + 1
        self.__tiles = 3
        

    def __render(self, target : Surface) -> None:
        for i in range(0, self.__tiles):
            for j in range(0, self.__tiles):
                target.blit(self.__sprite, (-self.__sprite.get_rect().width + (i * self.__sprite.get_rect().width + self.__scroll_x), -self.__sprite.get_rect().height + (j * self.__sprite.get_rect().height + self.__scroll_y)))


    def scroll(self, horizontal_scroll : float, vertical_scroll : float) -> None:
        """
        Moves the Background by the amount provided.

        :param horizontal_scroll: The amount of pixels this Background should move horizontally this frame.
        :type horizontal_scroll: float

        :param vertical_scroll: The amount of pixels this Background should move vertically this frame.
        :type vertical_scroll: float
        """
        self.__scroll_x -= horizontal_scroll
        self.__scroll_y -= vertical_scroll

        if abs(self.__scroll_x) > self.__sprite.get_rect().width:
            if self.__scroll_x > 0:
                self.__scroll_x -= self.__sprite.get_rect().width
            else:
                self.__scroll_x += self.__sprite.get_rect().width

        if abs(self.__scroll_y) > self.__sprite.get_rect().height:
            if self.__scroll_y > 0:
                self.__scroll_y -= self.__sprite.get_rect().height
            else:
                self.__scroll_y += self.__sprite.get_rect().height
        
