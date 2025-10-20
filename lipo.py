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
        uid = str(message.author.id)
        if (message.content.startswith("!lipoboard")):
            t = pick_string(["🏆 currently running lipo challenges:\n",
            "🏆 get a load a these top " + (str(len(participants)) if len(participants) < 9 else "eight") + " nerds:\n",
            "🏆 here's currently lipos:\n",
            "🏆 check check check check it out:\n",
            "🏆 eight"])
            embed = discord.Embed(title=t)
            for l in sorted(participants.items(), key=lambda item: item[1]['points'], reverse=True)[0:8]:
                embed.add_field(name=l[1]['name'], value=str(l[1]['points']) + " points for `" + (l[1]['c'] if len(l[1]['c']) <= 26 else (l[1]['c'][0:26] + "...")) + "` since <t:" + str(int(l[1]['start'])) + ">", inline=False)
                # embed.add_field(name="lipo", value=l[1]['c'], inline=True)
                # embed.add_field(name="for", value=humanize.precisedelta(dt.timedelta(seconds=dt.datetime.utcnow().timestamp()-l[1]['start']), minimum_unit='hours', suppress=['microseconds','seconds','minutes']))
                # out += "**" + participants[uid]['name'] + "**: " + str(participants[uid]['points']) + " points on `" + participants[uid]['c'] + "`\n"
            await message.channel.send(embed=embed)
        elif (message.content.startswith("!lipo")):
            if ' ' not in message.content:
                az = list(map(chr, range(97, 123)))
                c = pick_string(az)
            elif message.content[6:].isdigit() and int(message.content[6:]) > 1999:
                await message.channel.send('please try a lower character limit please')
                return
            elif len(message.content[6:]) >= 1:
                c = message.content[6:].lower()
            if uid not in participants:
                participants[uid] = {}
                participants[uid]['c'] = c
                participants[uid]['points'] = 0
                participants[uid]['name'] = message.author.name
                participants[uid]['start'] = dt.datetime.now().timestamp()
                participants[uid]['best'] = ""
                if c.isdigit():
                    await message.channel.send(message.author.mention + ", you have started a lipogram challenge for words with `" + c + "` letters or fewer. Have fun!")
                if c == 'qat':
                    await message.channel.send(message.author.mention + ", you have started a lipogram challenge for sentences in [qat](https://www.quinapalus.com/qat.html) order. Have fun!")
                elif len(c) > 1:
                    await message.channel.send(message.author.mention + ", you have started a lipogram challenge for the letters in `" + c + "`. Have fun!")
                else:
                    await message.channel.send(message.author.mention + ", you have started a lipogram challenge for the letter `" + c + "`. Have fun!")
                logcommand.log_globally(logging.INFO, "New lipo challenge started by " + message.author.name + " for letter `" + c + "`")
                lipo.save()
            else:
                c = participants[uid]['c']
                if c.isdigit():
                    await message.channel.send("you're doing a lipo challenge for words with `" + c + "` letters or fewer with `" + str(participants[uid]['points']) + " points`")
                if c == 'qat':
                    await message.channel.send("you're doing a lipo challenge for sentences in [qat](https://www.quinapalus.com/qat.html) order with `" + str(participants[uid]['points']) + " points`")
                elif len(c) > 1:
                    await message.channel.send("you're doing a lipo challenge for the letters in `" + c + "` with `" + str(participants[uid]['points']) + " points`")
                else:
                    await message.channel.send("you're doing a lipo challenge for letter `" + c + "` with `" + str(participants[uid]['points']) + " points`")
        else:
            st = message.content.lower()
            # if re.fullmatch(r'https?:\/\/(?:www\.)?(?:(?:t(?:e|x)nor\.com\/vi(?:e|x)w\/)|(?:giphy\.com\/gifs\/)|(?:[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)\.(jpg|jpeg|png|gif|gifv|webm|mp4|mov)))(?:\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*))?', str): # should cover most image embed type that shows up on discord, doesnt match if the text is not shown (WILL MATCH 'message [link]' AND WHATNOT, WILL MATCH YT/TWITTER/SPOTIFY LINKS)
                # return # idk feel free to reward points i dont think it should count lol
            st = re.sub(r'https?:\/\/[^\s<]+[^<.,:;"\'\]\s]', '', st) # erase all URLs
            st = re.sub(r'<(?:(?:a?:\w+:)|(?:\@\&?)|\#)\d{1,19}>', '', st) # erase emojis, channel tags and user/role mentions
            if uid in participants:
                matches = None
                # account for word length lipo
                if participants[uid]['c'].isdigit():
                    # extract all of the character words found in the string
                    words = re.split('\W+', st)
                    # filter down to just the words longer than the max length
                    matches = [[a for a in words if len(a) > int(participants[uid]['c'])], 'word longer than ' + participants[uid]['c'] + ' letters']
                    if len(matches[0]) == 0:
                        matches = None
                elif participants[uid]['c'] == 'qat':
                    # extract all of the character words found in the string, allowing for apostrophes
                    words = re.split(r"[^\w'-]+", st)
                    # make sure words are in order by word length followed by alphabetical order
                    sorted_words = sorted(words, key=lambda w: (lipo.qat_length(w), w))
                    if words != sorted_words:
                        # matches is an array with the first word that is out of order in index 0 followed by the reason in index 1
                        for i in range(min(len(words), len(sorted_words))):
                            if words[i] != sorted_words[i]:
                                matches = [[words[i]], 'word out of qat order']
                                break
                else:
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
                        await message.reply(pick_string(["YOU DON'T HAVE TO DO A LIPO IF YOU DON'T WANT TO (" + str(participants[uid]['points']) + " points)",
                        "THE JOKE ISN'T FUNNY. YOU LOSE. (" + str(participants[uid]['points']) + " points)",
                        "DID YOU ENJOY YOURSELF? (" + str(participants[uid]['points']) + " points)",
                        "HAHAHAHAHAHAHA GOOD ONE I LIKED THAT ONE SEE YOU STARTED A LIPO THEN IMMEDIATELY FAILED SO FUNNY (" + str(participants[uid]['points']) + " points)",
                        "BRUH (" + str(participants[uid]['points']) + " points)"]))
                    else:
                        await message.reply(pick_string(["epic fail (" + str(participants[uid]['points']) + " points)",
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
        global participants
        # we have to do shenanigans here to be able to serialize our dict with tuple keys
        db.put_item(TableName="trashbot", Item={'name':{'S':'lipo'}, 'data':{'S':json.dumps(participants)}})

    def qat_length(w):
        length = len(re.sub(r"[-']", '', w))
        return (length)