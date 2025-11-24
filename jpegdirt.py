import requests

class jpegdirt:
    async def run(self, message):
        parts = message.content.split(' ', 1)
        if parts[0] == "jpegdirt!random":
            r = requests.get("https://jpegdirt.tumblr.com/random", allow_redirects=True)
            await message.channel.send(r.url)