import pygame
from os.path import exists as file_exists
from multimethod import multimethod
from typing import overload

from pygame.surface import Surface
from pygame.locals import (RLEACCEL)

class Tile():
    def __init__(self) -> None:
        self.__sprite = pygame.Surface((64,64)).convert_alpha()
        self.__rect = self.__sprite.get_rect()
        self.__raw_image = self.__sprite

        self.__generate_sprite()


    def update(self, delta_time : float) -> None:
        pass


    def render(self, render_target : Surface) -> None:
        render_target.blit(self.__sprite, self.__rect)


    def set_position(self, x : float, y : float) -> None:
        self.__rect.move_ip(x, y)


    def set_image_rect(self, colour : tuple[int, int, int]) -> None:
        self.__raw_image = pygame.Surface((self.__rect.width, self.__rect.height)).convert_alpha()
        self.__raw_image.fill(colour)
        self.__generate_sprite()


    @overload
    def set_image(self, image_filepath : str) -> None:
        if(image_filepath is not None and file_exists(image_filepath)):
            from dna_engine import game
            self.set_image(game.Game._Game__get_texture(image_filepath))

    
    def set_image(self, texture : Surface) -> None:
        old_rect = self.__rect

        self.__sprite = texture
        self.__rect = self.__raw_image.get_rect()
        self.__rect.x = old_rect.x
        self.__rect.y = old_rect.y
        self.__rect.width = old_rect.width
        self.__rect.height - old_rect.height

        self.__raw_image.set_colorkey((255,255,255), RLEACCEL)
        self.__generate_sprite()


    def get_image(self) -> pygame.sprite.Sprite:
        return self.__sprite


    def __set_dimensions(self, width : int, height : int) -> None:
        self.__rect.width = width
        self.__rect.height = height
        self.__sprite = pygame.transform.scale(self.__sprite, (width, height))


    def __generate_sprite(self) -> None: 
        self.__sprite = pygame.transform.rotozoom(self.__raw_image, 0, 1)
        #self.__rect = self.__sprite.get_rect(center=self.__rect.center)