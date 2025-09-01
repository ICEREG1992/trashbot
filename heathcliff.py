import datetime as dt
import comics

class heathcliff:
    async def run(self, message):
        if (message.content == "!heathcliff"):
            ch = comics.search("heathcliff", dt.datetime.now().date())
            await message.channel.send(ch.image_url)
