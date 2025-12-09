import requests
import re

class jpegdirt:
    async def run(self, message):
        if re.match(r'^jp.*g(dirt)?!random', message.content.lower()):
            r = requests.get("https://jpegdirt.tumblr.com/random", allow_redirects=True)
            await message.channel.send(r.url)