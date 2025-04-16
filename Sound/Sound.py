import pygame

from IO.ResourceLoader import ResourceLoader
from Logging.Logger import Logger
from Enums.LogType import LogType

class Sound:
    def __init__(self, resLoaderPtr):
        pygame.mixer.init()
        self.__resLoaderPtr: ResourceLoader = resLoaderPtr
        pygame.mixer.set_num_channels(8) # Number of available sound channels. Feel free to change.

    def playSound(self, sound, vol):
        # Plays a sound from the ResourceLoader
        # Check for available channels
        channel = pygame.mixer.find_channel(True)
        soundRes = self.__resLoaderPtr.accessResource(sound, returnIfMissing=False)
        if channel and soundRes:
            channel.set_volume(vol)
            channel.play(soundRes)
        else:
            Logger.log(f"Failed to play sound '{sound}'! The resource might not have been found, or no audio channel is available. (PYGE_TYPE_AUDIO_ERROR, PYGE_NON_FATAL_ERROR)", LogType.ERROR, self)

    def playMusic(self, filePath, vol, loops: int):
        # Plays music from disk. Passing -1 for "loops" loops infinitely
        pygame.mixer.music.load(filePath) # Loading before getting the channel insures that we have the file. This is necessary since time delays when loading from disk are greater.
        pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.play(loops) # Music always plays on Channel 0