import requests
import helperfunctions
from permissions import permissions
import os
import boto3
import subprocess

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global mcIP
mcIP = ""

global server

class mc:

    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'mc_ip'}})
        global mcIP
        mcIP = d['Item']['data']['S']

    async def run(self, message):
        global mcIP
        global server
        if mcIP and message.content == "!whosuprn":
            r = requests.get('https://api.mcsrvstat.us/2/' + mcIP)
            o = r.json()
            if o['online']:
                n = str(o['players']['online'])
                if (n == '0'):
                    await message.channel.send(helperfunctions.pick_string(["nah nobody up rn", "not rn sorry", "nope", "nothing much whos uprn with u", "nah", "negative"]))
                else:
                    out = ""
                    for p in o['players']['list']:
                        out += p + "\n"
                    await message.channel.send(out)
            else:
                await message.channel.send(helperfunctions.pick_string([
                    "uh oh server down (down)",
                    "haha ummmmm i kicked something back here hehe oops uhhh (down)",
                    "whoa whoa whoa waho whoa whao smmmm ummmmmmmmm server??? server??? servv?er?? (down)",
                    "WHOOPS UH OH HEHEHE (down)",
                    "server is sorta sus rn ngl (down)",
                    "server is down (down) (down) (epic down)",
                    "it is down (down)"]))
        elif message.content.startswith("!setwhosup ") and permissions.allowed(message.author.id, "blue"):
            i = message.content[11:]
            mcIP = i
            await message.channel.send(helperfunctions.pick_string(["ok i'll watch " + mcIP + " for ya",
                "ok sure minecraft ip set to " + mcIP,
                "New IP Set! haha wasnt that goofy"]))
            mcplayers.save()
        elif message.content == "!hostmc" and permissions.allowed(message.author.id, "blue"):
            if server is None:
                await message.channel.send(helperfunctions.pick_string([
                    "NO!!!!!!!!!!",
                    "WAIT YOUR TURN",
                    "one at a time pls"
                ]))
            else:
                await message.channel.send(helperfunctions.pick_string([
                    "hhhhnnnnnnngggggg...",
                    "\*inhales\*",
                    "ok one sec"
                ]))
                server = subprocess.Popen('java -Xmx1024M -Xms1024M -jar /home/william/minecraft/server.jar nogui', stdin=subprocess.PIPE, shell=True)
                helperfunctions.bot_wait_long()
                await message.channel.send(helperfunctions.pick_string([
                    "ok im runnin",
                    "epic minecraft",
                    "aw yeah b sure to mine some dimonds for me :)"
                ]))
            
        elif message.content == "!stophost" and permissions.allowed(message.author.id, "blue"):
            server.kill()

    def save():
        global mcIP
        db.put_item(TableName="trashbot", Item={'name':{'S':'mc_ip'}, 'data':{'S':mcIP}})