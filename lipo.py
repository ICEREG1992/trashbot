import json
import helperfunctions
import datetime as dt
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
        uid = str(message.author.id)
        if (message.content.startswith("!lipo ")):
            if ' ' not in message.content:
                az = list(map(chr, range(97, 123)))
                c = pick_string(az)
            elif len(message.content[6:]) >= 1:
                c = message.content[6:].lower()
            if uid not in participants:
                participants[uid] = {}
                participants[uid]['c'] = c
                participants[uid]['points'] = 0
                participants[uid]['name'] = message.author.name
                participants[uid]['start'] = dt.datetime.utcnow().timestamp()
                participants[uid]['best'] = ""
                if len(c) > 1:
                    await message.channel.send(message.author.mention + ", you have started a lipogram challenge for the letters in `" + c + "`. Have fun!")
                else:
                    await message.channel.send(message.author.mention + ", you have started a lipogram challenge for the letter `" + c + "`. Have fun!")
                logcommand.log_globally(logging.INFO, "New lipo challenge started by " + message.author.name + " for letter `" + c + "`")
                lipo.save()
            else:
                c = participants[uid]['c']
                if len(c) > 1:
                    await message.channel.send("you're doing a lipo challenge for the letters in `" + c + "` with `" + str(participants[uid]['points']) + " points`")
                else:
                    await message.channel.send("you're doing a lipo challenge for letter `" + c + "` with `" + str(participants[uid]['points']) + " points`")
        elif (message.content.startswith("!lipoboard")):
            out = pick_string(["currently running lipo challenges:\n",
            "get a load a these nerds:\n",
            "here's currently lipos:\n",
            "check check check check it out:\n"])
            for uid in participants:
                out += "**" + participants[uid]['name'] + "**: " + str(participants[uid]['points']) + " points on `" + participants[uid]['c'] + "`\n")
            await message.channel.send(out)
        else:
            st = message.content.lower()
            # if re.fullmatch(r'https?:\/\/(?:www\.)?(?:(?:t(?:e|x)nor\.com\/vi(?:e|x)w\/)|(?:giphy\.com\/gifs\/)|(?:[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)\.(jpg|jpeg|png|gif|gifv|webm|mp4|mov)))(?:\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*))?', str): # should cover most image embed type that shows up on discord, doesnt match if the text is not shown (WILL MATCH 'message [link]' AND WHATNOT, WILL MATCH YT/TWITTER/SPOTIFY LINKS)
                # return # idk feel free to reward points i dont think it should count lol
            st = re.sub(r'[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)', '', st) # erase all URLs
            st = re.sub(r'(<a?)?:\w+:(\d{18}>)?', '', st) # erase discord emojis
            if uid in participants:
                matches = None
                for n in participants[uid]['c']:
                    if n in st:
                        # extract all of the character words found in the string
                        words = re.split('\W+', st)
                        # filter down to just the words containing the keyword
                        matches = [[a for a in words if n in a], n]
                        if len(matches[0]) == 0:
                            matches[0] = n
                        break
                if matches:
                    if (participants[uid]['points'] == 0):
                        await message.channel.send(pick_string(["YOU DON'T HAVE TO DO A LIPO IF YOU DON'T WANT TO (" + str(participants[uid]['points']) + " points)",
                        "THE JOKE ISN'T FUNNY. YOU LOSE. (" + str(participants[uid]['points']) + " points)",
                        "DID YOU ENJOY YOURSELF? (" + str(participants[uid]['points']) + " points)",
                        "HAHAHAHAHAHAHA GOOD ONE I LIKED THAT ONE SEE YOU STARTED A LIPO THEN IMMEDIATELY FAILED SO FUNNY (" + str(participants[uid]['points']) + " points)",
                        "BRUH (" + str(participants[uid]['points']) + " points)"]))
                    await message.channel.send(pick_string(["epic fail (" + str(participants[uid]['points']) + " points)",
                    "lipogram challenge failed (" + str(participants[uid]['points']) + " points)",
                    "it was a good try but you failed after " + str(participants[uid]['points']) + " messages",
                    "no dice, i see a `" + matches[1] + "` in there (" + str(participants[uid]['points']) + " points)",
                    "sadly you're not allowed to say `" + pick_string(matches[0]) + "` (" + str(participants[uid]['points']) + " points)",
                    "lol this user said " + pick_string(matches[0]) + " (" + str(participants[uid]['points']) + " points)",
                    "laugh at this user they used letter " + matches[1] + " (" + str(participants[uid]['points']) + " points)",
                    "YOU CAN\"T SAY `" + pick_string(matches[0]) + "` LOLLLLLLL (" + str(participants[uid]['points']) + " points)"]))
                    logcommand.log_globally(logging.INFO, "`" + participants[uid]['c'] + "` lipogram challenge for " + message.author.name + " has ended with `" + str(participants[uid]['points']) + "` points.")
                    participants.pop(uid, None)
                else:
                    participants[uid]['points'] += 1
                    if 'best' in participants[uid] and len(st) > len(participants[uid]['best']):
                        participants[uid]['best'] = st
                lipo.save()
                    
    def save():
        # we have to do shenanigans here to be able to serialize our dict with tuple keys
        db.put_item(TableName="trashbot", Item={'name':{'S':'lipo'}, 'data':{'S':json.dumps(participants)}})
