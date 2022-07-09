import requests
import helperfunctions
from permissions import permissions
import os
import boto3

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global mcIP
mcIP = ""

class mcplayers:

    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'mc_ip'}})
        global mcIP
        mcIP = d['Item']['data']['S']

    async def run(self, message):
        if mcIP and message.content == "!whosuprn":
            r = requests.get('https://api.mcsrvstat.us/2/' + mcIP)
            o = r.json()
            if o['online']:
                n = str(o['players']['online'])
                if (n == '0'):
                    await message.channel.send(helperfunctions.pick_string(["nah nobody up rn", "not rn sorry", "nope", "nothing much whos uprn with u", "nah", "negative"]))
                else:
                    out = ""
                    for p in o['players']['list']:
                        out += p + "\n"
                    await message.channel.send(out)
            else:
                await message.channel.send(helperfunctions.pick_string(["uh oh server down", "haha ummmmm i kicked something back here hehe oops uhhh", "whoa whoa whoa waho whoa whao smmmm ummmmmmmmm server??? server??? servv?er??", "WHOOPS UH OH HEHEHE", "server is sorta sus rn ngl"]))
        elif message.content.startswith("!setwhosup ") and permissions.allowed(message.author.id, "blue"):
            i = message.content[11:]
            mcIP = i
            await message.channel.send(pick_string(["ok i'll watch " + mcIP + " for ya",
                "ok sure minecraft ip set to " + mcIP,
                "New IP Set! haha wasnt that goofy"]))
            mcplayers.save()

    def save():
        db.put_item(TableName="trashbot", Item={'name':{'S':'mc_ip'}, 'data':{'S':mcIP}})