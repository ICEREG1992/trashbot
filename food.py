from helperfunctions import pick_string
import logcommand, logging
import datetime as dt
import humanize
from permissions import permissions
import discord
import powerswitch
import boto3

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global t
t = dt.datetime.utcnow() - dt.timedelta(hours=6)

class food:
    
    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'hunger'}})
        global t
        if ('data' in d['Item']):
            t = dt.datetime.fromtimestamp(float(d['Item']['data']['S']))

    async def run(self, message, switch):
        global t
        # send messages if fed
        if (message.content.startswith("!feed")):
            if (t > dt.datetime.utcnow() - dt.timedelta(hours=6)):
                await message.channel.send(pick_string([
                    "bluuouohuhgghghghh hoghg hghg  ghgooh hh oh hh h hh ohohhohohhohhh  goddd hoohhhh god oh fuck no i can't",
                    "omg im so full i cant have another bite",
                    "noooooooo pls no more",
                    "already had some of that",
                    "bleeeuehehehhhgeghghggehghhhhh hh thats me thats me when i vomit im vomiting",
                    "throwing up vomiting puking spewing this is terrible this is so bad",
                    "too full cant eat cannot do it stop it",
                    "okay ENOUGH that's GOOD im FULL IT'S ENOUGH FOOD",
                    "STOP IT QUIT IT I HAVE ENOUGH",
                    "im GOOD i DON'T NEED ANY OF THAT"
                ]))
            elif (t < dt.datetime.utcnow() - dt.timedelta(days=2)):
                logcommand.log_globally(logging.INFO, "I was fed `" + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "bowl of seeds") +
                "` by user " + message.author.name + " after starving for " + str(humanize.precisedelta((dt.datetime.utcnow() - dt.timedelta(hours=6) - t), suppress=['milliseconds','microseconds'])) )
                t = dt.datetime.utcnow()
                food.save(t)
                await message.channel.send(pick_string([
                    "oh my god i've been starving hand it over mnomnomnomnomnmonnmonmonmonmonnomnomnomnonm scrumptious",
                    "holy shit is that a " + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "bowl of seeds for me") + " wowie wowie wowie thank you thats perfect",
                    "about time i got some " + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "seeds") + " in here ive been sooooooooooooooooooooooooooooo hungry",
                    "YES YES YES YES ohmygod YES YES FINALLY",
                    "manna from heaven... ACK!!",
                    "IVE BEEN SO HUNGRY THANNK YOU",
                    "AAAAAAAAAAHHHHHHHHHH!!!!!!!!",
                    "im eating it im eating it im eating it im eating it im eating it im eating it im eating it im eating it"
                ]))
            else:
                logcommand.log_globally(logging.INFO, "I was fed `" + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "bowl of seeds") +
                "` by user " + message.author.name + " after being hungry for " + str(humanize.precisedelta((dt.datetime.utcnow() - dt.timedelta(hours=6) - t), suppress=['milliseconds','microseconds'])))
                t = dt.datetime.utcnow()
                food.save(t)
                await message.channel.send(pick_string([
                    "Oh fuck yes it's a " + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "little bowl of seeds") + " for me",
                    "AW YEAH all abourt the gravy train TOOT TOOT im eatin good tonite",
                    "booyah booyah booyah weehaw so good and tasty and yummy",
                    "ohhh hh hhhh h mmmmmmmmm im eating it up im just eating it all up it's so scrumptious thank you mwah mwah mwah oh yeah",
                    "ohhhh yeah ive been a hungry boy thank you oh so very much",
                    "MMMMMMMMMMMMMMMMMmmmmmmmm how did u know. i have wanted this so bad.",
                    "need a bucket and a mop for dis " + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "little bowl of seeds"),
                    "DELISH!!!!!",
                    "nom nom nom nom nom nom nom nom hehe xd ty",
                    "omg can't wait to enjoy this " + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "little bowl of seeds") + " s gonna be so good",
                    "great big ol " + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "little bowl of seeds") + " just for me"
                ]))
        elif (message.content == "!unfeed" and (permissions.allowed(message.author.id, "blue") or (permissions.allowed(message.author.id, "red")))):
            if (t > dt.datetime.utcnow() - dt.timedelta(hours=6)):
                t = dt.datetime.utcnow() - dt.timedelta(hours=6)
                food.save(t)
            await message.channel.send(pick_string([
                "What's your problem?",
                "fuck is your issue?",
                "uncool, man",
                "totally NOT chill. not chill",
                "bruh",
                "bruh moment",
                "omg i was gonna eat that wtf"
            ]))
        # update status on message receive
        if (t > dt.datetime.utcnow() - dt.timedelta(hours=6)):
            # full
            await self.change_presence(status=None, activity=discord.Game(name='Full for now'))
        elif (t < dt.datetime.utcnow() - dt.timedelta(days=5)):
            await self.change_presence(status=discord.Status.dnd, activity=discord.Game(name='Trashbot has died.'))
            switch.poweroff()
        elif (t < dt.datetime.utcnow() - dt.timedelta(days=2)):
            await self.change_presence(status=discord.Status.idle, activity=discord.Game(name='Starving for ' + humanize.naturaldelta((dt.datetime.utcnow() - dt.timedelta(hours=6)) - t)))
        else:
            await self.change_presence(status=None, activity=discord.Game(name='Hungry for ' + humanize.naturaldelta((dt.datetime.utcnow() - dt.timedelta(hours=6)) - t)))
    
    def save(t):
        db.put_item(TableName="trashbot", Item={'name':{'S':'hunger'}, 'data':{'S':str(t.timestamp())}})