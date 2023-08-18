import pygame;
from os.path import exists;
from typing import final

@final
class AudioManager():
    """
    The class which is responsible for background music or sound effects in a game project.
	- Supports looping background music.
	- Sound effects can be pre-loaded for better performance during runtime.
    """
    __volume = 80;
    __bgm_is_paused = False
    __bgm_loop_start = 0

    __instance = None
    BGM_LOOP_EVENT = pygame.USEREVENT + 1

    def __init__(self) -> None:
        if AudioManager.__instance is None:
            AudioManager.__instance = self
            pygame.mixer.init()
            AudioManager.set_volume(AudioManager.__volume if AudioManager.__volume != None else 0.8);
        


    def play_bgm(filepath : str, loop = True, loop_from_millis = 0, fade_in_millis = 0) -> None:
        """
        Plays a piece of background music.

        :param filepath: The filepath, file name and filetype of the desired audio file.
        :type filepath: str

        :param loop: Determines whether or not this music will loop infinitely. 'True' by default.
        :type loop: bool, optional

        :param loop_from_millis: Provides a loop-from point in milliseconds, once the audio has finished playing. '0' milliseconds by default.
        :type loop_from_millis: int, optional

        :param fade_in_millis: Provides a period of time (in milliseconds) which the music will fade in to the set volume. '0' milliseconds by default.
        :type fade_in_millis: int, optional
        """
        from dna_engine import game
        game.Game._Game__build_asset(filepath)
        pygame.mixer.music.load("dist/" + filepath if not game.Game._Game__is_running_through_bundle() else filepath);
        pygame.mixer.music.set_volume(AudioManager.__volume)
        
        if(loop == True):
            AudioManager.__bgm_loop_start = loop_from_millis
            pygame.mixer.music.play(loops=1, start=0, fade_ms=fade_in_millis);
            pygame.mixer.music.set_endevent(AudioManager.BGM_LOOP_EVENT)
        else:
            pygame.mixer.music.play(loops=1, start=0, fade_ms=fade_in_millis);
    

    def __restart_bgm_loop():
        pygame.mixer.music.set_endevent(0)
        pygame.mixer.music.play(loops=-1, start=AudioManager.__bgm_loop_start / 1000);


    def fadeout_bgm(time_in_millis : int) -> None:
        """
        Fades out the currently playing background music.

        :param time_in_millis: The amount of time, in milliseconds, the fadeout should last for.
        :type time_in_millis: int
        """
        pygame.mixer.music.fadeout(time_in_millis)


    def pause_bgm(pause_state : bool) -> None:
        """
        Pauses or resumes an existing background music track.

        :param pause_state: Determines whether the background music should be paused or resumed.
        :type pause_state: bool
        """
        if pause_state is True:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()
        
        AudioManager.__bgm_is_paused = pause_state

    
    def is_bgm_paused() -> bool:
        """
        Checks to see if the current background music is paused.

        :return: Returns 'true' if the current background music is paused. Returns 'false' in any other state, or if no background music track has been set up.
        :rtype: bool
        """
        return AudioManager.__bgm_is_paused
        


    def stop_bgm() -> None:
        """
        Stops the current background music track.
        """
        pygame.mixer.music.stop()


    def play_sfx(filepath : str) -> None:
        """
        Plays a sound effect.

        :param filepath: The filepath, file name and filetype of the desired audio file.
        :type filepath: str
        """
        try:
            from dna_engine import game
            new_sfx = game.Game._Game__get_audio(filepath)
            new_sfx.set_volume(AudioManager.__volume);
            new_sfx.play();
        except FileNotFoundError as e: raise(e)


    def set_volume(volume : float) -> None:
        """
        Sets the master volume of all audio handled by the AudioManager.

        :param volume: The desired volume, from 0 to 100.
        :type volume: float
        """
        AudioManager.__volume = max(min(volume, 100), 0);
        pygame.mixer.music.set_volume(AudioManager.__volume / 100);

    
    def get_volume() -> float:
        """
        Gets the current master volume of this AudioManager.

        :return: A floating-point value representing the master volume.
        :rtype: float
        """
        return AudioManager.__volume


    def __sound_exists(self, file_name : str) -> bool:
        return exists("audio/" + file_name);

