from AnieXEricaMusic.core.bot import AMBOT
from AnieXEricaMusic.core.dir import dirr
from AnieXEricaMusic.core.git import git
from AnieXEricaMusic.core.userbot import Userbot
from AnieXEricaMusic.misc import dbb, heroku

from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = AMBOT()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
