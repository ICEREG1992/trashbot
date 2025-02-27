import json
import discord
import helperfunctions
import humanize
import datetime as dt
from helperfunctions import pick_string
from permissions import permissions
from operator import attrgetter
import boto3
import logcommand, logging
import re
import string

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global participants
participants = {}

class pan:

    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'pan'}})
        global participants
        participants = json.loads(d['Item']['data']['S'])

    async def run(self, message):
        global participants
        uid = str(message.author.id)
        if (message.content.startswith("!panboard")):
            t = pick_string(["🏆 currently running pangram challenges:\n",
            "🏆 get a load a these top " + (str(len(participants)) if len(participants) < 9 else "eight") + " nerds:\n",
            "🏆 here's currently pangrams:\n",
            "🏆 check check check check it out:\n",
            "🏆 eight"])
            embed = discord.Embed(title=t)
            for l in sorted(participants.items(), key=lambda item: item[1]['points'], reverse=True)[0:8]:
                embed.add_field(name=l[1]['name'], value=str(l[1]['points']) + " points since <t:" + str(int(l[1]['start'])) + ">", inline=False)
            await message.channel.send(embed=embed)
        elif (message.content.equals("!pan")):
            if uid not in participants:
                participants[uid] = {}
                participants[uid]['points'] = 0
                participants[uid]['name'] = message.author.name
                participants[uid]['start'] = dt.datetime.now().timestamp()
                participants[uid]['best'] = ""
                await message.channel.send(message.author.mention + ", you have started a pangram challenge. every message you send must contain all letters of the alphabet. for more information, read a book.")
                logcommand.log_globally(logging.INFO, "New pangram challenge started by " + message.author.name)
                pan.save()
            else:
                await message.channel.send("you're doing a pangram challenge with `" + str(participants[uid]['points']) + " points`")
        else:
            st = message.content.lower()
            if uid in participants:
                if not set(string.ascii_lowercase).issubset(set(st.lower())): # pangram check is here
                    misses = list(set(string.ascii_lowercase) - set(st))
                    if (participants[uid]['points'] == 0):
                        await message.reply(pick_string(["YOU DON'T HAVE TO DO A PANGRAM IF YOU DON'T WANT TO (" + str(participants[uid]['points']) + " points)",
                        "THE JOKE ISN'T FUNNY. YOU LOSE. (" + str(participants[uid]['points']) + " points)",
                        "DID YOU ENJOY YOURSELF? (" + str(participants[uid]['points']) + " points)",
                        "HAHAHAHAHAHAHA GOOD ONE I LIKED THAT ONE SEE YOU STARTED A PANGRAM THEN IMMEDIATELY FAILED SO FUNNY (" + str(participants[uid]['points']) + " points)",
                        "BRUH (" + str(participants[uid]['points']) + " points)"]))
                    else:
                        await message.reply(pick_string(["epic fail (" + str(participants[uid]['points']) + " points)",
                        "pangram challenge failed (" + str(participants[uid]['points']) + " points)",
                        "it was a good try but you failed after " + str(participants[uid]['points']) + " messages",
                        "no dice, i don't see a `" + pick_string(misses) + "` in there (" + str(participants[uid]['points']) + " points)",
                        "sadly you had to say `" + pick_string(misses) + "` (" + str(participants[uid]['points']) + " points)",
                        "lol this user didn't have a `" + pick_string(misses) + "` (" + str(participants[uid]['points']) + " points)",
                        "laugh at this user they didn't use letter `" + pick_string(misses) + "` (" + str(participants[uid]['points']) + " points)",
                        "YOU ACTUALLY FORGOT `" + pick_string(misses) + "` LOLLLLLLL (" + str(participants[uid]['points']) + " points)"]))
                    logcommand.log_globally(logging.INFO, "pangram challenge for " + message.author.name + " has ended with `" + str(participants[uid]['points']) + "` points.")
                    participants.pop(uid, None)
                else:
                    participants[uid]['points'] += 1
                    if 'best' in participants[uid] and len(st) > len(participants[uid]['best']):
                        participants[uid]['best'] = st
                pan.save()
                    
    def save():
        global participants
        # we have to do shenanigans here to be able to serialize our dict with tuple keys
        db.put_item(TableName="trashbot", Item={'name':{'S':'pan'}, 'data':{'S':json.dumps(participants)}})
