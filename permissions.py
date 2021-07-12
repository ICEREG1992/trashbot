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
                name = await client.fetch_user(self, user_id=id)
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
        elif (message.content.startswith("!keycard ")):
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

    def get_users(color):
        if color in perms:
            return perms[color]

    def allowed(id, *colors):
        for color in colors:
            if color in perms and str(id) in perms[color]:
                return True
        return False

    def save():
        db.put_item(TableName="trashbot", Item={'name':{'S':'permissions'}, 'data':{'S':json.dumps(perms)}})