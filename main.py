import os
import sys
import logging
import discord
import humanize
import datetime as dt
import helperfunctions
from humor_contains import humor_contains
from humor_equals import humor_equals
from permissions import permissions
from uptime import uptime
from todo import todo
from karaoke import karaoke_manager
from battle import battle_manager
from train import spam_train
import logcommand
logging.basicConfig(level=logging.INFO)

if os.path.exists("key.txt"):
    f = open("key.txt", "r")
    TOKEN = f.read()
    f.close()
else:
    TOKEN = os.environ['TRASHBOT_KEY']

logging.info("Booting Trashbot v1.0.0 with token '" + TOKEN + "'")
logcommand.log_globally(logging.INFO, "Trashbot dyno spun up!")
helperfunctions.ensure_table()

class MyClient(discord.Client):
    async def on_ready(self):
        logging.info('Logged on as ' + str(self.user))
        humor_equals.init()
        humor_contains.init()
        permissions.init() 
        uptime.init() 
        todo.init() 
        karaoke_manager.init()

    async def on_message(self, message):
        # send message to battlebot out here since trashbot responds to its own messages here
        if message.author == self.user:
            await battle_manager.run(self, message)
        # only attempt to respond to messages if the message doesn't come from the bot
        if message.author != self.user and (not permissions.allowed(message.author.id, "black")):
            await humor_equals.run(self, message)
            await humor_contains.run(self, message)
            await permissions.run(self, message, discord.Client)
            await uptime.run(self, message)
            await todo.run(self, message)
            await karaoke_manager.run(self, message)
            await spam_train.run(self, message)
            await logcommand.logging_manager.run(self, message)
            #await battle_manager.run(self, message)

            if message.content.startswith("!ban "):
                await message.channel.send(message.content[5:] + " has been banned.")

            if message.content.startswith("!unban "):
                await message.channel.send(message.content[7:] + " has been unbanned. Suck it, staz!")

            if message.content == '!panic' and permissions.allowed(message.author.id, "blue", "red"):
                logcommand.log_globally(logging.INFO, "!panic triggered by " + message.author.name)
                await message.channel.send("ow, fuck!")
                python = sys.executable
                os.execl(python, python, * sys.argv)

            if message.content == '!shutdown' and permissions.allowed(message.author.id, "blue"):
                logcommand.log_globally(logging.INFO, "!shutdown triggered by " + message.author.name)
                await message.channel.send(helperfunctions.pick_string([
                    "night, night.",
                    "\uD83D\uDECC\uD83D\uDCA4",
                    "ok bye guys",
                    "good call cya",
                    "peace out bitches"
                ]))
                quit()

            if message.content == "!cum":
                await message.add_reaction("🇨")
                await message.add_reaction("🇺")
                await message.add_reaction("🇲")

            return

    async def on_reaction_add(self, reaction, user):
        await battle_manager.battle(self, reaction, user)
        if user != self.user and reaction.emoji == "🗑️":
            if reaction.message.author == self.user:
                logcommand.log_globally(logging.INFO, "tbot message deleted: ``" + reaction.message.content + "``")
                await reaction.message.delete(delay=0.5)

    # message_edit joke
    '''async def on_message_edit(self, before, after):
        if after.author != self.user and before.content != after.content and helperfunctions.chance(10):
            await after.channel.send(helperfunctions.pick_string([
                "LOL u made a lil fucky wucky there huh??",
                "LMFAO ok let's all just pretend we didn't see that typo",
                "press enter too soon buddy? lol lmfao",
                "EVERYBODY LOOK THIS PERSON MADE A MISTAKE!!!",
                "it's ok bro everyone makes mistakes just edit until it's good"
            ]))'''

client = MyClient()
client.run(TOKEN)
