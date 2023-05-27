import json
import helperfunctions
from helperfunctions import pick_string, humor_escape
from permissions import permissions
import boto3
import logcommand, logging

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global keyphrases
keyphrases = {}

class humor_contains:

    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'contains_phrases'}})
        global keyphrases
        keyphrases = json.loads(d['Item']['data']['S'])

    async def run(self, message):
        if (message.content.startswith("!containsadd ") and permissions.allowed(message.author.id, "blue")):
            keyword = message.content[13 : message.content.index("•")-1]
            response = message.content[message.content.index("•")+2:]
            if len(keyword) < 1 or len(response) < 1:
                await message.channel.send("something doesn't look right...")
                return
            if keyword not in keyphrases:
                keyphrases[keyword] = []
            keyphrases[keyword].append(response)
            logcommand.log_globally(logging.INFO, "New humor_contains response added by " + message.author.name + ", ``" + keyword + " : " + response + "``")
            humor_contains.save()
        elif (message.content.startswith("!containsremove ") and permissions.allowed(message.author.id, "blue")):
            if "•" in message.content:
                await message.channel.send("hold up there buddy, only a keyword can be deleted with this command")
                return
            else:
                keyword = message.content[16:]
                if keyword in keyphrases:
                    keyphrases.pop(keyword, None)
                    logcommand.log_globally(logging.INFO, "humor_contains keyword deleted by " + message.author.name + ", ``" + keyword + "``")
                    humor_contains.save()
                else:
                    await message.channel.send("that one doesnt seem to exist")
        else:
            for phrase in keyphrases:
                if phrase.lower() in message.content.lower():
                    await message.channel.send(humor_escape(message, pick_string(keyphrases[phrase])))

            '''
            if "black" in message.content:
                if helperfunctions.chance(10):
                    await message.channel.send("why you gotta make it a race thing")
            '''

    def save():
        db.put_item(TableName="trashbot", Item={'name':{'S':'contains_phrases'}, 'data':{'S':json.dumps(keyphrases)}})
