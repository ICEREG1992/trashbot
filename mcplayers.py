import requests
import helperfunctions
import os

if os.path.exists("ip.txt"):
    f = open("ip.txt", "r")
    ip = f.read()
    f.close()
elif "MC_IP" in os.environ:
    ip = os.environ['MC_IP']
else:
    ip = ""

class mcplayers:

    async def run(self, message):
        if ip and message.content == "!whosuprn":
            r = requests.get('https://api.mcsrvstat.us/2/' + ip)
            o = r.json()
            if o['online']:
                n = str(o['players']['online'])
                if (n == '0'):
                    await message.channel.send(helperfunctions.pick_string(["nah nobody up rn", "not rn sorry", "nope", "pokemon go to *schleep* bro", "u r the imposter rn", "bro everyone is asleep chill out"]))
                else:
                    out = ""
                    for p in o['players']['list']:
                        out += p + "\n"
                    await message.channel.send(out)
            else:
                await message.channel.send(helperfunctions.pick_string(["uh oh server down", "someone ping ian lol @ian hehe ummmmm ha ha @ian hahahahehehe", "whoa whoa whoa waho whoa whao smmmm ummmmmmmmm server??? server??? servv?er??", "WHOOPS UH OH HEHEHE", "server is the impossssstor"]))