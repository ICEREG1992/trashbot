import requests
import helperfunctions
import os

if os.path.exists("ip.txt"):
    f = open("ip.txt", "r")
    ip = f.read()
    f.close()
else:
    ip = ""

class mcplayers:

    async def run(self, message):
        if ip and message.content == "!whosuprn":
            r = requests.get('https://api.mcsrvstat.us/2/' + ip)
            o = r.json()
            n = str(o['players']['online'])
            if (n == '0'):
                await message.channel.send(helperfunctions.pick_string(["nah nobody up rn", "not rn sorry", "nope", "pokemon go to *schleep* bro", "u r the imposter rn", "bro everyone is asleep chill out"]))
            else:
                await message.channel.send(helperfunctions.pick_string(["yah there's " + n + " people online rn", "they up bro they up!!! they up!!! all " + n + " of em!!!",
                "looks like there's " + n + " folks mining they craft rn", "uhhhhh rn there's " + n + " crafters", "yoooo there's " + n + " people up rn and at least one of them is " + helperfunctions.pick_string(o['players']['list'])]))