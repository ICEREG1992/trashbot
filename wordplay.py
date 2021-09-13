import json
import helperfunctions
from helperfunctions import pick_string
from permissions import permissions
import boto3
import logcommand, logging
import re

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global keyphrases
keyphrases = {}

class wordplay:

    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'wordplay_keywords'}})
        global keyphrases
        keyphrases = json.loads(d['Item']['data']['S'])

    async def run(self, message):
        if (message.content.startswith("!wordplayadd ") and permissions.allowed(message.author.id, "blue")):
            keyword = message.content[13 : message.content.index("§")-1]
            response = message.content[message.content.index("§")+2:]
            if keyword not in keyphrases:
                keyphrases[keyword] = [response]
                # keyphrases[keyword].append(keyword)
            else:
                await message.channel.send("yea u already have a wordplay for that keyword lol cut it out")
            logcommand.log_globally(logging.INFO, "New wordplay keyword added by " + message.author.name + ", ``" + keyword + "``, response ``" + response + "``")
            wordplay.save()
        elif (message.content.startswith("!wordplayremove ") and permissions.allowed(message.author.id, "blue")):
            if "§" in message.content:
                await message.channel.send("hold up there buddy, only a keyword can be deleted with this command")
                return
            else:
                keyword = message.content[16:]
                if keyword in keyphrases:
                    keyphrases.pop(keyword, None)
                    logcommand.log_globally(logging.INFO, "wordplay keyword deleted by " + message.author.name + ", ``" + keyword + "``")
                    wordplay.save()
                else:
                    await message.channel.send("that one doesnt seem to exist")
        else:
            for phrase in keyphrases:
                if phrase.lower() in message.content.lower():
                    # spotted! now find the word that we found the keyword in
                    # extract all of the character words found in the string
                    words = re.split('\W+', message.content.lower())
                    # filter down to just the words containing the keyword
                    matches = [a for a in words if phrase in a]
                    for match in matches:
                        if match not in keyphrases[phrase][1:] and match != phrase:
                            keyphrases[phrase].append(match)
                            wordplay.save()
                            await message.channel.send(keyphrases[phrase][0])
                        elif match == phrase:
                            await message.channel.send(keyphrases[phrase][0])
                    

    def save():
        # we have to do shenanigans here to be able to serialize our dict with tuple keys
        db.put_item(TableName="trashbot", Item={'name':{'S':'wordplay_keywords'}, 'data':{'S':json.dumps(keyphrases)}})
        