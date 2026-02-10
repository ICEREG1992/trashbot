import boto3
import datetime as dt
import logcommand, logging
import json

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global t
t = dt.datetime.now(dt.timezone.utc)

class boots:
    
    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'boots'}})
        global t
        if ('data' in d['Item']):
            data = json.loads(d['Item']['data']['S'])
            if data == "0":
                t = dt.datetime.now(dt.timezone.utc)
                boots.save()
            else:
                t = dt.datetime.fromtimestamp(float(data), tz=dt.timezone.utc)

    async def run(self, message):
        global t
        if (message.content.startswith("!swampyboots")):
            new_t = dt.datetime.now(dt.timezone.utc)
            await message.channel.send("Days since last swampy boots: ~~" + str((new_t.date() - t.date()).days) + "~~ 0")
            t = new_t
            boots.save()

    def save():
        global t
        db.put_item(TableName="trashbot", Item={'name':{'S':'boots'}, 'data':{'S':json.dumps(t.timestamp())}})