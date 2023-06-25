import json
import helperfunctions
from helperfunctions import pick_string
from permissions import permissions
import boto3
import logcommand, logging
import re

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global participants
participants = {}

class lipo:

    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'lipo'}})
        global participants
        participants = json.loads(d['Item']['data']['S'])

    async def run(self, message):
        global participants
        if (message.content.startswith("!lipo")):
            if ' ' not in message.content:
                az = list(map(chr, range(97, 123)))
                c = pick_string(az)
            elif len(message.content[message.content.index(' ')+1:]) == 1 and message.content[message.content.index(' ')+1:].isascii():
                c = message.content[message.content.index(' ')+1:].lower()
            elif len(message.content[message.content.index(' ')+1:]) > 1:
                await message.channel.send("you can only start a lipogram challenge on a single character")
                return
            elif not message.content[message.content.index(' ')+1:].isascii():
                await message.channel.send("ascii characters only please. blame sloss and panic")
            if message.author.id not in participants:
                participants[message.author.id] = {}
                participants[message.author.id]['c'] = c
                participants[message.author.id]['points'] = 0
                await message.channel.send(message.author.mention + ", you have started a lipogram challenge for the letter `" + c + "`. Have fun!")
                logcommand.log_globally(logging.INFO, "New lipo challenge started by " + message.author.name + " for letter `" + c + "`")
                lipo.save()
            else:
                await message.channel.send("you're doing a lipo challenge for letter `" + participants[message.author.id]['c'] + "` with `" + str(participants[message.author.id]['points']) + " points`")
        else:
            if message.author.id in participants:
                if participants[message.author.id]['c'] in message.content.lower():
                    # extract all of the character words found in the string
                    words = re.split('\W+', message.content.lower())
                    # filter down to just the words containing the keyword
                    matches = [a for a in words if participants[message.author.id]['c'] in a]
                    if len(matches) == 0:
                        matches = ["https://media.discordapp.net/attachments/555540666776813568/1122654677574635530/293.jpg"]
                    await message.channel.send(pick_string(["epic fail (" + str(participants[message.author.id]['points']) + " points)",
                    "lipogram challenge failed (" + str(participants[message.author.id]['points']) + " points)",
                    "it was a good try but you failed after " + str(participants[message.author.id]['points']) + "messages",
                    "no dice, i see a `" + participants[message.author.id]['c'] + "` in there (" + str(participants[message.author.id]['points']) + " points)",
                    "sadly you're not allowed to say `" + pick_string(matches) + "` (" + str(participants[message.author.id]['points']) + " points)",
                    "lol this user said " + pick_string(matches) + " (" + str(participants[message.author.id]['points']) + " points)",
                    "laugh at this user they used letter" + participants[message.author.id]['c'] + " (" + str(participants[message.author.id]['points']) + " points)",
                    "YOU CAN\"T SAY `" + pick_string(matches) + "` LOLLLLLLL (" + str(participants[message.author.id]['points']) + " points)"]))
                    logcommand.log_globally(logging.INFO, "`" + participants[message.author.id]['c'] + "` lipogram challenge for " + message.author.name + " has ended with `" + str(participants[message.author.id]['points']) + "` points.")
                    participants.pop(message.author.id, None)
                else:
                    participants[message.author.id]['points'] += 1
                lipo.save()
                    
    def save():
        # we have to do shenanigans here to be able to serialize our dict with tuple keys
        db.put_item(TableName="trashbot", Item={'name':{'S':'lipo'}, 'data':{'S':json.dumps(participants)}})