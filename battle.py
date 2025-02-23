import helperfunctions
import random
import math
import logcommand, logging

b = {}

class battle_manager:
    async def run(self, message):
        if message.content == "!battle" or message.content == "!battle <@!450507364768940034>":
            # bot battle
            logcommand.log_globally(logging.INFO, "Bot battle started by " + message.author.name)
            await battle_manager.add_bot_battle(str(message.author.id), message.channel)
        elif message.content.startswith("!battle <@"):
            # user battle
            if (message.mentions[0].id != message.author.id):
                logcommand.log_globally(logging.INFO, "User battle started by " + message.author.name + " with " + message.mentions[0].name)
                await battle_manager.add_user_battle(str(message.author.id), str(message.raw_mentions[0]), self, message.channel)
        elif message.author == self.user and message.content.startswith("battle"):
            # initialize battle
            await b[message.content[6:]].initialize(message)

    async def battle(self, reaction, user):
        uid = str(user.id)
        # print("Reaction received: " + uid + " with emoji " + reaction.emoji)
        if uid in b:
            await b[uid].battle(uid, reaction)

    async def add_bot_battle(uid, channel):
        battle_manager.clean_battles()
        if uid in b:
            channel.send(helperfunctions.pick_string([
                "easy bro one at a time man",
                "bro calm down!! chill! sheesh dawg u aint gotta fight everyone",
                "easy easy EASY EASY bro deep breaths, u dont have to do this"
            ]))
        else:
            bat = BattleB(channel, uid)
            b[uid] = bat

    async def add_user_battle(uid, eid, bot, channel):
        battle_manager.clean_battles()
        if uid in b or eid in b:
            await channel.send(helperfunctions.pick_string([
                "easy bro one at a time man",
                "bro calm down!! chill! sheesh dawg u aint gotta fight everyone",
                "easy easy EASY EASY bro deep breaths, u dont have to do this"
            ]))
        else:
            bat = BattleU(channel, uid, eid, bot)
            b[uid] = bat
            b[eid] = bat
            await bat.spawn()

    def clean_battles():
        mark = []
        for uid in b:
            if not b[uid].active:
                mark.append(uid)
        for x in mark:
            b.pop(x, None)

# holds a bunch of constants
class Battle:
    blank = "<:blank:1343320608917946398>"
    green = "<:green:1343320610041761852>"
    half_green = "<:halfgreen:1343320611040002118>"
    purple = "<:purple:1343320613799854153>"
    half_purple = "<:halfpurple:1343320612050829382>"
    left = "<:left:1343339406437781605>"
    left_red = "<:leftred:1343339407243214888>"
    right = "<:right:1343339408388259840>"
    right_red = "<:rightred:1343339409432379412>"
    attack = "⚔️"
    heal = "💊"
    run = "🏃"
    punch = "💥"
    robot = "🤖"
    hospital = "🚑"

    deads = ["💀", "☠️", "👻", "🪦", "🦴", "⚰️", "🩻", "🙃", "😵"]
    wins = ["😁", "😎", "😤", "😏"]
    normals = ["😠", "😬", "🤪", "🤔"]
    hurts = ["😣", "😟", "😢", "🤒", "🤕", "🤢"]
    crits = ["☢️","⚛️","☣️","💢","💠","🌀","📢","🪄","🗡️","🪓","🔪","🧨","💣","🪚","🔨","🚀","🛰️","🔥"]

