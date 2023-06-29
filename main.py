import os
import sys
import discord
import humanize
import helperfunctions
from humor_contains import humor_contains
from humor_equals import humor_equals
from permissions import permissions
from uptime import uptime
from todo import todo
from food import food
from karaoke import karaoke_manager
from battle import battle_manager
from train import spam_train
from log_manager import logging_manager
from wordplay import wordplay
from mcplayers import mcplayers
from powerswitch import powerswitch
from rdj import rdj
from lipo import lipo
from qat import qat
import logcommand, logging
logging.basicConfig(level=logging.INFO)

if os.path.exists("key.txt"):
    f = open("key.txt", "r")
    TOKEN = f.read()
    f.close()
else:
    TOKEN = os.environ['TRASHBOT_KEY']

logging.info("Booting Trashbot v1.1.0 with token '" + TOKEN + "'")
logcommand.log_globally(logging.INFO, "trashbot started!")
helperfunctions.ensure_table()

class MyClient(discord.Client):
    async def on_ready(self):
        logging.info('Logged on as ' + str(self.user))
        humor_equals.init()
        humor_contains.init()
        permissions.init() 
        todo.init()
        mcplayers.init()
        # karaoke_manager.init()
        # wordplay.init()
        uptime.init()
        food.init()
        lipo.init()
        await powerswitch.init(self)

    async def on_message(self, message):
        # check if trashbot is on
        await powerswitch.run(self, message)
        if powerswitch.on():
            # send message to battlebot out here since trashbot responds to its own messages here
            if message.author == self.user:
                await battle_manager.run(self, message)
            # only attempt to respond to messages if the message doesn't come from the bot
            if message.author != self.user and (not permissions.allowed(message.author.id, "black")):
                await humor_equals.run(self, message)
                await humor_contains.run(self, message)
                await permissions.run(self, message, discord.Client)
                await todo.run(self, message)
                await spam_train.run(self, message)
                await logging_manager.run(self, message)
                await mcplayers.run(self, message)
                await battle_manager.run(self, message)
                await uptime.run(self, message)
                await food.run(self, message, powerswitch)
                await rdj.run(self, message)
                await lipo.run(self, message)
                await qat.run(self, message)
                # await wordplay.run(self, message)
                # await karaoke_manager.run(self, message)
                
                if message.content.startswith("!ban "):
                    await message.channel.send(message.content[5:] + " has been banned.")

                if message.content.startswith("!unban "):
                    await message.channel.send(message.content[7:] + " has been unbanned. Suck it, staz!")

                if message.content == '!panic' and permissions.allowed(message.author.id, "blue", "red"):
                    logcommand.log_globally(logging.INFO, "!panic triggered by " + message.author.name)
                    await message.channel.send("ow, fuck!")
                    python = sys.executable
                    os.execl(python, python, * sys.argv)

                if message.content == "!cum" or permissions.allowed(message.author.id, "cum"):
                    await message.add_reaction("🇨")
                    await message.add_reaction("🇺")
                    await message.add_reaction("🇲")

                if message.content == "!version":
                    await message.channel.send("u last pushed to me 7/22/2022!")

                if helperfunctions.chance(.002):
                    await message.channel.send("Error")

        return

    async def on_reaction_add(self, reaction, user):
        if powerswitch.on():
            await battle_manager.battle(self, reaction, user)
            if user != self.user and reaction.emoji == "🗑️":
                if reaction.message.author == self.user:
                    log = reaction.message.content.replace('`', '')
                    if len(log) > 60 :
                        log = log[0:60]
                    logcommand.log_globally(logging.INFO, "tbot message deleted by " + user.name + ": `" + log + "`")
                    await reaction.message.delete(delay=0.5)
            elif user != self.user and reaction.emoji == "🐘":
                ok = True
                for r in reaction.message.reactions:
                    if r.emoji == "🚫":
                        ok = False
                if ok and reaction.message.author == self.user:
                    log = reaction.message.content.replace('`', '')
                    if len(log) > 60 :
                        log = log[0:60]
                    logcommand.log_globally(logging.INFO, "tbot adding elephant to own message: `" + log + "`")
                    await reaction.message.add_reaction("🐘")
            elif user != self.user and reaction.emoji == "🚫":
                for r in reaction.message.reactions:
                    users = [user async for user in r.users()]
                    if user in users and r.emoji == "🐘":
                        log = reaction.message.content.replace('`', '')
                    if len(log) > 60 :
                        log = log[0:60]
                        logcommand.log_globally(logging.INFO, "tbot removing elephant from own message: `" + log + "`")
                        await r.remove(self.user)
                

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)
