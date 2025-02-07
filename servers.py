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
            r = requests.get('https://api.mcsrvstat.us/3/' + mcIP)
            o = r.json()
            if o['online']:
                n = str(o['players']['online'])
                if (n == '0'):
                    await message.channel.send(helperfunctions.pick_string(["nah nobody up rn", "not rn sorry", "nope", "nothing much whos uprn with u", "nah", "negative"]))
                else:
                    out = ""
                    if o['players']['list']:
                        for p in o['players']['list']:
                            out += p['name'] + "\n"
                        if len(o['players']['list']) > o['players']['online']:
                            out += "and " + str(len(o['players']['list']) - o['players']['online']) + " more"
                    else:
                        out = str(o['players']['online']) + " people online rn"
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
        if mcIP and message.content == "!mcversion":
            r = requests.get('https://api.mcsrvstat.us/3/' + mcIP)
            o = r.json()
            if o['online']:
                n = str(o['version'])
                await message.channel.send(n)
            else:
                await message.channel.send(helperfunctions.pick_string([
                    "i can't tell",
                    "i won't tell",
                    "idk lol",
                    "it's a secret"]))
        elif message.content.startswith("!setwhosup ") and permissions.allowed(message.author.id, "blue"):
            i = message.content[11:]
            mcIP = i
            await message.channel.send(helperfunctions.pick_string(["ok i'll watch " + mcIP + " for ya",
                "ok sure minecraft ip set to " + mcIP,
                "New IP Set! haha wasnt that goofy"]))
            servers.save()
        # minecraft
        elif message.content.startswith("!hostmc") and permissions.allowed(message.author.id, "blue"):
            if not servers.serverExists():
                # set map first
                if len(message.content) > 7:
                    map = message.content[8:]
                    map = helperfunctions.sanitize(map)
                    try:
                        subprocess.check_output(['test', '-d', '/home/william/minecraft/' + map])
                    except subprocess.CalledProcessError as e:
                        await message.channel.send("i was not able to find a map called that")
                        return
                    await message.channel.send("i was able to find a map called that")
                    config = jproperties.Properties()
                    with open('/home/william/minecraft/' + 'server.properties', 'r+b') as file:
                        config.load(file, "utf-8")
                        config["level-name"] = map
                        file.seek(0)
                        file.truncate(0)
                        config.store(file, encoding="utf-8")
                else:
                    intro = "pls tell me a map.. i see these map names:\n"
                    maps = os.walk('/home/william/minecraft/')
                    # fuckery
                    maps = next(maps)[1]
                    # trim folders we don't want
                    for x in ['crash-reports','libraries','logs','versions','.fabric', 'debug', 'plugins', 'bundler']:
                        if x in maps:
                            maps.remove(x)
                    # sort
                    maps.sort()
                    # print list of maps
                    out = ""
                    for x in maps:
                        out += '- ' + x + "\n"
                    await message.channel.send(intro + out)
                    return

                # now boot
                await message.channel.send(helperfunctions.pick_string([
                    "hhhhnnnnnnngggggg...",
                    "\*inhales\*",
                    "ok one sec"
                ]))
                server = subprocess.Popen(['java', '-Xms1024M', '-Xmx1024M', '-jar', 'server.jar', 'nogui'], cwd=r'/home/william/minecraft/', stdin=subprocess.PIPE)
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
        elif message.content == "!mclog":
            try:
                with open('/home/william/minecraft/logs/latest.log', 'r') as file:
                    lines = [line.strip() for _, line in zip(range(10), file)]  # Read first 10 lines
                    log_text = '\n'.join(lines) if lines else "Log file is empty."
                    
                    if log_text:
                        await message.channel.send(f"```\n{log_text}\n```")  # Send in a code block for formatting
                    else:
                        await message.channel.send("No log data available.")
            except FileNotFoundError:
                await message.channel.send("Log file not found.")
            except Exception as e:
                await message.channel.send(f"Error reading log file: {e}")

        # sven coop
        elif message.content == "!hostsven" and permissions.allowed(message.author.id, "blue"):
            if not servers.serverExists():
                await message.channel.send(helperfunctions.pick_string([
                    "hhhhnnnnnnngggggg...",
                    "\*inhales\*",
                    "ok one sec"
                ]))
                server = subprocess.Popen(['bash','svends_run', '+maxplayers', '16'], cwd=r'/home/william/steam/', stdin=subprocess.PIPE)
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
                    if servers.serverExists():
                        subprocess.run(['pkill', '-f', 'svends_amd'])
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
                    subprocess.run(['pkill', '-f', 'svends'])
                    await message.channel.send("i tracked it down and killed it")
            else:
                await message.channel.send("im not hosting anything rn")

    def serverExists():
        global server
        if server is None:
            try:
                subprocess.check_output(["pgrep", '-f', "server.jar"])
            except subprocess.CalledProcessError as e:
                try:
                    subprocess.check_output(["pgrep", '-f', "svends"]) # todo
                except subprocess.CalledProcessError as e:
                    return False
        return True

    def save():
        global mcIP
        db.put_item(TableName="trashbot", Item={'name':{'S':'mc_ip'}, 'data':{'S':mcIP}})