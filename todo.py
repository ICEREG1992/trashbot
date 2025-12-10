import os
import json
import discord
import helperfunctions
from helperfunctions import pick_string
from permissions import permissions
import random
import boto3

db = boto3.client('dynamodb', region_name='us-east-2')

global todos
todos = {}

class todo:

    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'todo'}})
        global todos
        todos = json.loads(d['Item']['data']['S'])

    async def run(self, message):
        uid = str(message.author.id)
        dm = message.channel.type is discord.ChannelType.private

        if message.content.startswith("!todo "):
            t = message.content[6:]
            if uid not in todos:
                todos[uid] = []
            todos[uid].append(t)

            await message.channel.send(pick_string([
                "added to todo list. get to work bud",
                "ok thats on the list now",
                "yeah good idea probably. added to the list",
                "sounds good, hope it doesnt take too long",
                "i'll write that down for ya"
            ]))

            todo.save()
            return

        if message.content.startswith("!todoclear "):
            if not dm and not permissions.allowed_channel(message.channel.id):
                await message.add_reaction("❌")
                return

            if uid not in todos or len(todos[uid]) == 0:
                return

            arg = message.content[11:]

            if "," in arg:
                idxs = arg.split(',')
                idxs.sort(reverse=True, key=int)
                for n in idxs:
                    todos[uid].pop(int(n) - 1)
            else:
                todos[uid].pop(int(arg) - 1)

            await message.channel.send(pick_string([
                "removed from todo list. good job man im proud of ya",
                "scratch that one off, eh? nice",
                "u killin it bro nice one",
                "hell yeah. i feel better already",
                "its lit like bic!!! turn up bro thats hella good",
                "good work my main man! u doin it"
            ]))

            todo.save()
            return

        if message.content == "!todo":
            if not dm and not permissions.allowed_channel(message.channel.id):
                await message.add_reaction("❌")
                return

            if uid not in todos:
                todos[uid] = []

            items = todos[uid]

            await message.channel.send(pick_string([
                "ok here's what needs to be done",
                "here's the list bro, knock some of em out for me",
                "i have a list! i have a list... a list of all the bugs you've missed!",
                "todo.. todo.. todo todo todo todo todoooooooooo",
                "yo check dis out",
                "i got a big brain wit " + str(len(items)) + " things inside it",
                "i am trashbot, hear my plea:",
                "daaaaaaaamn bro that's a lot lollllll hop to it"
            ]))

            if len(items) == 0:
                await message.channel.send("uuuhhhhh.... nothing! nice, man. get some sleep.")
                return

            s = ""
            for i, entry in enumerate(items):
                s += f"{i+1}. {entry}\n"
            await message.channel.send(s)

    def save():
        db.put_item(
            TableName="trashbot",
            Item={'name': {'S': 'todo'}, 'data': {'S': json.dumps(todos)}}
        )
