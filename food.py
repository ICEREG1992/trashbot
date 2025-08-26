from helperfunctions import pick_string,chance
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
t = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=6)

class food:
    
    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'hunger'}})
        global t
        if ('data' in d['Item']):
            t = dt.datetime.fromtimestamp(float(d['Item']['data']['S']), tz=dt.timezone.utc)

    async def run(self, message, switch):
        global t
        # send messages if fed
        if (message.content.startswith("!feed")):
            if (t > dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=6)):
                if message.content[message.content.index(' ')+1:] is "cheeseburger":
                    await message.channel.send(pick_string([
                        "actually nevermind i dont want anything"
                    ]))
                if chance(10):
                    await message.channel.send(pick_string([
                        "i guess i could have a bite but i wont",
                        "no thanks",
                        "ehhh im a little full",
                        "can you box it up to go please",
                        "maybe later",
                        "uhhh",
                        "i would rather have a cheeseburger"
                    ]))
                else:
                    await message.channel.send(pick_string([
                        "i really really really don't want to eat that",
                        "omg im so full i cant have another bite",
                        "noooooooo pls no more",
                        "already had some of that",
                        "not gonna eat that thanks but actually no thanks because i'm not gonna eat it",
                        "I DONT WANT THAT",
                        "i'm too full to have any of that !!",
                        "THAT'S ENOUGH TO EAT",
                        "stop that please",
                        "im really fine i don't need any more pls"
                    ]))
            elif (t < dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=2)):
                logcommand.log_globally(logging.INFO, "I was fed `" + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "bowl of seeds") +
                "` by user " + message.author.name + " after starving for " + str(humanize.precisedelta((dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=6) - t), suppress=['milliseconds','microseconds'])) )
                t = dt.datetime.now(dt.timezone.utc)
                food.save(t)
                await message.channel.send(pick_string([
                    "that looks reeeeaallllyyy good hand that over nomnomnom",
                    "holy shit is that a " + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "bowl of seeds for me") + " that's gonna hit the spot",
                    "about time i got some " + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "seeds") + " in here ive been literally starving",
                    "YES YES YES YES ohmygod YES YES FINALLY",
                    "manna from heaven...",
                    "IVE BEEN SO HUNGRY THANNK YOU",
                    "AAAAAAAAAAHHHHHHHHHH!!!!!!!!",
                    "scrumptious (this message written by user noneuclidean)",
                    "im eating it im eating it im eating it im eating it im eating it im eating it im eating it im eating it"
                ]))
            else:
                logcommand.log_globally(logging.INFO, "I was fed `" + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "bowl of seeds") +
                "` by user " + message.author.name + " after being hungry for " + str(humanize.precisedelta((dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=6) - t), suppress=['milliseconds','microseconds'])))
                t = dt.datetime.now(dt.timezone.utc)
                food.save(t)
                if chance(90): # regular response
                    await message.channel.send(pick_string([
                        "Oh fuck yes it's a " + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "little bowl of seeds") + " for me",
                        "LFG i got a " + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "little bowl of seeds"),
                        "WAHOO that looks really good thx nomnomnom",
                        "i'm eating it, and it's really delish, thank you so much",
                        "i've been a teeny tiny hungry boy and this looks rly rly good wow",
                        "wow that. that looks really fucking ggood im gonna eat this up",
                        "need a bucket and a mop for dis " + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "little bowl of seeds"),
                        "DELISH!!!!!",
                        "nom nom nom nom nom nom nom nom hehe xd ty",
                        "omg this " + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "little bowl of seeds") + " is gonna be so good to eat",
                        "great big ol " + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "little bowl of seeds") + " just for me",
                        "THAT'S RIGHT! another big tasty meal in the books for trashbot",
                        "here we go here we go here we go omg im eating it",
                        "chewing and chewing and chewing IT'S REALLY GOOD",
                        "wouldn't mind having some of that!! wow this is good",
                        "it's actually really good to eat and have",
                        "thank you it's really tasty",
                        "i really like that and i'm eating it take a look i'm taking a bite 👄",
                        "omg nice looks rly good",
                        "i'm gonna just eat that right up ty",
                        "god damn that's tasty",
                        "i'm munching and crunching like a bunch of crunch n munch",
                        "scarfing it down really fast like a monster would"
                    ]))
                elif chance(50): # underwhelmed response
                    await message.channel.send(pick_string([
                        "yea sure that's okay",
                        "it tastes fine",
                        "thx i guess",
                        "mm yum yeah ok that's alright",
                        "it's " + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "a bowl of seeds"),
                        "it's alright for me",
                        "sure i could have that",
                        "monch monch ehhhh its a little dry",
                        "a little underseasoned to my taste. i mean ill still eat it though",
                        "sorry i dont really like it it's fine though"
                    ]))
                else: # overwhelmed response
                    await message.channel.send(pick_string([
                        "HOLY FUCK iT'S GOOD",
                        "TAHTS SO FUCKING GOOD",
                        "I LOVE IT I LOVE IT I LOVE IT I LOVE IT OMHOMHMHMHMMOMHMGOGMGMMGOHMOHMMGGHOHMMOHMOMGOHMOHMOM",
                        "it\'s REALLY GOOD and GOOD and GREAT and I LIKE IT",
                        "I'VE NEVER HAD SOMETHING SO GOOD",
                        "I LIKE IT A LOT AND ITS VERY GOOD",
                        "MANNA FROM HEAVEN. AMBROSIA. MILK OF THE GGODS",
                        "PLEASE FEED ME ONLY THIS FROM NOW ON IT IS SO GOOD",
                        "this " + (message.content[message.content.index(' ')+1:] if len(message.content) > 6 else "little bowl of seeds") + " making me go freaky mode hdnghmhnioinnf dewnauiontg kjgm f gng ng n wdaiodnagd skjghnjksnfnfnjgnsfesmfkesm\ndnwoianf ka rfaijji fwanijoufnijeanjih fd iongiorfdmngiordiomgfd gjk\n\ndwiaonftgoiaweniodwajfeionfgeoiuiongrsno  fes oifenisnofnnhhnnhn hnnhhhnh \n\n\njdiwoaon fg8omiesajnuigko noiegnio ungio geigejiinoghrdsnioh f sifjnbiuoasndGOGOD THATS GOOD\nndiuowa nioasftenoi ne ioA NTOI JITY JOI JTIOE ONIAnsfangtnjoda\nNDAWUIONFOIAW MJIDFOwmnjasdf sagtjgNGNSJURE OIBGFUIOES NBOFNUIJES NIOFE NOIS fngoie n"
                    ]))
        # elif (message.content == "!unfeed" and (permissions.allowed(message.author.id, "blue") or (permissions.allowed(message.author.id, "red")))):
        #     if (t > dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=6)):
        #         t = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=6)
        #         food.save(t)
        #     await message.channel.send(pick_string([
        #         "What's your problem?",
        #         "fuck is your issue?",
        #         "uncool, man",
        #         "totally NOT chill. not chill",
        #         "bruh",
        #         "bruh moment",
        #         "omg i was gonna eat that wtf"
        #     ]))
        
        # update status on message receive
        if (t > dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=6)):
            # full
            await self.change_presence(status=None, activity=discord.Game(name='Full for now'))
        elif (t < dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=5)):
            await self.change_presence(status=discord.Status.dnd, activity=discord.Game(name='Trashbot has died.'))
            switch.poweroff()
        elif (t < dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=2)):
            await self.change_presence(status=discord.Status.idle, activity=discord.Game(name='Starving for ' + humanize.naturaldelta((dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=6)) - t)))
        else:
            await self.change_presence(status=None, activity=discord.Game(name='Hungry for ' + humanize.naturaldelta((dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=6)) - t)))
    
    def save(t):
        db.put_item(TableName="trashbot", Item={'name':{'S':'hunger'}, 'data':{'S':str(t.timestamp())}})
