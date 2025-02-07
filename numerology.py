import helperfunctions

class numerology:
    async def run(self, message):
        if message.content.startswith(('!num ', '!numerology ', '!six ')):
            arr = list(' '.join(message.content.split(' ')[1:]).lower())
            total = sum(ord(c) - 96 for c in arr if 'a' <= c <= 'z')
            if message.content.startswith('!six '):
                total = total * 6
            await message.channel.send(str(total))
        elif message.content == '!num':
            await message.channel.send(helperfunctions.pick_string([
                'num num num',
                'num num num num num',
                'nom nom nom hehe',
                'num num give me gum gum',
                'num nom num nom num',
                'num num non mom',
                'num non mum nun',
                'num num nom mom mum',
                'nommy nommy nom',
                'mom',
                'num',
                'nom',
                'rum'
            ]))
        elif message.content == '!six':
            await message.channel.send(helperfunctions.pick_string([
                '6'
            ]))