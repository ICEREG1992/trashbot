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
            logcommand.log_globally(logging.INFO, "User battle started by " + message.author.name + " with " + message.mentions[0].name)
            await battle_manager.add_user_battle(str(message.author.id), str(message.raw_mentions[0]), message.channel)
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

    async def add_user_battle(uid, eid, channel):
        battle_manager.clean_battles()
        if uid in b or eid in b:
            await channel.send(helperfunctions.pick_string([
                "easy bro one at a time man",
                "bro calm down!! chill! sheesh dawg u aint gotta fight everyone",
                "easy easy EASY EASY bro deep breaths, u dont have to do this"
            ]))
        else:
            bat = BattleU(channel, uid)
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
    blank = "<:blank:445505783224991747>"
    green = "<:green:482986420668071937>"
    half_green = "<:halfgreen:482986735073230848>"
    purple = "<:purple:482986438195937291>"
    half_purple = "<:halfpurple:482986748926885908>"
    attack = "⚔️"
    heal = "💊"
    run = "🏃"
    punch = "💥"
    robot = "🤖"
    hospital = "🚑"

    deads = ["💀", "👻", "🙃", "😵"]
    wins = ["😁", "☺️", "😤"]
    normals = ["😠", "😬", "🤪", "🤔"]
    hurts = ["😣", "😟", "😢", "🤒", "🤕", "🤢"]

class BattleU:
    attack_response = ["oh damn he goin in!", "worldstar!!", "worldstar!", "oh get him!", "yea show him the 1-2 mayweather!", "3-4 mcgreggor!!!", "yo beat the shit outta him!", "yooooooooo!!!!!!!", "show him what fer!", "ohh damn!"]
    heal_response = ["he chargin up!", "ohkay!", "oh damnn!", "ok bro he finna heal right up then!", "weird flex but ok", "ooh!", "he need some milk!!", "you aint even seen his final form yet!!!"]
    run_response = ["sorta anticlimactic but ok", "hey how come he can just leave?", "fuckin lame!", "ok he's running now", "booooooo", "loser"]
    prompt_response = ["ohkay what next tho!", "brooo hit him back!", "damn bro swing at him!", "HIT HIMMM!!", "AIGHT!", "LES GOOO", "*bruh*!!", "u just gon let him do that!?!", "what u gon do next tho!?"]
    start_response = ["swing first bro, swing first!", "whoa okay guys settle down a lil", "oh he doin it!", "omg someone film this", "broooooooooo"]

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
            "Pick a button bro lets go!",
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
            elif uid != self.uid and self.turn:
                await self.right_attack()
        elif (reaction.emoji == Battle.heal):
            if uid == self.uid and not self.turn:
                await self.left_heal()
            elif uid != self.uid and self.turn:
                await self.right_heal()
        elif (reaction.emoji == Battle.run):
            if uid == self.uid and not self.turn:
                await self.left_run()
            elif uid != self.uid and self.turn:
                await self.right_run()

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

            if self.right_health <= 0:
                self.left_emoji = helperfunctions.pick_string(Battle.wins)
                self.right_emoji = helperfunctions.pick_string(Battle.deads)
                self.update_bars()
                await self.message.edit(content=self.bars + "\nAnd <@" + self.uid + "> wins!!!")
                for reaction in self.message.reactions:
                    reaction.clear()
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

            if self.left_health <= 0:
                self.right_emoji = helperfunctions.pick_string(Battle.wins)
                self.left_emoji = helperfunctions.pick_string(Battle.deads)
                self.update_bars()
                await self.message.edit(content=self.bars + "\nLOL! <@" + self.uid + "> you got your ass kicked bro!")
                for reaction in self.message.reactions:
                    reaction.clear()
                self.active = False

    async def left_heal(self):
        if self.active:
            heal = random.randint(10,20)
            self.left_emoji = Battle.hospital
            self.update_bars()
            await self.message.edit(content = self.bars + "\n" + helperfunctions.pick_string(BattleU.heal_response))
            self.left_health += heal
            self.left_emoji = helperfunctions.pick_string(Battle.normals)
            helperfunctions.bot_wait()
            self.update_bars()
            await self.message.edit(content=self.bars + "\n" + helperfunctions.pick_string(BattleU.prompt_response))

            self.turn = not self.turn

    async def right_heal(self):
        if self.active:
            heal = random.randint(10,20)
            self.right_emoji = Battle.hospital
            self.update_bars()
            await self.message.edit(content = self.bars + "\n" + helperfunctions.pick_string(BattleU.heal_response))
            self.right_health += heal
            self.right_emoji = helperfunctions.pick_string(Battle.normals)
            helperfunctions.bot_wait()
            self.update_bars()
            await self.message.edit(content=self.bars + "\n" + helperfunctions.pick_string(BattleU.prompt_response))

            self.turn = not self.turn

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

class BattleB:
    x = ""