class BattleU:
    attack_response = ["oh damn they goin in!",
                       "worldstar!!",
                       "worldstar!",
                       "oh get them!",
                       "yea show them the 1-2 mayweather!",
                       "3-4 mcgreggor!!!",
                       "yo beat the shit outta them!",
                       "yooooooooo!!!!!!!",
                       "show them what fer!",
                       "ohh damn!",
                       "they on x-games mode!"]
    crit_response = ["CRITICAL HIT!!!",
                     "MASSIVE DAMAGE!",
                     "THEY GOIN CRAZZYYYYYY",
                     "WOW THAT WAS A BIG HIT",
                     "IT'S SUPER EFFECTIVE!",
                     "CRITICAL HIT !!"]
    heal_response = ["they chargin up!",
                     "ohkay!",
                     "oh damnn!",
                     "ok dawg he finna heal right up then!",
                     "weird flex but ok",
                     "ooh!",
                     "they need some milk!!",
                     "you aint even seen their final form yet!!!"]
    run_response = ["sorta anticlimactic but ok",
                    "hey how come they can just leave?",
                    "lame!!!",
                    "ok they're running now",
                    "booooooo",
                    "loser"]
    prompt_response = ["ohkay what next tho!",
                       "brooo hit them back!",
                       "damn dawg swing at them!",
                       "HIT THEMMM!!",
                       "AIGHT!",
                       "LES GOOO",
                       "*bruh*!!",
                       "u just gon let them do that!?!",
                       "what u gon do next tho!?"]
    start_response = ["swing first bro, swing first!",
                      "whoa okay guys settle down a lil",
                      "oh they doin it!",
                      "omg someone film this",
                      "broooooooooo",
                      "get their ass!!!"]

    def __init__(self, c, u, e, b):
        self.channel = c
        self.uid = u
        self.eid = e
        self.bot = b

    async def spawn(self):
        await self.channel.send("battle" + str(self.uid))

    async def initialize(self, m):
        self.message = m
        
        # build intro
        await self.message.add_reaction(Battle.attack)
        await self.message.add_reaction(Battle.heal)
        await self.message.add_reaction(Battle.run)
        await self.message.edit(content=helperfunctions.pick_string(BattleU.start_response))
        helperfunctions.bot_wait()

        # set battle vars proper
        self.left_emoji = helperfunctions.pick_string(Battle.normals)
        self.right_emoji = helperfunctions.pick_string(Battle.normals)
        self.left_health = random.randint(10, 30)
        self.right_health = random.randint(10, 30)
        self.active = True
        self.turn = False # false for left's turn, true for right's turn
        self.update_bars()
        await self.message.edit(content=self.bars + "\n" + helperfunctions.pick_string([
            "Pick a button dude lets go!",
            "Aight frosh pick a button!"
            ]))

    def update_bars(self):
        self.bars = ""
        if self.left_health < 0:
            self.left_health = 0
        if self.right_health < 0:
            self.right_health = 0
        blanks = (30-self.left_health) + (30-self.right_health)
        self.bars = self.left_emoji + (Battle.left if self.turn else Battle.left_red) +\
            (Battle.green * math.floor(self.left_health / 2)) +\
            (Battle.half_green if self.left_health % 2 != 0 else "") +\
            (Battle.blank * math.floor(blanks / 2)) +\
            (Battle.half_purple if self.right_health % 2 != 0 else "") +\
            (Battle.purple * math.floor(self.right_health / 2)) +\
            (Battle.right if not self.turn else Battle.right_red) + self.right_emoji

    async def battle(self, uid, reaction):
        if (reaction.emoji == Battle.attack):
            if uid == self.uid and not self.turn:
                await self.left_attack()
            elif uid == self.eid and self.turn:
                await self.right_attack()
        elif (reaction.emoji == Battle.heal):
            if uid == self.uid and not self.turn:
                await self.left_heal()
            elif uid == self.eid and self.turn:
                await self.right_heal()
        elif (reaction.emoji == Battle.run):
            if uid == self.uid and not self.turn:
                await self.left_run()
            elif uid == self.eid and self.turn:
                await self.right_run()
        elif (reaction.emoji in Battle.crits):
            # check to make sure trashbot actually added that emoji
            if reaction.emoji in [r.emoji for r in self.message.reactions]:
                if uid == self.uid:
                    await self.left_crit()
                elif uid == self.eid:
                    await self.right_crit()

    async def left_attack(self):
        if self.active:
            damage = random.randint(5,15)
            self.turn = not self.turn
            self.right_emoji = Battle.punch
            self.update_bars()
            await self.message.edit(content=self.bars + "\n" + helperfunctions.pick_string(BattleU.attack_response))
            self.right_health -= damage
            self.right_emoji = helperfunctions.pick_string(Battle.hurts)
            helperfunctions.bot_wait()
            self.update_bars()
            await self.message.edit(content=self.bars + "\n" + helperfunctions.pick_string(BattleU.prompt_response))
            if helperfunctions.chance(10):
                await self.message.add_reaction(helperfunctions.pick_string(Battle.crits))

            if self.right_health <= 0:
                self.left_emoji = helperfunctions.pick_string(Battle.wins)
                self.right_emoji = helperfunctions.pick_string(Battle.deads)
                self.update_bars()
                await self.message.edit(content=self.bars + "\nAnd <@" + self.uid + "> wins!!!")
                for reaction in self.message.reactions:
                    await reaction.remove(self.bot.user)
                self.active = False

    async def right_attack(self):
        if self.active:
            damage = random.randint(5,15)
            self.turn = not self.turn
            self.left_emoji = Battle.punch
            self.update_bars()
            await self.message.edit(content=self.bars + "\n" + helperfunctions.pick_string(BattleU.attack_response))
            self.left_health -= damage
            self.left_emoji = helperfunctions.pick_string(Battle.hurts)
            helperfunctions.bot_wait()
            self.update_bars()
            await self.message.edit(content=self.bars + "\n" + helperfunctions.pick_string(BattleU.prompt_response))
            if helperfunctions.chance(10):
                await self.message.add_reaction(helperfunctions.pick_string(Battle.crits))

            if self.left_health <= 0:
                self.right_emoji = helperfunctions.pick_string(Battle.wins)
                self.left_emoji = helperfunctions.pick_string(Battle.deads)
                self.update_bars()
                await self.message.edit(content=self.bars + "\nLOL! <@" + self.uid + "> you got your ass kicked bro!")
                for reaction in self.message.reactions:
                    await reaction.remove(self.bot.user)
                self.active = False

    async def left_crit(self):
        if self.active:
            # first remove crit emoji so it doesn't get triggered again
            for reaction in self.message.reactions:
                if reaction.emoji in Battle.crits:
                    await reaction.remove(self.bot.user)
            damage = random.randint(10,20)
            if not self.turn:
                self.turn = not self.turn    
            self.right_emoji = Battle.punch
            self.update_bars()
            await self.message.edit(content=self.bars + "\n" + helperfunctions.pick_string(BattleU.crit_response))
            self.right_health -= damage
            self.right_emoji = helperfunctions.pick_string(Battle.hurts)
            helperfunctions.bot_wait()
            self.update_bars()
            await self.message.edit(content=self.bars + "\n" + helperfunctions.pick_string(BattleU.prompt_response))
            
            if self.right_health <= 0:
                self.left_emoji = helperfunctions.pick_string(Battle.wins)
                self.right_emoji = helperfunctions.pick_string(Battle.deads)
                self.update_bars()
                await self.message.edit(content=self.bars + "\nAnd <@" + self.uid + "> wins!!!")
                for reaction in self.message.reactions:
                    await reaction.remove(self.bot.user)
                self.active = False

    async def right_crit(self):
        if self.active:
            # first remove crit emoji so it doesn't get triggered again
            for reaction in self.message.reactions:
                if reaction.emoji in Battle.crits:
                    await reaction.remove(self.bot.user)
            damage = random.randint(10,20)
            if self.turn:
                self.turn = not self.turn    
            self.left_emoji = Battle.punch
            self.update_bars()
            await self.message.edit(content=self.bars + "\n" + helperfunctions.pick_string(BattleU.crit_response))
            self.left_health -= damage
            self.left_emoji = helperfunctions.pick_string(Battle.hurts)
            helperfunctions.bot_wait()
            self.update_bars()
            await self.message.edit(content=self.bars + "\n" + helperfunctions.pick_string(BattleU.prompt_response))

            if self.left_health <= 0:
                self.right_emoji = helperfunctions.pick_string(Battle.wins)
                self.left_emoji = helperfunctions.pick_string(Battle.deads)
                self.update_bars()
                await self.message.edit(content=self.bars + "\nLOL! <@" + self.uid + "> you got your ass kicked bro!")
                for reaction in self.message.reactions:
                    await reaction.remove(self.bot.user)
                self.active = False

    async def left_heal(self):
        if self.active:
            self.turn = not self.turn
            heal = random.randint(10,20)
            self.left_emoji = Battle.hospital
            self.update_bars()
            await self.message.edit(content = self.bars + "\n" + helperfunctions.pick_string(BattleU.heal_response))
            self.left_health += heal
            self.left_emoji = helperfunctions.pick_string(Battle.normals)
            helperfunctions.bot_wait()
            self.update_bars()
            await self.message.edit(content=self.bars + "\n" + helperfunctions.pick_string(BattleU.prompt_response))
            if helperfunctions.chance(10):
                await self.message.add_reaction(helperfunctions.pick_string(Battle.crits))

    async def right_heal(self):
        if self.active:
            self.turn = not self.turn
            heal = random.randint(10,20)
            self.right_emoji = Battle.hospital
            self.update_bars()
            await self.message.edit(content = self.bars + "\n" + helperfunctions.pick_string(BattleU.heal_response))
            self.right_health += heal
            self.right_emoji = helperfunctions.pick_string(Battle.normals)
            helperfunctions.bot_wait()
            self.update_bars()
            await self.message.edit(content=self.bars + "\n" + helperfunctions.pick_string(BattleU.prompt_response))
            if helperfunctions.chance(10):
                await self.message.add_reaction(helperfunctions.pick_string(Battle.crits))

    async def left_run(self):
        if self.active:
            self.left_emoji = Battle.run
            self.update_bars()
            await self.message.edit(content = self.bars + "\n" + helperfunctions.pick_string(BattleU.run_response))
            self.active = False
            helperfunctions.bot_wait()
            self.left_health = 0
            self.update_bars()
            await self.message.edit(content = self.bars + "\nif you can't take the heat, get out of the fryer dude!")
            for reaction in self.message.reactions:
                await reaction.remove(self.bot.user)

    async def right_run(self):
        if self.active:
            self.right_emoji = Battle.run
            self.update_bars()
            await self.message.edit(content = self.bars + "\n" + helperfunctions.pick_string(BattleU.run_response))
            self.active = False
            helperfunctions.bot_wait()
            self.right_health = 0
            self.update_bars()
            await self.message.edit(content = self.bars + "\ndude i dont think that person wanted to fight anybody")
            for reaction in self.message.reactions:
                await reaction.remove(self.bot.user)

