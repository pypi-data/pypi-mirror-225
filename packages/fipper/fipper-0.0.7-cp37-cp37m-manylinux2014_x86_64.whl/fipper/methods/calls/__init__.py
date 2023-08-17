from .functions import CallsFunctions
from .telegram import TeleAPI
from .thumbnail import ThumbnailSong
from .tools import Tools
from .youtube import YouTubeAPI


class Calls(
    CallsFunctions,
    TeleAPI,
    ThumbnailSong,
    Tools,
    YouTubeAPI,
):
    pass
