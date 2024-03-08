import requests
import helperfunctions
from permissions import permissions
import os
import boto3
import subprocess
import jproperties

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global mcIP
mcIP = ""

global server
server = None

class servers:

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
            servers.save()
        # minecraft
        elif message.content == "!hostmc" and permissions.allowed(message.author.id, "blue"):
            if not servers.serverExists():
                await message.channel.send(helperfunctions.pick_string([
                    "hhhhnnnnnnngggggg...",
                    "\*inhales\*",
                    "ok one sec"
                ]))
                server = subprocess.Popen(['java','-Xmx2048M','-Xmx2048M','-jar','server.jar','nogui'], cwd=r'/home/william/minecraft/', stdin=subprocess.PIPE)
                helperfunctions.bot_wait_long()
                await message.channel.send(helperfunctions.pick_string([
                    "ok im runnin",
                    "epic minecraft",
                    "aw yeah b sure to mine some dimonds for me :)"
                ]))
            else:
                await message.channel.send(helperfunctions.pick_string([
                    "NO!!!!!!!!!!",
                    "WAIT YOUR TURN",
                    "one at a time pls"
                ]))
        elif message.content == "!mcip":
            if servers.serverExists():
                config = jproperties.Properties()
                with open('/home/william/minecraft/' + 'server.properties', 'rb') as file:
                    config.load(file)
                await message.channel.send(config.get("server-ip").data + ":" + config.get("server-port").data)
            else:
                await message.channel.send("im not hosting anything rn")
        # sven coop
        elif message.content == "!hostsven" and permissions.allowed(message.author.id, "blue"):
            if not servers.serverExists():
                await message.channel.send(helperfunctions.pick_string([
                    "hhhhnnnnnnngggggg...",
                    "\*inhales\*",
                    "ok one sec"
                ]))
                server = subprocess.Popen(['bash','launch.sh'], cwd=r'/home/william/steam/', stdin=subprocess.PIPE)
                helperfunctions.bot_wait_long()
                await message.channel.send(helperfunctions.pick_string([
                    "ok im runnin",
                    "epic sven",
                    "aw yeah shoot em up baybee :)"
                ]))
            else:
                await message.channel.send(helperfunctions.pick_string([
                    "NO!!!!!!!!!!",
                    "WAIT YOUR TURN",
                    "one at a time pls"
                ]))
        elif message.content == "!svenip":
            if servers.serverExists():
                # do this later
                await message.channel.send("no can do sry")
        elif message.content == "!stophost" and permissions.allowed(message.author.id, "blue"):
            if servers.serverExists():
                if server:
                    server.kill()
                    server = None
                    await message.channel.send(helperfunctions.pick_string([
                        "it's dead, jim",
                        "kablam",
                        "kablooie",
                        "die die die die die die die die",
                        "goodnight little fishie"
                    ]))
                else:
                    subprocess.run(['pkill', '-f', '\'bash launch.sh\''])
                    subprocess.run(['pkill', '-f', 'server.jar'])
                    await message.channel.send("i tracked it down and killed it")
            else:
                await message.channel.send("im not hosting anything rn")

    def serverExists():
        global server
        if server is None:
            try:
                subprocess.check_output(["pgrep", '-f', "\'bash launch.sh\'"])
            except subprocess.CalledProcessError as e:
                return False
        return True

    def save():
        global mcIP
        db.put_item(TableName="trashbot", Item={'name':{'S':'mc_ip'}, 'data':{'S':mcIP}})