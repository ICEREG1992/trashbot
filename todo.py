import os
import json
import helperfunctions
from helperfunctions import pick_string
from permissions import permissions
import random
import boto3

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global todo_list
todo_list = []

class todo:

    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'todo'}})
        global todo_list
        todo_list = json.loads(d['Item']['data']['S'])

    async def run(self, message):
        if (message.content.startswith("!todo ") and permissions.allowed(message.author.id, "blue", "red")):
            t = message.content[6:]
            todo_list.append(t)
            await message.channel.send("added to todo list. get to work bud")
            todo.save()
        elif (message.content.startswith("!todoclear ") and permissions.allowed(message.author.id, "blue")):
            i = int(message.content[11:])-1
            await message.channel.send("removed from todo list. good job man im proud of ya")
            todo_list.remove(todo_list[i])
            todo.save()
        elif (message.content == "!todo"):
            await message.channel.send("ok here's what needs to be done")
            s = ""
            if len(todo_list) == 0:
                s = "uuuhhhhh.... nothing! nice, man. get some sleep."
            for t in range(len(todo_list)):
                s += "**" + str(t+1) + "**: " + todo_list[t] + "\n"
            await message.channel.send(s)
        
    def save():
        db.put_item(TableName="trashbot", Item={'name':{'S':'todo'}, 'data':{'S':json.dumps(todo_list)}})