class BattleB:
    attack_response = ["oh damn they goin in!",
                       "worldstar!!",
                       "worldstar!",
                       "oh get them!",
                       "yea show them the 1-2 mayweather!",
                       "3-4 mcgreggor!!!",
                       "yo beat the shit outta them!",
                       "yooooooooo!!!!!!!",
                       "show them what fer!",
                       "ohh damn!",
                       "they on x-games mode!"]
    heal_response = ["they chargin up!",
                     "ohkay!",
                     "oh damnn!",
                     "ok dawg he finna heal right up then!",
                     "weird flex but ok",
                     "ooh!",
                     "they need some milk!!",
                     "you aint even seen their final form yet!!!"]
    run_response = ["sorta anticlimactic but ok",
                    "hey how come they can just leave?",
                    "lame!!!",
                    "ok they're running now",
                    "booooooo",
                    "loser"]
    prompt_response = ["ohkay what next tho!",
                       "brooo hit them back!",
                       "damn dawg swing at them!",
                       "HIT THEMMM!!",
                       "AIGHT!",
                       "LES GOOO",
                       "*bruh*!!",
                       "u just gon let them do that!?!",
                       "what u gon do next tho!?"]
    start_response = ["aight let's go then!!",
                      "aight bet!!!",
                      "come get me dawg!",
                      "you want a fight? u got a fight dude",
                      "oh you wanna go? you wanna go!?",
                      "aaaaaahhhhh don't hurt me"]
    
    def __init__(self, c, u):
        self.channel = c
        self.uid = u

    async def spawn(self):
        await self.channel.send("battle" + str(self.uid))

    async def initialize(self, m):
        self.message = m
        
        # build intro
        await self.message.add_reaction(Battle.attack)
        await self.message.add_reaction(Battle.heal)
        await self.message.add_reaction(Battle.run)
        await self.message.edit(content=helperfunctions.pick_string(BattleB.start_response))
        helperfunctions.bot_wait()

        # set battle vars proper
        self.left_emoji = helperfunctions.pick_string(Battle.normals)
        self.right_emoji = helperfunctions.pick_string(Battle.robot)
        self.left_health = random.randint(10, 30)
        self.right_health = random.randint(10, 30)
        self.active = True
        self.turn = False # false for left's turn, true for right's turn
        self.update_bars()
        await self.message.edit(content=self.bars + "\n" + helperfunctions.pick_string([
            "Pick a button dude lets go!",
            "Aight frosh pick a button!"
            ]))

    def update_bars(self):
        self.bars = ""
        if self.left_health < 0:
            self.left_health = 0
        if self.right_health < 0:
            self.right_health = 0
        blanks = (30-self.left_health) + (30-self.right_health)
        self.bars = self.left_emoji + ":" +\
            (Battle.green * math.floor(self.left_health / 2)) +\
            (Battle.half_green if self.left_health % 2 != 0 else "") +\
            (Battle.blank * math.floor(blanks / 2)) +\
            (Battle.half_purple if self.right_health % 2 != 0 else "") +\
            (Battle.purple * math.floor(self.right_health / 2)) +\
            ":" + self.right_emoji
        
    async def battle(self, uid, reaction):
        if (reaction.emoji == Battle.attack):
            if uid == self.uid and not self.turn:
                await self.left_attack()
        elif (reaction.emoji == Battle.heal):
            if uid == self.uid and not self.turn:
                await self.left_heal()
        elif (reaction.emoji == Battle.run):
            if uid == self.uid and not self.turn:
                await self.left_run()