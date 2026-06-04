import json
import os
from helperfunctions import pick_string
from logcommand import log_globally
import logging
import boto3

logging.basicConfig(level=logging.INFO)

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global perms
perms = {}

class permissions:

    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'permissions'}})
        global perms
        perms = json.loads(d['Item']['data']['S'])

    async def run(self, message, client):
        if (message.content.startswith("!give ")):
            if (permissions.allowed(message.author.id, "blue")):
                color_and_user = message.content[6:]
                color = color_and_user[0:color_and_user.index("keycard ")-1]
                id = str(message.raw_mentions[0])
                name = await client.fetch_user(self, id)
                name = name.name
                permissions.add_user(id, name, color)
                await message.channel.send("User <@" + str(id) + "> given " + color + " keycard.")
                log_globally(logging.INFO, message.mentions[0].name + " given " + color + " keycard by " + message.author.name)
            else:
                await message.channel.send("You need a blue keycard to do that, " + message.author.name + ".")
        elif (message.content.startswith("!revoke ")):
            if (permissions.allowed(message.author.id, "blue")):
                color_and_user = message.content[8:]
                color = color_and_user[0:color_and_user.index("keycard ")-1]
                id = str(message.raw_mentions[0])
                permissions.remove_user(id, color)
                await message.channel.send("<@" + str(id) + ">'s " + color + " keycard has been revoked. Sorry about that.")
                log_globally(logging.INFO, message.mentions[0].name + " revoked " + color + " keycard by " + message.author.name)
            else:
                await message.channel.send("You need a blue keycard to do that, " + message.author.name + ".")
        elif (message.content.startswith(("!keycard ", "!keycards ")) and len(message.mentions) == 0):
            color = message.content[9:]
            await message.channel.send(
                pick_string([
                    "**here's everyone with the " + color + " keycard:**\n",
                    "**yup, all " + color + " keycard members:**\n",
                    "**here ya go, boss:**\n",
                    "**can do,, here's all " + color + " keycards:**\n",
                    "**hot and ready, " + color + " keycards for your heady:**\n"
                ]) + str(permissions.get_users(color))
            )
            return
        elif (message.content.startswith(("!keycard ", "!keycards "))):
            user = message.mentions[0].id
            await message.channel.send(
                pick_string([
                    "**here's all the keycards " + message.mentions[0].name + " has:**\n"
                ]) + str(permissions.get_colors(user))
            )
        elif (message.content.startswith("!addallowedchannel ")):
            if (permissions.allowed(message.author.id, "blue")):
                channel_id = message.content[19:]
                channel_id = channel_id.strip("<#>")
                permissions.add_allowed_channel(channel_id)
                await message.channel.send("Channel <#" + channel_id + "> added to allowed channels.")
            else:
                await message.channel.send("You need a blue keycard to do that, " + message.author.name + ".")
        elif (message.content.startswith("!removeallowedchannel ")):
            if (permissions.allowed(message.author.id, "blue")):
                channel_id = message.content[22:]
                channel_id = channel_id.strip("<#>")
                permissions.remove_allowed_channel(channel_id)
                await message.channel.send("Channel <#" + channel_id + "> removed from allowed channels.")
            else:
                await message.channel.send("You need a blue keycard to do that, " + message.author.name + ".")
            
        return

    def add_user(id, name, color):
        if color not in perms:
            perms[color] = {}
        perms[color][id] = name
        permissions.save()

    def remove_user(id, color):
        if color in perms:
            if str(id) in perms[color]:
                perms[color].pop(str(id))
            if len(perms[color]) == 0:
                perms.pop(color, None)
        permissions.save()

    def add_allowed_channel(channel_id):
        if "allowed_channels" not in perms:
            perms["allowed_channels"] = []
        if channel_id not in perms["allowed_channels"]:
            perms["allowed_channels"].append(channel_id)
        permissions.save()

    def remove_allowed_channel(channel_id):
        if "allowed_channels" in perms:
            if channel_id in perms["allowed_channels"]:
                perms["allowed_channels"].remove(channel_id)
        permissions.save()

    def get_users(color):
        if color in perms:
            return perms[color]

    def get_colors(user):
        out = []
        for color in perms:
            if str(user) in perms[color]:
                out.append(color)
        return out

    def allowed(id, *colors):
        for color in colors:
            if color in perms and str(id) in perms[color]:
                return True
        return False
    
    def allowed_channel(channel_id):
        if "allowed_channels" in perms:
            return str(channel_id) in perms["allowed_channels"]
        return False

    def save():
        db.put_item(TableName="trashbot", Item={'name':{'S':'permissions'}, 'data':{'S':json.dumps(perms)}})