import helperfunctions

class numerology:
    async def run(self, message):
        if message.content.startswith(('!num ', '!numerology ')):
            arr = list(' '.join(message.content.split(' ')[1:]).lower())
            total = sum(ord(c) - 97 for c in arr if 'a' <= c <= 'z')
            await message.channel.send(str(total))
        elif message.content.startswith('!num'):
            await message.channel.send(helperfunctions.pick_string([
                'num num num',
                'num num num num num',
                'nom nom nom hehe',
                'num num give me gum gum',
                '🥶❄️ HELP ITS SO COLD IM TURNING NUMB PLS LET ME INSIDE 🧊😰☃️'
            ]))