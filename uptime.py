import os
import datetime as dt
import humanize
import helperfunctions
from helperfunctions import pick_string
import boto3

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global record_uptime
record_uptime = dt.timedelta(seconds= 0)

start_time = dt.datetime.now()

class uptime:

    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'uptime'}})
        global record_uptime
        if ('data' in d['Item']):
            record_uptime = dt.timedelta(seconds=float(d['Item']['data']['S']))

    async def run(self, message):
        global record_uptime
        if message.content == "!uptime":
            t = dt.datetime.now() - start_time
            
            s = humanize.precisedelta(t)
            await message.channel.send(pick_string([
                "Trashbot has been up for " + s + ". wow!",
                "ya boi's been going for " + s + " aye!",
                "choo choo! this train's been goin for like " + s + " or smth!",
                "uh probably like " + s + " or something idk",
                "thanks for asking! i've been up for " + s + "."
            ]))

            if t > record_uptime:
                record_uptime = t
                uptime.save(record_uptime)
                await message.channel.send(pick_string([
                    "hey, that's a new record!",
                    "whoa, i've never been up that long before!",
                    "ding ding! thas a record!"
                ]))

        if message.content == "!recorduptime":
            s = humanize.precisedelta(dt.datetime(record_uptime))
            message.channel.send(pick_string([
                "the longest i've been up is " + s + "!",
                "my current record for staying awake is " + s + "!",
                "my longest uptime is " + s + ", but i bet i could do better!"
            ]))
                    
    
    def save(t):
        db.put_item(TableName="trashbot", Item={'name':{'S':'uptime'}, 'data':{'S':str(t.total_seconds())}})