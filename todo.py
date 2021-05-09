import os
import json
import helperfunctions
from helperfunctions import pick_string
from permissions import permissions
import random

f = open("todo.json", "r")
todo_list = json.loads(f.read())
f.close()

class todo:

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
        with open("todo.json", "w") as outfile:
            json.dump(todo_list, outfile, indent=2)
