import helperfunctions
from permissions import permissions
import boto3
import json
import logcommand, logging

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global lyrics
lyrics = "•"

k = {}

class karaoke_manager:
    # this module is included for historical purposes
    # it acts a little weird around the end of songs but otherwise is pretty good
    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'lyrics'}})
        global lyrics
        lyrics = json.loads(d['Item']['data']['S'])

    async def run(self, message):
        if (message.content == "!karaoke"):
            print(message.channel)
            logcommand.log_globally(logging.INFO, "Karaoke started in " + str(message.channel.id))
            await karaoke_manager.add_karaoke(message.channel)
        elif (message.channel.id in k and k[message.channel.id].active):
            await k[message.channel.id].run(message)
            # karaoke.run takes care of setting active to False
        elif (message.content.startswith("!givelyrics ") and permissions.allowed(message.author.id, "blue", "red")):
            new_lyrics = message.content[12:]
            global lyrics
            lyrics = new_lyrics.split("\n")
            await message.channel.send("New lyrics loaded!")
            logcommand.log_globally(logging.INFO, "New karaoke lyrics loaded by " + message.author.name)
            karaoke_manager.save(lyrics)

    async def add_karaoke(channel):
        karaoke_manager.clean_karaoke()
        if channel.id not in k:
            x = Karaoke(lyrics.copy(), channel)
            await x.start()
            k[channel.id] = x

    def clean_karaoke():
        mark = []
        for x in k:
            if not k[x].active:
                mark.append(x)
        for x in mark:
            k.pop(x, None)

    def save(l):
        db.put_item(TableName="trashbot", Item={'name':{'S':'lyrics'}, 'data':{'S':json.dumps(l)}})


