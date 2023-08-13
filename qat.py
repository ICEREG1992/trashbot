import re
import requests
import sys

e = ("Error: pattern too long or too complex",
    "Error: unexpected character in pattern",
    "Error: expected } at end of tagged item")

dicts = ("UKACD",
        "YAWL",
        "ABLE",
        "Moby",
        "PDL",
        "BNC",
        "Broda",
        "Union")

global dict
dict = 4

# thx kube

class qat:

    async def run(self, message):
        global dict
        if message.content.lower().startswith("!qat "):
            s = message.content[5:]
            r = requests.post("https://www.quinapalus.com/cgi-bin/qat", params={"ent": "Search", "pat": s, "dict": dict})
            allText = r.text

            for error in e:
                if (error in allText):
                    await message.channel.send("qat says `" + error + "`")
                    return

            # Replace strings in text
            replacements = [["<br>", ""], ["<td>", ""], 
                            ["<tr>", ""], ["</tr>", ""], 
                            ["<td>", ""], ["</td>", ""], 
                            ["&nbsp;&nbsp;", "_"], ["&nbsp;", ""], 
                            ["&middot;", "·"]]
            for replacement in replacements:
                allText = allText.replace(replacement[0], replacement[1])

            # Convert text to list of lines
            allLines = allText.splitlines()

            # Anticipate start and end of results block
            startOffset = 0
            if (re.match(r".*([A-Z]).*", s)):
                startString, endString = "</form>", "</table>"
                startOffset = 2
            else:
                startString, endString = "</form>", "Total solutions found"
                startOffset = 1
            start, end = 0, 0

            # Find where results start and end
            for line in enumerate(allLines):
                if (startString in line[1] and start == 0):
                    start = line[0]
                elif (endString in line[1] and end == 0):
                    end = line[0]

            # Only keep lines with results
            resultLines = filter(
                lambda line: re.match(r"<b>|<i>", line) is None,
                allLines[start+startOffset:end]
            )
            
            # Convert list of lines to list of words
            resultWords = [ word
                            for line in resultLines
                            for word in line.split(" ") ]

            # send results
            if len(resultWords) > 0:
                await message.channel.send(' '.join(resultWords)[0:2000])
            else:
                await message.channel.send('i got nothin boss')
        elif message.content.lower().startswith("!dict"):
            if len(message.content) > 6:
                pc = message.content.lower()[6:]
                if pc in [a.lower() for a in dicts]:
                    dict = dicts.index(pc)
                    await message.channel.send('successfully set qat dictionary to `' + dicts[dict] + '`')
                else:
                    await message.channel.send('thats not a dictionary')
            else:
                await message.channel.send('qat dictionary currently set to `' + dicts[dict] + '`.\navailable dictionaries: `UKACD`, `YAWL`, `ABLE`, `Moby`, `PDL`, `BNC`, `Broda`, `Union`. the default is `PDL`. ')
                