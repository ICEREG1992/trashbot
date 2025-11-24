import requests
import re

class jpegdirt:
    async def run(self, message):
        parts = message.content.split(' ', 1)
        if re.match(r'jp.*gdirt!random', parts[0]):
            r = requests.get("https://jpegdirt.tumblr.com/random", allow_redirects=True)
            await message.channel.send(r.url)