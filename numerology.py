import helperfunctions

class numerology:
    async def run(self, message):
        if message.content.startswith('!num ') or message.content.startswith('!numerology '):
            arr = list(' '.join((message.content.split(' ')[1:]).lower()))
            s = 0
            for c in arr:
                s += ord(c) - 97
            await message.channel.send(str(s))