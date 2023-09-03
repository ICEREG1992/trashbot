import json
import helperfunctions
from helperfunctions import pick_string, humor_escape
from permissions import permissions
import boto3
import logcommand, logging
import re
import string

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global keyphrases
keyphrases = {}

class humor_regex:

    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'regex_phrases'}})
        global keyphrases
        keyphrases = json.loads(d['Item']['data']['S'])

    async def run(self, message):
        if (message.content.startswith("!regexadd ") and permissions.allowed(message.author.id, "blue")):
            keyword = message.content[10 : message.content.index("•")-1]
            response = message.content[message.content.index("•")+2:]
            if len(keyword) < 1 or len(response) < 1:
                await message.channel.send("something doesn't look right...")
                return
            try:
                re.compile(keyword)
            except re.error:
                await message.channel.send("that doesn't look like valid regex...")
                return
            if keyword not in keyphrases:
                keyphrases[keyword] = []
            keyphrases[keyword].append(response)
            logcommand.log_globally(logging.INFO, "New humor_regex response added by " + message.author.name + ", ``" + keyword + " : " + response + "``")
            humor_regex.save()
        elif (message.content.startswith("!regexremove ") and permissions.allowed(message.author.id, "blue")):
            if "•" in message.content:
                await message.channel.send("hold up there buddy, only a keyword can be deleted with this command")
                return
            else:
                keyword = message.content[13:]
                if keyword in keyphrases:
                    keyphrases.pop(keyword, None)
                    logcommand.log_globally(logging.INFO, "humor_regex keyword deleted by " + message.author.name + ", ``" + keyword + "``")
                    humor_regex.save()
                else:
                    await message.channel.send("that one doesnt seem to exist")
        else:
            for phrase in keyphrases:
                o = re.match(phrase, message.content)
                if o:
                    await message.channel.send(humor_escape(message, pick_string(keyphrases[phrase]), o))

    def save():
        db.put_item(TableName="trashbot", Item={'name':{'S':'regex_phrases'}, 'data':{'S':json.dumps(keyphrases)}})
