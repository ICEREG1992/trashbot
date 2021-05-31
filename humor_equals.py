import os
import json
import helperfunctions
from helperfunctions import pick_string
from permissions import permissions
import random
import boto3

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global keyphrases
keyphrases = {}

class humor_equals:

    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'equals_phrases'}})
        global keyphrases
        keyphrases = json.loads(d['Item']['data']['S'])

    async def run(self, message):
        if (message.content.startswith("!equalsadd ") and permissions.allowed(message.author.id, "blue")):
            keyword = message.content[11 : message.content.index("§")-1].lower()
            response = message.content[message.content.index("§")+2:]
            if keyword not in keyphrases:
                keyphrases[keyword] = []
            keyphrases[keyword].append(response)
            humor_equals.save()
        elif (message.content.startswith("!equalsremove ") and permissions.allowed(message.author.id, "blue")):
            if "§" in message.content:
                await message.channel.send("hold up there buddy, only a keyword can be deleted with this command")
                return
            else:
                keyword = message.content[14:]
                keyphrases.pop(keyword, None)
                if len(keyphrases[keyword]) == 0:
                    keyphrases.pop(keyword, None)
                humor_equals.save()
        else:
            for phrase in keyphrases:
                if phrase == message.content.lower():
                    await message.channel.send(pick_string(keyphrases[phrase]))
        
    def save():
        db.put_item(TableName="trashbot", Item={'name':{'S':'equals_phrases'}, 'data':{'S':json.dumps(keyphrases)}})
