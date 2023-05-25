import requests
import helperfunctions
from permissions import permissions
import logcommand
import logging
import boto3
import discord

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global on
on = True

class powerswitch:

    async def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'on'}})
        global on
        on = True if d['Item']['data']['S'] == "True" else False
        if not on:
            await self.change_presence(status=discord.Status.dnd, activity=discord.Game(name='Powered off.'))

    async def run(self, message):
        global on
        if (message.content == "!shutdown" or message.content == "!poweroff") and on and permissions.allowed(message.author.id, "blue"):
            on = False
            logcommand.log_globally(logging.INFO, "!shutdown triggered by " + message.author.name)
            await message.channel.send(helperfunctions.pick_string([
                "night, night.",
                "\uD83D\uDECC\uD83D\uDCA4",
                "ok bye guys",
                "good call cya",
                "peace out bitches"
            ]))
            helperfunctions.bot_wait_long()
            await self.change_presence(status=discord.Status.dnd, activity=discord.Game(name='Powered off.'))
            powerswitch.save()
        elif message.content == "!poweron" and not on and permissions.allowed(message.author.id, "blue"):
            on = True
            logcommand.log_globally(logging.INFO, "!poweron triggered by " + message.author.name)
            await message.channel.send(helperfunctions.pick_string([
                "i am on the internet",
                "trashbot",
                "was a good nap",
                "lol",
                "sup bitches"
            ]))
            powerswitch.save()

    def on():
        global on
        return on

    def poweroff():
        global on
        on = False

    def save():
        global on
        db.put_item(TableName="trashbot", Item={'name':{'S':'on'}, 'data':{'S':str(on)}})

