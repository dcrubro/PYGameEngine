import pygame
from Logging.Logger import Logger
from Enums.LogType import LogType

class Sound:
    def __init__(self, resLoaderPtr):
        pygame.mixer.init()
        # The usage status of the channels (False = Available, True = In Use). The channel count is a limitation of pygame and not PYGameEngine.
        # Note that Channel 0 is reserved for Music.
        self.__channelStatus = {
            1: False,
            2: False,
            3: False,
            4: False,
            5: False,
            6: False,
            7: False
        }
        self.__resLoaderPtr = resLoaderPtr

    def playSound(self, sound, vol):
        # Plays a sound from the ResourceLoader
        # Check for available channels
        for k, v in self.__channelStatus.items():
            if not(v):
                # Channel available
                channel = pygame.mixer.Channel(k)
                self.__channelStatus[k] = True
                res = self.__resLoaderPtr.accessResource(sound, returnIfMissing=False)
                res.set_volume(vol)
                if res: # Check resource status
                    channel.play(res)
                    self.__channelStatus[k] = False
                    return
                self.__channelStatus[k] = False
            Logger.log(f"Failed to play sound '{sound}'! The resource might not have been found, or no audio channel is available. (PYGE_TYPE_AUDIO_ERROR, PYGE_NON_FATAL_ERROR)", LogType.ERROR, self)

    def playMusic(self, filePath, vol, loops: int):
        # Plays music from disk. Passing -1 for "loops" loops infinitely
        pygame.mixer.music.load(filePath) # Loading before getting the channel insures that we have the file. This is necessary since time delays when loading from disk are greater.
        pygame.mixer.music.set_volume(vol)
        pygame.mixer.music.play(loops) # Music always plays on Channel 0