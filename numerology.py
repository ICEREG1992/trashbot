import helperfunctions

class numerology:
    async def run(self, message):
        if message.content.startswith(('!num ', '!numerology ')):
            arr = list(' '.join(message.content.split(' ')[1:]).lower())
            total = sum(ord(c) - 97 for c in arr if 'a' <= c <= 'z')
            await message.channel.send(str(total))