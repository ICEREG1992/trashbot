import helperfunctions
import logcommand, logging

channels = {}

class spam_train:

    async def run(self, message):
        if message.channel.id in channels:
            # get queue
            q = channels[message.channel.id]
            # add to queue and/or dequeue
            q.append(message.content)
            if len(q) == 3:
                # check if all three the same
                if (q[0].lower() == q[1].lower() and q[1].lower() == q[2].lower()):
                    # reply at third, afterwards smaller chance to add to chain
                    if not q.active or (q.active and helperfunctions.chance(20)):
                        logcommand.log_globally(logging.INFO, "Train triggered: ``" + q[0] + "``")
                        helperfunctions.bot_wait()
                        await message.channel.send(message.content)
                    q.active = True
                else:
                    q.active = False
        else:
            # add channel to channels
            channels[message.channel.id] = Feed()
            channels[message.channel.id].append(message.content)

class Feed:
    def __init__(self, queue=[], active=False):
        self.queue = queue
        self.active = active

    def __getitem__(self, key):
        return self.queue[key]

    def append(self, msg):
        self.queue.append(msg)
        if len(self) > 3:
            self.queue.pop(0)

    def __len__(self):
        return len(self.queue)