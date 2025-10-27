import json
import random
import helperfunctions
import logcommand, logging
import datetime as dt
import boto3

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global reminders
reminders = []

multipliers = {
    's': 1/60,
    'm': 1,
    'h': 60,
    'd': 1440,
    'w': 10080,
    'M': 43200,
    'y': 525600
}

class remind:
    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'reminders'}})
        global reminders
        if ('data' in d['Item']):
            reminders = json.loads(d['Item']['data']['S'])

    async def run(self, message):
        if message.content.startswith("!remindme "):
            parts = message.content.split(' ', 2)
            if len(parts) < 3:
                await message.channel.send("try telling me a time and a message")
                return
            try:
                t = parts[1]
                if t[-1] in multipliers:
                    duration = float(t[:-1]) * multipliers[t[-1]]
                else:
                    await message.channel.send(f"{t} what")
                    return
            except ValueError:
                await message.channel.send(f"that doesnt look like a number")
                return
            reminder_msg = ' '.join(parts[2:])
            if duration < 30:
                await helperfunctions.bot_wait(duration * 60)
                await message.channel.send(helperfunctions.pick_string([
                        f"{message.author.mention} make sure you remember to `{reminder_msg}`",
                        f"hey {message.author.mention} you gotta `{reminder_msg}`",
                        f"{message.author.mention} don't forget `{reminder_msg}`",
                        f"{message.author.mention} it's been {duration} {"minute" if duration == 1 else "minutes"}, `{reminder_msg}`",
                    ]))
                logcommand.log_globally(logging.INFO, f"Sent reminder to {message.author.name}: {reminder_msg}")
            else:
                timestamp = dt.datetime.now(dt.timezone.utc).timestamp()
                reminders.append((message.author.id, message.channel.id, reminder_msg, duration, timestamp))
                remind.save(reminders)
                await message.reply(helperfunctions.pick_string([
                        "heard, chef",
                        "gotcha",
                        "i'll remind you",
                        "you betcha",
                        "dont worry about it",
                        "tick tock on the clock"
                    ]))
                logcommand.log_globally(logging.INFO, f"set reminder for {message.author.name} in {t}: {reminder_msg}")
        
        # if message is reply and is !cancel
        elif message.content.startswith("!cancel") and message.reference is not None:
            try:
                ref_message = await message.channel.fetch_message(message.reference.message_id)
            except:
                await message.channel.send("weird i cant find that message")
                return
            to_remove = []
            for i, (user_id, channel_id, reminder_msg, duration, timestamp) in enumerate(reminders):
                if user_id == ref_message.author.id and channel_id == ref_message.channel.id and reminder_msg in ref_message.content:
                    to_remove.append(i)
            if to_remove:
                for i in reversed(to_remove):
                    reminders.pop(i)
                remind.save(reminders)
                await message.channel.send("cancelled that reminder for you")
                logcommand.log_globally(logging.INFO, f"cancelled reminder for {ref_message.author.name}: {reminder_msg}")

        # Check for due reminders
        to_remove = []
        for i, (user_id, channel_id, reminder_msg, duration, timestamp) in enumerate(reminders):
            if dt.datetime.now(dt.timezone.utc).timestamp() >= timestamp + duration * 60:
                user = await self.fetch_user(user_id)
                channel = await self.fetch_channel(channel_id)
                if user:
                    await channel.send(helperfunctions.pick_string([
                            f"{user.mention} make sure you remember to `{reminder_msg}`",
                            f"hey {user.mention} you gotta `{reminder_msg}`",
                            f"{user.mention} don't forget `{reminder_msg}`",
                            f"{user.mention} it's been {duration}, `{reminder_msg}`",
                        ]))
                    logcommand.log_globally(logging.INFO, f"Sent reminder to {user.name}: {reminder_msg}")
                    to_remove.append(i)
                else:
                    print("no user")
        
        # Remove sent reminders
        if to_remove:
            for i in reversed(to_remove):
                reminders.pop(i)
            remind.save(reminders)
    
    def save(reminders):
        db.put_item(TableName="trashbot", Item={'name':{'S':'reminders'}, 'data':{'S':json.dumps(reminders)}})