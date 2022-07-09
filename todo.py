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
            await message.channel.send(pick_string(["added to todo list. get to work bud",
                "ok thats on the list now",
                "yeah good idea probably. added to the list",
                "sounds good, hope it doesnt take too long",
                "i'll write that down for ya"]))
            todo.save()
        elif (message.content.startswith("!todoclear ") and permissions.allowed(message.author.id, "blue")):
            i = int(message.content[11:])-1
            await message.channel.send(pick_string(["removed from todo list. good job man im proud of ya",
                "scratch that one off, eh? nice",
                "u killin it bro nice one",
                "hell yeah. i feel better already",
                "its lit like bic!!! turn up bro thats hella good",
                "good work my main man! u doin it"]))
            todo_list.remove(todo_list[i])
            todo.save()
        elif (message.content == "!todo"):
            await message.channel.send(pick_string(["ok here's what needs to be done",
                "here's the list bro, knock some of em out for me",
                "i have a list! i have a list... a list of all the bugs you've missed!",
                "todo.. todo.. todo todo todo todo todoooooooooo",
                "yo check dis out",
                "i got a big brain wit " + str(len(todo_list)) + " things inside it",
                "i am trashbot, hear my plea:",
                "daaaaaaaamn bro that's a lot lollllll hop to it"]))
            s = ""
            if len(todo_list) == 0:
                s = "uuuhhhhh.... nothing! nice, man. get some sleep."
            for t in range(len(todo_list)):
                s += "**" + str(t+1) + "**: " + todo_list[t] + "\n"
            await message.channel.send(s)
        
    def save():
        db.put_item(TableName="trashbot", Item={'name':{'S':'todo'}, 'data':{'S':json.dumps(todo_list)}})
