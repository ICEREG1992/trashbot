import os
import json
import helperfunctions
from helperfunctions import pick_string, humor_escape
from permissions import permissions
import random
import boto3
import logcommand, logging

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
            keyword = message.content[11 : message.content.index("•")-1].lower()
            response = message.content[message.content.index("•")+2:]
            if len(keyword) < 1 or len(response) < 1:
                await message.channel.send("something doesn't look right...")
                return
            if keyword not in keyphrases:
                keyphrases[keyword] = []
            keyphrases[keyword].append(response)
            logcommand.log_globally(logging.INFO, "New humor_equals response added by " + message.author.name + ", ``" + keyword + " : " + response + "``")
            humor_equals.save()
        elif (message.content.startswith("!equalsremove ") and permissions.allowed(message.author.id, "blue")):
            if "•" in message.content:
                await message.channel.send("hold up there buddy, only a keyword can be deleted with this command")
                return
            else:
                keyword = message.content[14:]
                if keyword in keyphrases:
                    keyphrases.pop(keyword, None)
                    logcommand.log_globally(logging.INFO, "humor_contains keyword deleted by " + message.author.name + ", ``" + keyword + "``")
                    humor_equals.save()
                else:
                    await message.channel.send("that one doesnt seem to exist")
        else:
            for phrase in keyphrases:
                if phrase.lower() == message.content.lower():
                    await message.channel.send(humor_escape(message, pick_string(keyphrases[phrase])))
        
    def save():
        db.put_item(TableName="trashbot", Item={'name':{'S':'equals_phrases'}, 'data':{'S':json.dumps(keyphrases)}})
