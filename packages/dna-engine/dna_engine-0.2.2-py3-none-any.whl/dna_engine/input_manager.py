import pygame;
from enum import Enum
from typing import final

@final
class MouseButtons(Enum):
    Left = 0
    Middle = 1
    Right = 2

@final
class InputManager(object):
    """
    The class which is responsible for detecting inputs from the user.
    - Supports keyboard and mouse inputs.
    - Can detect single presses, holds and releases of individual keys/buttons.
`   """
    __current_keys_pressed = []
    __prev_keys_pressed = []
    __current_m_buttons_pressed = []
    __prev_m_buttons_pressed = []
    __mouse_scroll_delta = 0
    
    def __update(self, keys_pressed) -> None:
        if not InputManager.__current_keys_pressed:
            InputManager.__prev_keys_pressed = keys_pressed;
        else:
            InputManager.__prev_keys_pressed = InputManager.__current_keys_pressed;
        InputManager.__current_keys_pressed = keys_pressed;
    
        if not InputManager.__current_m_buttons_pressed:
            InputManager.__prev_m_buttons_pressed = pygame.mouse.get_pressed()
        else:
            InputManager.__current_m_buttons_pressed = pygame.mouse.get_pressed()


    def is_key_pressed(key: str) -> bool:
        """
        Checks to see if the given keyboard key has just been pressed this frame.

        :param key: The keyboard key to check.
        :type key: str

        :return: Returns 'True' if this key was first pressed on this frame of the game. Otherwise, returns 'False'.
        :rtype: bool
        """
        return InputManager.__current_keys_pressed[pygame.key.key_code(key.lower())] is True and InputManager.__prev_keys_pressed[pygame.key.key_code(key.lower())] is False


    def is_key_released(key: str) -> bool:
        """
        Checks to see if the given keyboard key has just been released this frame of the game.

        :param key: The keyboard key to check.
        :type key: str

        :return: Returns 'True' if this key has only just been released in the current frame of the game. Otherwise, returns 'False'.
        :rtype: bool
        """
        return InputManager.__current_keys_pressed[pygame.key.key_code(key.lower())] is False and InputManager.__prev_keys_pressed[pygame.key.key_code(key.lower())] is True


    def is_key_held(key: str) -> bool:
        """
        Checks to see if the given keyboard key has been held for at least 2 consecutive frames of the game.

        :param key: The keyboard key to check.
        :type key: str

        :return: Returns 'True' if this key was held for at least 2 consecutive frames of the game. Otherwise, returns 'False'.
        :rtype: bool
        """
        return InputManager.__current_keys_pressed[pygame.key.key_code(key.lower())] is True and InputManager.__prev_keys_pressed[pygame.key.key_code(key.lower())] is True
    

    def is_key_up(key : str) -> bool:
        """
        Checks to see if the given keyboard key has been un-pressed for at least 2 consecutive frames.

        :param key: The keyboard key to check.
        :type key: str

        :return: Returns 'True' if this key has been un-pressed for at least 2 consecutive frames. Otherwise, returns 'False'.
        :rtype: bool
        """
        return InputManager.__current_keys_pressed[pygame.key.key_code(key.lower())] is False and InputManager.__prev_keys_pressed[pygame.key.key_code(key.lower())] is False


    def is_mouse_button_pressed(button : str) -> bool:
        """
        Checks to see if the given mouse button has just been pressed this frame.

        :param button: The mouse button to check.
        :type button: str

        :return: Returns 'True' if this button was first pressed on this frame of the game. Otherwise, returns 'False'.
        :rtype: bool
        """
        return InputManager.__current_m_buttons_pressed[MouseButtons[(button.lower())]] is True and InputManager.__prev_m_buttons_pressed[MouseButtons[(button.lower())]] is False
    

    def is_mouse_button_released(button : str) -> bool:
        """
        Checks to see if the given mouse button has just been released this frame of the game.

        :param button: The mouse button to check.
        :type button: str

        :return: Returns 'True' if this button has only just been released in the current frame of the game. Otherwise, returns 'False'.
        :rtype: bool
        """
        return InputManager.__current_m_buttons_pressed[MouseButtons[(button.lower())]] is False and InputManager.__prev_m_buttons_pressed[MouseButtons[(button.lower())]] is True


    def is_mouse_button_held(button : str) -> bool:
        """
        Checks to see if the given mouse button has been held for at least 2 consecutive frames of the game.

        :param button: The mouse button to check.
        :type button: str

        :return: Returns 'True' if this button was held for at least 2 consecutive frames of the game. Otherwise, returns 'False'.
        :rtype: bool
        """
        return InputManager.__current_m_buttons_pressed[MouseButtons[(button.lower())]] is True and InputManager.__prev_m_buttons_pressed[MouseButtons[(button.lower())]] is True


    def is_mouse_button_up(button : str) -> bool:
        """
        Checks to see if the given mouse button has been un-pressed for at least 2 consecutive frames.

        :param button: The mouse button to check.
        :type button: str

        :return: Returns 'True' if this button has been un-pressed for at least 2 consecutive frames. Otherwise, returns 'False'.
        :rtype: bool
        """
        return InputManager.__current_m_buttons_pressed[MouseButtons[(button.lower())]] is False and InputManager.__prev_m_buttons_pressed[MouseButtons[(button.lower())]] is False


    def get_mouse_position() -> pygame.Vector2:
        """
        Gets the current on-screen position of the user's mouse, in pixel co-ordinates. 

        :return: A Vector2 object representing the x (horizontal) and y (vertical) axis pixel co-ordinates of the mouse.
        :rtype: pygame.Vector2
        """
        mouse_pos = pygame.mouse.get_pos()
        return pygame.Vector2(mouse_pos[0], mouse_pos[1])
    

    def set_mouse_position(new_position : pygame.Vector2) -> None:
        """
        Sets the current on-screen position of the user's mouse.

        :param new_position: The x (horizontal) and y (vertical) axis pixel co-ordinates that the mouse should move to.
        :type new_position: pygame.Vector2
        """
        pygame.mouse.set_pos(new_position.x, new_position.y)
    

    def get_mouse_scroll_delta() -> float:
        """
        Gets the amount the user's mouse scroll wheel has scrolled this frame.

        :return: A floating-point value representing the amount the mouse scroll wheel has turned this frame.
        :rtype: float
        """
        return InputManager.__mouse_scroll_delta
    
    
    def __set_mouse_scroll_delta(delta : float) -> None:
        InputManager.__mouse_scroll_delta = delta