class Karaoke:
    def __init__(self, lyrics, channel):
        self.active = True
        self.lyrics = lyrics
        self.channel = channel
        self.next()

    async def start(self):
        await self.channel.send("duuuuude i love this song. okay i'll start")
        await helperfunctions.bot_wait()
        await self.channel.send(self.next_line)
        self.next()

    async def run(self, message):
        if self.active:
            if message.content == "!exit" or message.content == "!quit" or message.content == "!stop":
                await self.channel.send("yeah, i get kinda bored there too. thanks for singing with me.")
                self.active = False
            elif len(self.lyrics) > 0:
                u_line = Karaoke.format(message.content)
                e_line = Karaoke.format(self.next_line)
                # print(u_line + " // " + e_line)

                u_set = word_set(u_line.split(" "))
                e_set = word_set(e_line.split(" "))
                out_set = self.next_line.split(" ")

                # figure out where u_set starts (before or after?)
                if Karaoke.comes_first(e_set, u_set): # u_set starts after
                    Karaoke.align_sets(e_set, u_set)

                    # match each word onward, allowing for 2 extras/missing
                    self.consume_input(e_set, u_set)
                    
                    # if e_set is gone, get next line and send it, formatted
                    if (len(e_set) == 0): # if we're out of words, recharge and send
                        self.next()
                        await self.channel.send(Karaoke.sing(self.next_line, Karaoke.num_exclamation(message.content), Karaoke.is_uppercase(message.content)))
                    else:
                        # if not, get the rest and send it original, and formatted
                        await self.channel.send(Karaoke.sing(" ".join(out_set[-len(e_set.words):]), Karaoke.num_exclamation(message.content), Karaoke.is_uppercase(message.content)))

                    # load next line
                    self.next()

                elif Karaoke.comes_first(u_set, e_set): # u_set starts before
                    Karaoke.align_sets(u_set, e_set)

                    # match each word onward, allowing for 2 extras/missing
                    self.consume_input(e_set, u_set)

                    # if e_set is gone, get next line and send it, formatted
                    if (len(e_set) == 0): # if we're out of words, recharge
                        self.next()
                        await self.channel.send(Karaoke.sing(self.next_line, Karaoke.num_exclamation(message.content), Karaoke.is_uppercase(message.content)))
                    else:
                        # if not, get the rest and send it original, and formatted
                        await self.channel.send(Karaoke.sing(" ".join(out_set[-len(e_set.words):]), Karaoke.num_exclamation(message.content), Karaoke.is_uppercase(message.content)))

                    # load next line
                    self.next()

                else:
                    await self.channel.send(helperfunctions.pick_string([
                        "hey.. i thought we had a thing going? if u want to, you can say !exit to stop.",
                        "thats not how the song goes...",
                        "i dont think i remember that line being there",
                        "come on man, sing the song :c. u can say !exit to stop if u wanna"]))

            if len(self.lyrics) == 0:
                await self.channel.send("i think that's where the song ends. thanks for singing with me.")
                self.active = False

    def align_sets(starts_first, starts_second):
        while starts_second[0] not in starts_first:
            starts_second.words.pop(0)
        starts_first.words = starts_first.words[starts_first.words.index(starts_second[0]) + 1:]
        starts_second.words.pop(0)

    def ensure_words(self):
        return

    def consume_input(self, expected, user):
        strikes = 3
        while (len(user.words) != 0 and (user[0] in expected or expected[0] in expected)):
            # every word it's off, subtract a strike
            # print(str(expected.index(user[0])) + ", " + str(user.index(expected[0])))
            m = max(value for value in [expected.index(user[0]), user.index(expected[0])] if value is not None)
            if (m == expected.index(user[0])):
                strikes -= expected.index(user[0])
                if strikes < 2:
                    # you're out of strikes, break
                    break
                else:
                    expected.words = expected.words[expected.index(user[0]) + 1:]
                    user.words.pop(0)
                    if (len(expected.words) == 0 and len(user) != 0): # if we're out of words, recharge
                        self.next()
                        expected = word_set(Karaoke.format(self.next_line).split(" "))
                        out_set = self.next_line.split(" ")
            else:
                strikes -= user.index(expected[0])
                if strikes < 2:
                    # you're out of strikes, break
                    break
                else:
                    user.words = user.words[user.index(expected[0]) + 1:]
                    expected.words.pop(0)
                    if (len(expected.words) == 0 and len(user) != 0): # if we're out of words, recharge
                        self.next()
                        expected = word_set(Karaoke.format(self.next_line).split(" "))
                        out_set = self.next_line.split(" ")

    def comes_first(a, b):
        x = -1
        y = -1
        for i in range(len(a)):
            if a[i] in b:
                x = i
                break
        for i in range(len(b)):
            if b[i] in a:
                y = i
                break
        return x > y or (x > -1 and x == y)

    def next(self):
        self.next_line = self.lyrics.pop(0)
        if (len(self.next_line) == 0):
            self.next_line = self.lyrics.pop(0)
        if (self.next_line == "•"):
            self.next_line = ""
    
    def format(line):
        return Karaoke.shorten(Karaoke.remove_punc(line.lower()))

    def sing(line, exclamation, uppercase):
        return line.upper() + ("!" * exclamation) if uppercase else line + ("!" * exclamation)

    def shorten(line):
        l = list(line)
        for c in range(len(l)-1):
            if (l[c] == l[c+1]):
                l[c] = ""
        while l[len(l)-1] == " ": # remove trailing spaces
            l.pop(len(l)-1)
        s = "".join(l)
        print(s)
        return s

    def remove_punc(line):
        l = list(line)
        for i in range(len(l)):
            char = l[i]
            if not (char.isalpha() or char in "() ？、"): #remove all body punctuation
                l[i] = ""
        # char = l[-1]
        # if not (char.isalpha() or char in "?!"): # preserve ending ? or ! characters
        #     l[len(l)-1] = ""
        s = "".join(l)
        return s

    def is_uppercase(line):
        count = 0
        for i in line:
            if (i.islower()):
                count += 1
        return count < (len(line)/4)

    def num_exclamation(line):
        return line.count("!")

    def words_similar(a, b):
        hits = 0
        misses = 0
        b_copy = str(b)
        for c in a:
            if c in b:
                hits += 1
                b_copy = b_copy.replace(c, "")
            else:
                misses += 1
        a_copy = str(a)
        for c in b:
            if c in a_copy:
                hits += 1
                a_copy = a_copy.replace(c, "")
            else:
                misses += 1
        return hits > (misses * (.4 * ((len(a) + len(b)) / 2)))

class word_set:
    def __init__(self, l):
        self.words = l
    
    def __contains__(self, key):
        for s in self.words:
            if Karaoke.words_similar(s, key):
                return key
    
    def __getitem__(self, key):
        return self.words[key]

    def index(self, key):
        for i in range(len(self.words)):
            if Karaoke.words_similar(self.words[i], key):
                return i

    def __len__(self):
        return len(self.words)

    def __str__(self):
        return " ".join(self.words)