import json
import random
import urllib.parse
import urllib.request

class witscord:
    async def run(self, message):
        parts = message.content.split(' ', 1)
        if parts[0] == "witsco!random":
            await message.channel.send(self.witsco_random())
        elif parts[0] == "witsco!search":
            if len(parts) < 2:
                await message.channel.send("search what")
                return
            await message.channel.send(self.witsco_search(parts[1]))

    def witsco_random():
        random_url = 'http://witscord.net/~staz/w/api.php?action=query&list=random&rnnamespace=0&format=json'
        title = json.load(urllib.request.urlopen(random_url))['query']['random'][0]['title']
        return 'http://witscord.net/~staz/w/index.php/' + urllib.parse.quote(title)

    def witsco_search_url(query, what):
        return ('http://witscord.net/~staz/w/api.php?action=query&list=search&format=json&srwhat='
            + urllib.parse.quote(what) + '&srnamespace=0&srlimit=20&srsearch=' + urllib.parse.quote(query))

    def witsco_search(query):
        result = json.load(urllib.request.urlopen(witscord.witsco_search_url(query, 'title')))['query']['search']
        if len(result) > 0:
            return 'http://witscord.net/~staz/w/index.php/' + urllib.parse.quote(result[0]['title'])
        result = json.load(urllib.request.urlopen(witscord.witsco_search_url(query, 'text')))['query']['search']
        if len(result) > 0:
            return 'http://witscord.net/~staz/w/index.php/' + urllib.parse.quote(random.choice(result)['title'])