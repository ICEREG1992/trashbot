import helperfunctions

channels = {}

class spam_train:

    async def run(self, message):
        if message.channel.id in channels:
            # get queue
            q = channels[message.channel.id]
            # add to queue/dequeue
            if len(q) == 3:
                q.pop(0)
                q.append(message.content)
                # check if all three the same
                if (q[0] == q[1] and q[1] == q[2]):
                    helperfunctions.bot_wait_long()
                    await message.channel.send(message.content)
            else:
                q.append(message.content)
        else:
            # add channel to channels
            channels[message.channel.id] = []
            channels[message.channel.id].append(message.content)
