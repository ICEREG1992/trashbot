import os
import json
import helperfunctions
from helperfunctions import pick_string
from permissions import permissions
import random

f = open("contains_phrases.json", "r")
keyphrases = json.loads(f.read())
f.close()

class humor_contains:

    async def run(self, message):
        if (message.content.startswith("!containsadd ") and permissions.allowed(message.author.id, "blue")):
            keyword = message.content[13 : message.content.index("§")-1]
            response = message.content[message.content.index("§")+2:]
            if keyword not in keyphrases:
                keyphrases[keyword] = []
            keyphrases[keyword].append(response)
            humor_contains.save()
        elif (message.content.startswith("!containsremove ") and permissions.allowed(message.author.id, "blue")):
            if "§" in message.content:
                await message.channel.send("hold up there buddy, only a keyword can be deleted with this command")
                return
            else:
                keyword = message.content[16:]
                keyphrases.pop(keyword, None)
                if len(keyphrases[keyword]) == 0:
                    keyphrases.pop(keyword, None)
                humor_contains.save()
        else:
            for phrase in keyphrases:
                if phrase in message.content:
                    await message.channel.send(pick_string(keyphrases[phrase]))

            if "black" in message.content:
                if helperfunctions.chance(10):
                    await message.channel.send("why you gotta make it a race thing")
        
    def save():
        with open("contains_phrases.json", "w") as outfile:
            json.dump(keyphrases, outfile, indent=2)
