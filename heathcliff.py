import datetime as dt
import comics

class heathcliff:
    async def run(self, message):
        if (message.content == "!heathcliff"):
            ch = comics.search("heathcliff", dt.datetime.now().date())
            if ch:
                await message.channel.send(ch.image_url)
            else:
                await message.channel.send("hasn't been uploaded yet, wait a few hours pls")
