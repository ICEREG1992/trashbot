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

class servers:

    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'mc_ip'}})
        global mcIP
        mcIP = d['Item']['data']['S']

    async def run(self, message):
        global mcIP
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
            if not servers.runningServer():
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
                    "*inhales*",
                    "ok one sec"
                ]))
                subprocess.Popen(['java', '-Xms3072M', '-Xmx3072M', '-jar', 'server.jar', 'nogui'], cwd=r'/home/william/minecraft/', stdin=subprocess.PIPE)
                helperfunctions.bot_wait_long()
                await message.channel.send(helperfunctions.pick_string([
                    "ok im runnin",
                    "epic minecraft",
                    "aw yeah b sure to mine some dimonds for me :)"
                ]))
            else:
                await message.channel.send(helperfunctions.pick_string([
                    "looks like i'm already running " + servers.runningServer(),
                    "it's already " + servers.runningServer(),
                    "it's actually " + servers.runningServer() + " time rn baybee",
                    "i'll keep hosting " + servers.runningServer() + " instead ok"
                ]))
        elif message.content == "!mcip":
            if servers.runningServer():
                config = jproperties.Properties()
                with open('/home/william/minecraft/' + 'server.properties', 'rb') as file:
                    config.load(file)
                await message.channel.send(config.get("server-ip").data + ":" + config.get("server-port").data)
            else:
                await message.channel.send("im not hosting anything rn")
        elif message.content == "!mclog":
            with open('/home/william/minecraft/logs/latest.log', 'r') as file:
                lines = file.readlines()[-10:]
                log_text = ''.join(lines) if lines else "Log file is empty."
                
                if log_text:
                    await message.channel.send(f"```\n{log_text}\n```")  # Send in a code block for formatting
                else:
                    await message.channel.send("🪵")

        # sven coop
        elif message.content == "!hostsven" and permissions.allowed(message.author.id, "blue"):
            if not servers.runningServer():
                await message.channel.send(helperfunctions.pick_string([
                    "hhhhnnnnnnngggggg...",
                    "*inhales*",
                    "ok one sec"
                ]))
                subprocess.Popen(['bash','svends_run', '+maxplayers', '16'], cwd=r'/home/william/Steam/steamapps/common/Sven Co-op Dedicated Server', stdin=subprocess.PIPE)
                helperfunctions.bot_wait()
                await message.channel.send(helperfunctions.pick_string([
                    "ok im runnin",
                    "epic sven",
                    "aw yeah shoot em up baybee :)"
                ]))
            else:
                await message.channel.send(helperfunctions.pick_string([
                    "looks like i'm already running " + servers.runningServer(),
                    "it's already " + servers.runningServer(),
                    "it's actually " + servers.runningServer() + " time rn baybee",
                    "i'll keep hosting " + servers.runningServer() + " instead ok"
                ]))
        elif message.content == "!svenip":
            if servers.runningServer():
                r = requests.get('https://ipecho.net/plain')
                await message.channel.send(r.text)

        # tf2
        elif message.content == "!hosttf2" and permissions.allowed(message.author.id, "blue"):
            if not servers.runningServer():
                await message.channel.send(helperfunctions.pick_string([
                    "hhhhnnnnnnngggggg...",
                    "*inhales*",
                    "ok one sec"
                ]))
                # first get game server account login token
                token = ""
                if os.path.exists('/home/william/Steam/steamapps/common/Team Fortress 2 Dedicated Server/' + 'token.txt'):
                    f = open('/home/william/Steam/steamapps/common/Team Fortress 2 Dedicated Server/' + 'token.txt', "r")
                    token = f.read()
                    f.close()
                else:
                    await message.channel.send("will doesn't have the token set up right")
                    return
                subprocess.Popen(['bash','srcds_run', '-game', 'tf', '+maxplayers', '16', '+map', 'ctf_2fort', '+sv_setsteamaccount', token], cwd=r'/home/william/Steam/steamapps/common/Team Fortress 2 Dedicated Server', stdin=subprocess.PIPE)
                helperfunctions.bot_wait()
                await message.channel.send(helperfunctions.pick_string([
                    "ok im runnin",
                    "epic tf2",
                    "aw yeah shoot em up baybee :)"
                ]))
            else:
                await message.channel.send(helperfunctions.pick_string([
                    "looks like i'm already running " + servers.runningServer(),
                    "it's already " + servers.runningServer(),
                    "it's actually " + servers.runningServer() + " time rn baybee",
                    "i'll keep hosting " + servers.runningServer() + " instead ok"
                ]))
        elif message.content == "!tf2ip":
            if servers.runningServer():
                r = requests.get('https://ipecho.net/plain')
                await message.channel.send(r.text)

        # css
        elif message.content == "!hostcss" and permissions.allowed(message.author.id, "blue"):
            if not servers.runningServer():
                await message.channel.send(helperfunctions.pick_string([
                    "hhhhnnnnnnngggggg...",
                    "*inhales*",
                    "ok one sec"
                ]))
                # first get game server account login token
                token = ""
                if os.path.exists('/home/william/Steam/steamapps/common/Counter-Strike Source Dedicated Server/' + 'token.txt'):
                    f = open('/home/william/Steam/steamapps/common/Counter-Strike Source Dedicated Server/' + 'token.txt', "r")
                    token = f.read()
                    f.close()
                else:
                    await message.channel.send("will doesn't have the token set up right")
                    return
                subprocess.Popen(['bash','srcds_run', '-game', 'cstrike', '+maxplayers', '16', '+map', 'de_dust2', '+sv_setsteamaccount', token], cwd=r'/home/william/Steam/steamapps/common/Counter-Strike Source Dedicated Server', stdin=subprocess.PIPE)
                helperfunctions.bot_wait()
                await message.channel.send(helperfunctions.pick_string([
                    "ok im runnin",
                    "epic cs:s",
                    "aw yeah shoot em up baybee :)"
                ]))
            else:
                await message.channel.send(helperfunctions.pick_string([
                    "looks like i'm already running " + servers.runningServer(),
                    "it's already " + servers.runningServer(),
                    "it's actually " + servers.runningServer() + " time rn baybee",
                    "i'll keep hosting " + servers.runningServer() + " instead ok"
                ]))
        elif message.content == "!cssip":
            if servers.runningServer():
                r = requests.get('https://ipecho.net/plain')
                await message.channel.send(r.text)

        # ttt
        elif message.content == "!hostttt" and permissions.allowed(message.author.id, "blue"):
            if not servers.runningServer():
                # figure out map first
                map = 'ttt_rooftops_2016_v1'
                if len(message.content) > 8:
                    map = message.content[9:]
                    map = helperfunctions.sanitize(map)
                    if map not in ['ttt_rooftops_2016_v1', 'ttt_college']:
                        await message.channel.send("that's not a map i can start on")
                        return
                await message.channel.send(helperfunctions.pick_string([
                    "hhhhnnnnnnngggggg...",
                    "*inhales*",
                    "ok one sec"
                ]))
                # first get game server account login token
                token = ""
                if os.path.exists('/home/william/Steam/steamapps/common/GarrysModDS/' + 'token.txt'):
                    f = open('/home/william/Steam/steamapps/common/GarrysModDS/' + 'token.txt', "r")
                    token = f.read()
                    f.close()
                else:
                    await message.channel.send("will doesn't have the token set up right")
                    return
                subprocess.Popen(['bash','srcds_run', '-game', 'garrysmod', '+gamemode', 'terrortown', '+maxplayers', '16', '+map', map, '+host_workshop_collection', '3100438906', '+sv_setsteamaccount', token], cwd=r'/home/william/Steam/steamapps/common/GarrysModDS', stdin=subprocess.PIPE)
                helperfunctions.bot_wait_medium()
                await message.channel.send(helperfunctions.pick_string([
                    "ok im runnin",
                    "epic ttt",
                    "I'M INNO"
                ]))
            else:
                await message.channel.send(helperfunctions.pick_string([
                    "looks like i'm already running " + servers.runningServer(),
                    "it's already " + servers.runningServer(),
                    "it's actually " + servers.runningServer() + " time rn baybee",
                    "i'll keep hosting " + servers.runningServer() + " instead ok"
                ]))
        elif message.content == "!tttip":
            if servers.runningServer():
                r = requests.get('https://ipecho.net/plain')
                await message.channel.send(r.text)

        # tron
        elif message.content == "!hosttron" and permissions.allowed(message.author.id, "blue"):
            if not servers.runningServer():
                await message.channel.send(helperfunctions.pick_string([
                    "hhhhnnnnnnngggggg...",
                    "*inhales*",
                    "ok one sec"
                ]))
                subprocess.Popen(['bash', '-c', './AppRun'], cwd=r'/home/william/armagetron/squashfs-root', stdin=subprocess.PIPE)
                helperfunctions.bot_wait_medium()
                await message.channel.send(helperfunctions.pick_string([
                    "ok im runnin",
                    "epic tron",
                    "its the game grid :O"
                ]))
            else:
                await message.channel.send(helperfunctions.pick_string([
                    "looks like i'm already running " + servers.runningServer(),
                    "it's already " + servers.runningServer(),
                    "it's actually " + servers.runningServer() + " time rn baybee",
                    "i'll keep hosting " + servers.runningServer() + " instead ok"
                ]))
        elif message.content == "!tronip":
            if servers.runningServer():
                r = requests.get('https://ipecho.net/plain')
                await message.channel.send(r.text + ":4535")


        # poweroff                
        elif message.content == "!stophost" and permissions.allowed(message.author.id, "blue"):
            if servers.runningServer():
                subprocess.run(['pkill', '-f', '\'bash launch.sh\''])
                subprocess.run(['pkill', '-f', 'server.jar'])
                subprocess.run(['pkill', '-f', 'svends'])
                subprocess.run(['pkill', '-f', 'srcds'])
                subprocess.run(['pkill', '-f', 'armagetronad-dedicated'])
                await message.channel.send(helperfunctions.pick_string([
                    "it's dead, jim",
                    "kablam",
                    "kablooie",
                    "die die die die die die die die",
                    "goodnight little fishie"
                ]))
            else:
                await message.channel.send("im not hosting anything rn")

    def runningServer():
        out = ""
        try:
            subprocess.check_output(["pgrep", '-f', "server.jar"])
            out = "minecraft"
        except subprocess.CalledProcessError as e:
            try:
                subprocess.check_output(["pgrep", '-f', "svends"])
                out = "sven"
            except subprocess.CalledProcessError as e:
                try:
                    subprocess.check_output(["pgrep", '-f', "srcds"])
                    out = "a source game"
                except subprocess.CalledProcessError as e:
                    try:
                        subprocess.check_output(["pgrep", '-f', "armagetronad-dedicated"])
                        out = "tron"
                    except subprocess.CalledProcessError as e:
                        return ""
        return out

    def save():
        global mcIP
        db.put_item(TableName="trashbot", Item={'name':{'S':'mc_ip'}, 'data':{'S':mcIP}})
