import os

# Control sounds
class MusicPlayer:
    class AudioNotFoundError(Exception):
        def __init__(self):
            super().__init__("Audio file path is not defined, self.__path not found.")

    def __init__(self) -> None:
        os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
        from pygame import mixer
        # mixer.init(48000, -16, 1, 1024)
        self.__player = mixer
        self.__player.init()

    def play(self, path) -> None:
        self.__path = path
        if os.path.exists(path):
            self.__player.music.load(path)
            self.__path = path
            self.__player.music.play(-1)

    def pause(self) -> None:
        self.__player.music.pause()

    def unpause(self) -> None:
        self.__player.music.unpause()

    def change_volume(self, volume: float) -> None:
        self.__player.music.set_volume(volume)

    def getFileMetadata(self) -> None:
        if os.path.exists(self.__path):
            from tinytag import TinyTag
            info = TinyTag.get(self.__path, image=True)
            return {
                "name": info.title,
                "artist": info.artist,
                "year": info.year if info.year else None,
                "composer": info.composer,
                "duration": info.duration
            }