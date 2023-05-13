import random
import helperfunctions
import logcommand, logging

channels = {}

class spam_train:

    async def run(self, message):
        if message.channel.id in channels:
            # get queue
            q = channels[message.channel.id]
            # have queue process the new message
            q.proc(message)
            # if three similar messages have been sent and they pass the varied check
            if q.count >= q.lim and q.varied:
                # if it's the first time (not set active yet) reply all the time, else reply 10% of the time
                if not q.active or (q.active and helperfunctions.chance(10)):
                    logcommand.log_globally(logging.INFO, "Train triggered: `" + q.mem.content + "`")
                    helperfunctions.bot_wait()
                    await message.channel.send(message.content)
        else:
            # add channel to channels
            channels[message.channel.id] = Feed(mem = message)

class Feed:
    def __init__(self, mem=None, active=False):
        self.mem = mem
        self.active = active
        self.varied = False
        self.count = 0
        self.lim = random.choice([2, 3])

    def proc(self, msg):
        if self.mem.content.lower() == msg.content.lower():
            self.count += 1
            if self.count > self.lim: # strictly greater as we don't want this happening on first trigger
                self.active = True
            if self.mem.author != msg.author:
                self.varied = True
            # for the edge case that a person spams a message
            # we want the message which satasfies the "varied" rec to also spur the tbot train
            if self.count == self.lim and self.varied == False:
                self.count = self.lim - 1
        else:
            self.count = 0
            self.active = False
            self.varied = False
            self.lim = random.choice([2, 3])
        self.mem = msg