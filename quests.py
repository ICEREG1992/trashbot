import json
import random
import helperfunctions
import logcommand, logging
import datetime as dt
import boto3
from discord import MessageType
from types import SimpleNamespace

from permissions import permissions

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global questsData
questsData = {}

basetags = ["general", "random", "notag", "null", "none"]

class quests:
    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'quests'}})
        global questsData
        if ('data' in d['Item']):
            questsData = json.loads(d['Item']['data']['S'])
            # if no quests, rewards, punishments, and tags keys, create them
            if 'quests' not in questsData:
                questsData['quests'] = []
            if 'rewards' not in questsData:
                questsData['rewards'] = []
            if 'punishments' not in questsData:
                questsData['punishments'] = []
            if 'tags' not in questsData:
                questsData['tags'] = {}
            if 'enabled' not in questsData:
                questsData['enabled'] = True
            if 'messages' not in questsData:
                questsData['messages'] = {}
            if 'players' not in questsData:
                questsData['players'] = {}
            quests.save()
    
    async def run(self, message, bulk = False):
        if questsData["enabled"] == True:
            if message.content.startswith("!quest ") or message.content == "!quest":
                parts = message.content.split(' ')
                if quests.playerQuests(message.author.id) and parts[1] not in questsData["messages"].keys():
                    await message.channel.send(f"watch out! you already have a quest active.")
                if len(parts) > 1:
                    if parts[1] in questsData["tags"].keys():
                        q = questsData["quests"][random.choice(questsData["tags"][parts[1]]["quests"])]
                        i = (await message.channel.send(q)).id
                        quests.addQuestToPlayer(message, i, tag=parts[1])
                    elif parts[1] in basetags:
                        q = random.choice(questsData["quests"])
                        i = (await message.channel.send(q)).id
                        quests.addQuestToPlayer(message, i, tag="random")
                    elif parts[1] in questsData["messages"].keys():
                        await message.channel.send(questsData["messages"][parts[1]])
                    else:
                        await message.channel.send(f"that's not a tag i know")
                else:
                    q = random.choice(questsData["quests"])
                    i = (await message.channel.send(q)).id
                    quests.addQuestToPlayer(message, i, tag="random")
            
            elif message.content.startswith("!quests ") or message.content == "!quests":
                parts = message.content.split(' ')
                if len(parts) > 1:
                    mention = parts[1]
                else:
                    mention = str(message.author.id)
                mention = mention.replace("<@", "").replace("!", "").replace(">", "")
                if mention.isdigit():
                    player_id = int(mention)
                    if str(player_id) in questsData["players"]:
                        if "quests" in questsData["players"][str(player_id)]:
                            if len(questsData["players"][str(player_id)]["quests"]) > 0:
                                out = f"<@{player_id}> has {len(questsData['players'][str(player_id)]['quests'])} quests active"
                                for q in questsData['players'][str(player_id)]['quests']:
                                    guild = q.get("guild")
                                    channel = q.get("channel")
                                    quest = q.get("quest")
                                    tag = q.get("tag", "?")

                                    if not guild or not channel or not quest:
                                        continue

                                    out += f"\n- https://discord.com/channels/{guild}/{channel}/{quest} ({tag})"
                                await message.channel.send(out)
                            else:
                                await message.channel.send(f"<@{player_id}> has no current quests")
                        else:
                            await message.channel.send(f"<@{player_id}> has no current quests")
                    else:
                        await message.channel.send(f"<@{player_id}> has no current quests")
                else:
                    await message.channel.send(f"that's not a valid user") 
            
            elif message.content.startswith("!reward ") or message.content == "!reward":
                if message.type == MessageType.reply:
                    parts = message.content.split(' ')
                    # get message to check it's from bot
                    channel_id = message.reference.channel_id
                    message_id = message.reference.message_id
                    c = await self.fetch_channel(channel_id)
                    m = await c.fetch_message(message_id)
                    if m.author != self.user:
                        await message.channel.send(f"that ain't me foo")
                        return
                    if m.content not in questsData["quests"]:
                        await message.channel.send("thats not a quest, silly!")
                        return
                    if message_id not in [q["quest"] for q in questsData["players"].get(str(message.author.id), {}).get("quests", [])]:
                        await message.channel.send("you can't claim a reward for that quest")
                        return
                    if len(parts) == 1:
                        # no tag specified, just give random reward
                        tag = quests.removeQuestFromPlayer(message.author.id, message_id)
                        if tag in basetags:
                            r = random.choice(questsData["rewards"])
                        else:
                            r = questsData["rewards"][random.choice(questsData["tags"][tag]["rewards"])]
                        quests.addRewardToPlayer(message.author.id, r)
                        await message.channel.send(r)
                    else:
                        tag = parts[1]
                        if tag in questsData["tags"].keys() and len(questsData["tags"][tag]["rewards"]) > 0:
                            quests.removeQuestFromPlayer(message.author.id, message_id)
                            r = questsData["rewards"][random.choice(questsData["tags"][tag]["rewards"])]
                            quests.addRewardToPlayer(message.author.id, r)
                            await message.channel.send(r)
                        elif tag in basetags:
                            r = random.choice(questsData["rewards"])
                        else:
                            await message.channel.send("i dont know about that tag")
                    
            elif message.content.startswith("!award ") or message.content == "!award":
                if message.type == MessageType.reply:
                    parts = message.content.split(' ')
                    if len(parts) > 1:
                        await message.channel.send(f"pick someone to award this quest to")
                    else:
                        # get message to check it's from bot
                        channel_id = message.reference.channel_id
                        message_id = message.reference.message_id
                        c = await self.fetch_channel(channel_id)
                        m = await c.fetch_message(message_id)
                        mention = message.mentions.first()
                        if mention is None:
                            await message.channel.send(f"you need to @mention them")
                            return
                        if m.author != self.user:
                            await message.channel.send(f"that ain't me foo")
                            return
                        if m.content not in questsData["quests"]:
                            await message.channel.send("thats not a quest man")
                            return
                        if message_id not in [q["quest"] for q in questsData["players"].get(str(message.author.id), {}).get("quests", [])]:
                            await message.channel.send("you can't award that quest")
                            return
                        tag = quests.removeQuestFromPlayer(message.author.id, message_id)
                        if tag in basetags:
                            r = random.choice(questsData["rewards"])
                            i = (await message.channel.send(r)).id
                            quests.addRewardToPlayer(mention.id, i, tag="random", reward=r)
                        else:
                            r = random.choice(questsData["rewards"])
                            i = (await message.channel.send(r)).id
                            quests.addRewardToPlayer(mention.id, i, tag=tag, reward=r)
                        await message.channel.send(f"awarded that quest's reward to <@{mention.id}> :)")
            
            elif message.content.startswith("!punishment ") or message.content == "!punishment":
                if message.type == MessageType.reply:
                    parts = message.content.split(' ')
                    if len(parts) > 1:
                        await message.channel.send(f"no tags for punishments")
                    else:
                        # get message to check it's from bot
                        channel_id = message.reference.channel_id
                        message_id = message.reference.message_id
                        c = await self.fetch_channel(channel_id)
                        m = await c.fetch_message(message_id)
                        if m.author != self.user:
                            await message.channel.send(f"that ain't me foo")
                            return
                        if m.content not in questsData["quests"]:
                            await message.channel.send("thats not a quest, silly!")
                            return
                        if message_id not in [q["quest"] for q in questsData["players"].get(str(message.author.id), {}).get("quests", [])]:
                            await message.channel.send("that's not your punishment to bear")
                            return
                        quests.removeQuestFromPlayer(message.author.id, message_id)
                        await message.channel.send(random.choice(questsData["punishments"]))

            elif message.content == "!reroll":
                if message.type == MessageType.reply:
                    # get message to check it's from bot
                    channel_id = message.reference.channel_id
                    message_id = message.reference.message_id
                    c = await self.fetch_channel(channel_id)
                    m = await c.fetch_message(message_id)
                    if m.author != self.user:
                        await message.channel.send(f"that ain't me foo")
                        return
                    if message_id not in [q["quest"] for q in questsData["players"].get(str(message.author.id), {}).get("quests", [])] or message_id not in [r["reward"] for r in questsData["players"].get(str(message.author.id), {}).get("inventory", [])]:
                        await message.channel.send("that's not your quest or reward to reroll")
                        return
                    if m.content in questsData["quests"]:
                        tag = quests.removeQuestFromPlayer(message.author.id, message_id)
                        if tag in basetags:
                            q = random.choice(questsData["quests"])
                            i = (await message.channel.send(q)).id
                            quests.addQuestToPlayer(message, i, tag="random")
                        else:
                            q = questsData["quests"][random.choice(questsData["tags"][tag]["quests"])]
                            i = (await message.channel.send(q)).id
                            quests.addQuestToPlayer(message, i, tag=tag)
                    elif m.content in questsData["rewards"]:
                        tag = quests.removeRewardFromPlayer(message.author.id, message_id)
                        if tag in basetags:
                            r = random.choice(questsData["rewards"])
                            i = (await message.channel.send(r)).id
                            quests.addRewardToPlayer(message, i, tag="random", reward=r)
                        else:
                            r = questsData["rewards"][random.choice(questsData["tags"][tag]["rewards"])]
                            i = (await message.channel.send(r)).id
                            quests.addRewardToPlayer(message, i, tag=tag, reward=r)
                else:
                    await message.channel.send(f"you gotta reply to the quest you want to reroll")

            elif message.content.startswith("!addquest ") and permissions.allowed(message.author.id, "blue"):
                parts = message.content.split(' ')
                if len(parts) >= 3:
                    quest = ' '.join(parts[2:])
                    quest = quest.replace(' // ', '\n')
                    questsData["quests"].append(quest)
                    tag = parts[1]
                    tags = tag.split(',')
                    ind = questsData["quests"].index(quest)
                    for tag in tags:
                        if tag in questsData["tags"].keys():
                            try:
                                questsData["tags"][tag]["quests"].append(ind)
                                quests.save()
                                if not bulk: await message.channel.send(f"added quest to tag {tag}")
                            except ValueError:
                                await message.channel.send("something terrible happened")
                        elif tag in basetags:
                            quests.save()
                        else:
                            questsData["tags"][tag] = {"quests": [ind], "rewards": []}
                            quests.save()
                            if not bulk: await message.channel.send(f"created new tag {tag} and added quest")
                else:
                    await message.channel.send("try giving me a tag and a quest")
                    return

            elif message.content.startswith("!removequest ") and permissions.allowed(message.author.id, "blue"):
                parts = message.content.split(' ')
                if len(parts) > 1:
                    quest = ' '.join(parts[1:])
                    quest = quest.replace(' // ', '\n')
                    if quest in questsData["quests"]:
                        i = questsData["quests"].index(quest)
                        questsData["quests"].remove(quest)
                        for t in questsData["tags"].keys():
                            if i in questsData["tags"][t]["quests"]:
                                questsData["tags"][t]["quests"].remove(i)
                        # if tag has no quests and no rewards, remove it
                        for t in list(questsData["tags"].keys()):
                            if len(questsData["tags"][t]["quests"]) == 0 and len(questsData["tags"][t]["rewards"]) == 0:
                                del questsData["tags"][t]
                        quests.save()
                        if not bulk: await message.channel.send(f"removed quest")
                    else:
                        await message.channel.send(f"that quest over there is NOT real")

            elif message.content.startswith("!addreward ") and permissions.allowed(message.author.id, "blue"):
                parts = message.content.split(' ')
                if len(parts) >= 3:
                    tag = parts[1]
                    reward = ' '.join(parts[2:])
                    reward = reward.replace(' // ', '\n')
                    tags = tag.split(',')
                    ind = len(questsData["rewards"])
                    questsData["rewards"].append(reward)
                    for tag in tags:
                        if tag in questsData["tags"].keys():
                            questsData["tags"][tag]["rewards"].append(ind)
                            quests.save()
                            if not bulk: await message.channel.send(f"added reward to tag {tag}")
                        elif tag in basetags:
                            quests.save()
                        else:
                            questsData["tags"][tag] = {"quests": [], "rewards": [ind]}
                            quests.save()
                            if not bulk: await message.channel.send(f"created new tag {tag} and added reward")
                else:
                    await message.channel.send("try giving me a tag and a reward")
                    return

            elif message.content.startswith("!removereward ") and permissions.allowed(message.author.id, "blue"):
                parts = message.content.split(' ')
                if len(parts) > 1:
                    reward = ' '.join(parts[1:])
                    reward = reward.replace(' // ', '\n')
                    if reward in questsData["rewards"]:
                        i = questsData["rewards"].index(reward)
                        questsData["rewards"].remove(reward)
                        for t in questsData["tags"].keys():
                            if i in questsData["tags"][t]["rewards"]:
                                questsData["tags"][t]["rewards"].remove(i)
                        # if tag has no quests and no rewards, remove it
                        for t in list(questsData["tags"].keys()):
                            if len(questsData["tags"][t]["quests"]) == 0 and len(questsData["tags"][t]["rewards"]) == 0:
                                del questsData["tags"][t]
                        quests.save()
                        if not bulk: await message.channel.send(f"removed reward")
                    else:
                        await message.channel.send(f"that reward over there is NOT real")

            elif message.content.startswith("!addpunishment") and permissions.allowed(message.author.id, "blue"):
                parts = message.content.split(' ')
                if len(parts) >= 2:
                    punishment = ' '.join(parts[1:])
                    punishment = punishment.replace(' // ', '\n')
                    questsData["punishments"].append(punishment)
                    quests.save()
                    if not bulk: await message.channel.send(f"added punishment")
                else:
                    await message.channel.send("add punishment what")
                    return

            elif message.content.startswith("!removepunishment ") and permissions.allowed(message.author.id, "blue"):
                parts = message.content.split(' ')
                if len(parts) > 1:
                    punishment = ' '.join(parts[1:])
                    punishment = punishment.replace(' // ', '\n')
                    if punishment in questsData["punishments"]:
                        questsData["punishments"].remove(punishment)
                        quests.save()
                        if not bulk: await message.channel.send(f"removed punishment")
                    else:
                        await message.channel.send(f"that punishment over there is NOT real")

            elif message.content.startswith("!addmessage ") and permissions.allowed(message.author.id, "blue"):
                parts = message.content.split(' ')
                if len(parts) >= 3:
                    tag = parts[1]
                    msg = ' '.join(parts[2:])
                    msg = msg.replace(' // ', '\n')
                    if tag in questsData["messages"].keys():
                        questsData["messages"][tag] = msg
                        quests.save()
                        if not bulk: await message.channel.send(f"overwrote message for `!quest {tag}`")
                    else:
                        questsData["messages"][tag] = msg
                        quests.save()
                        if not bulk: await message.channel.send(f"added message for `!quest {tag}`")
                elif len(parts) == 2:
                    questsData["messages"][tag] = ""
                    quests.save()
                    if not bulk: await message.channel.send(f"disabled response for `!quest {tag}`")
                else:
                    await message.channel.send("try giving me a tag and a message")
                    return
                
            elif message.content.startswith("!removemessage ") and permissions.allowed(message.author.id, "blue"):
                parts = message.content.split(' ')
                if len(parts) > 1:
                    tag = parts[1]
                    if tag in questsData["messages"].keys():
                        del questsData["messages"][tag]
                        quests.save()
                        if not bulk: await message.channel.send(f"removed message for tag {tag}")
                    else:
                        await message.channel.send(f"that doesn't exist yet")
                else:
                    await message.channel.send("remove message for what tag")
                    return

            elif message.content.startswith("!bulkadd") and permissions.allowed(message.author.id, "blue"):
                if len(message.content) < 9:
                    await message.channel.send("bulk add what")
                    return
                content = message.content[len("!bulkadd "):]
                lines = content.split('\n')
                await message.channel.send(f"adding {len(lines)} quests/rewards/punishments")
                for line in lines:
                    await quests.run(self, SimpleNamespace(content=line, author=message.author, channel=message.channel), bulk=True)
                await message.channel.send("all done")

            elif message.content == "!questlist" and permissions.allowed(message.author.id, "blue"):
                msg = ""
                tags = list(questsData["tags"].keys())
                if len(tags) == 0:
                    msg += ("no quests or rewards yet\n")
                else:
                    for t in tags:
                        msg += f"**{t}**: {len(questsData['tags'][t]['quests'])} quests, {len(questsData['tags'][t]['rewards'])} rewards\n"
                msg += f"{len(questsData['punishments'])} punishments\n"
                await message.channel.send(msg)

            elif message.content == "!clearquests" and permissions.allowed(message.author.id, "blue"):
                questsData['quests'] = []
                for t in questsData["tags"].keys():
                    questsData["tags"][t]["quests"] = []
                # if tag has no quests and no rewards, remove it
                for t in list(questsData["tags"].keys()):
                    if len(questsData["tags"][t]["quests"]) == 0 and len(questsData["tags"][t]["rewards"]) == 0:
                        del questsData["tags"][t]
                quests.save()
                await message.channel.send("cleared all quests")

            elif message.content == "!clearrewards" and permissions.allowed(message.author.id, "blue"):
                questsData['rewards'] = []
                for t in questsData["tags"].keys():
                    questsData["tags"][t]["rewards"] = []
                # if tag has no quests and no rewards, remove it
                for t in list(questsData["tags"].keys()):
                    if len(questsData["tags"][t]["quests"]) == 0 and len(questsData["tags"][t]["rewards"]) == 0:
                        del questsData["tags"][t]
                quests.save()
                await message.channel.send("cleared all rewards")

            elif message.content == "!clearpunishments" and permissions.allowed(message.author.id, "blue"):
                questsData['punishments'] = []
                # if tag has no quests and no rewards, remove it
                for t in list(questsData["tags"].keys()):
                    if len(questsData["tags"][t]["quests"]) == 0 and len(questsData["tags"][t]["rewards"]) == 0:
                        del questsData["tags"][t]
                quests.save()
                await message.channel.send("cleared all punishments")
            
            elif message.content == "!clearmessages" and permissions.allowed(message.author.id, "blue"):
                questsData['messages'] = {}
                quests.save()
                await message.channel.send("cleared all messages")

            elif message.content == "!clearuserrewards" and permissions.allowed(message.author.id, "blue"):
                for p in questsData["players"].keys():
                    if "inventory" in questsData["players"][p]:
                        questsData["players"][p]["inventory"] = []
                quests.save()
                await message.channel.send("cleared all user's rewards")

            elif message.content == "!disablequests" and permissions.allowed(message.author.id, "blue"):
                questsData["enabled"] = False
                quests.save()
                await message.channel.send("no more fun !!!")
        
        if message.content == "!enablequests" and permissions.allowed(message.author.id, "blue"):
            questsData["enabled"] = True
            quests.save()
            await message.channel.send("quests!!!")

    async def getQuestTag(self, message_id, channel_id):
        # use api to get message content
        c = await self.fetch_channel(channel_id)
        m = await c.fetch_message(message_id)
        if m.content in questsData["quests"]:
            i = questsData["quests"].index(m.content)
            if i is not None and m.author == self.user:
                # check tags for that index
                for t in questsData["tags"].keys():
                    if i in questsData["tags"][t]["quests"]:
                        return t
                # this is a base tag quest
                return "random"
        return None
    
    def addQuestToPlayer(message, message_id, tag):
        player_id = message.author.id
        if str(player_id) not in questsData["players"]:
            questsData["players"][str(player_id)] = {"quests": [], "inventory": []}
        if "quests" not in questsData["players"][str(player_id)]:
            questsData["players"][str(player_id)]["quests"] = []
        if message.guild is None:
            guild = "@me"
        else:
            guild = message.guild.id
        questsData["players"][str(player_id)]["quests"].append({"quest": message_id, "channel": message.channel.id, "guild": guild, "tag": tag, "date": str(dt.datetime.now())})
        quests.save()

    def removeQuestFromPlayer(player_id, message_id):
        if str(player_id) in questsData["players"]:
            if "quests" in questsData["players"][str(player_id)]:
                tag = [q["tag"] for q in questsData["players"][str(player_id)]["quests"] if q["quest"] == message_id][0]
                questsData["players"][str(player_id)]["quests"] = [q for q in questsData["players"][str(player_id)]["quests"] if q["quest"] != message_id]
                quests.save()
                return tag
        return "random"

    def addRewardToPlayer(message, message_id, tag, reward):
        player_id = message.author.id
        if str(player_id) not in questsData["players"]:
            questsData["players"][str(player_id)] = {"quests": [], "inventory": []}
        if "inventory" not in questsData["players"][str(player_id)]:
            questsData["players"][str(player_id)]["inventory"] = []
        questsData["players"][str(player_id)]["inventory"].append({"reward": message_id, "item": reward, "tag": tag, "date": str(dt.datetime.now())})
        quests.save()

    def removeRewardFromPlayer(player_id, message_id):
        if str(player_id) in questsData["players"]:
            if "inventory" in questsData["players"][str(player_id)]:
                tag = [r.get("tag", "random") for r in questsData["players"][str(player_id)]["inventory"] if r["reward"] == message_id][0]
                questsData["players"][str(player_id)]["inventory"] = [r for r in questsData["players"][str(player_id)]["inventory"] if r["reward"] != message_id]
                quests.save()
                return tag
        return "random"

    def playerQuests(player_id):
        if str(player_id) in questsData["players"]:
            if "quests" in questsData["players"][str(player_id)]:
                return questsData["players"][str(player_id)]["quests"]
        return 0

    def save():
        db.put_item(TableName="trashbot", Item={'name':{'S':'quests'}, 'data':{'S':json.dumps(questsData)}})