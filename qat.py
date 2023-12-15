import re
import requests
import sys
import helperfunctions

e = ("Error: pattern too long or too complex",
    "Error: unexpected character in pattern",
    "Error: expected } at end of tagged item",
    "Error: LHS must be single variable in negated match constraint")

dicts = ["UKACD",
        "YAWL",
        "ABLE",
        "Moby",
        "PDL",
        "BNC",
        "Broda",
        "Union"]

global dict
dict = 4

# thx kube

class qat:

    async def run(self, message):
        global dict
        if message.content.lower().startswith("!qat ") or message.content.lower().startswith("!taq "):
            s = message.content[5:]
            spoilerResult = False
            if s.startswith("||") and s.endswith("||"):
                spoilerResult = True
                s = s[2:-2] 
            r = requests.get("https://www.quinapalus.com/cgi-bin/qat", params={"ent": "Search", "pat": s, "dict": dict}, headers={"User-Agent": "qat-cli/1.0.0"})
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
            if (re.match(r".*(([A-Z])|(;)).*", s)):
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
                if (message.content.lower().startswith("!taq")):
                    resultWords.reverse()
                resultText = ' '.join(resultWords)[0:(1996 if spoilerResult else 2000)]
                if spoilerResult:
                    resultText = "||" + resultText + "||"
                await message.channel.send(resultText)
            else:
                await message.channel.send(helperfunctions.pick_string([
                    'i got nothin boss',
                    'computer says no',
                    "qat told me to tell you that there's nothing like that",
                    "i dunno i dunno",
                    "reply hazy, try again",
                    "my sources say no",
                    "outlook not so good"
                ]))
        elif message.content.lower().startswith("!dict"):
            if len(message.content) > 6:
                pc = message.content.lower()[6:]
                ld = [a.lower() for a in dicts]
                if pc in ld:
                    dict = ld.index(pc)
                    await message.channel.send('successfully set qat dictionary to `' + dicts[dict] + '`')
                else:
                    await message.channel.send('thats not a dictionary')
            else:
                await message.channel.send('qat dictionary currently set to `' + dicts[dict] + '`.\navailable dictionaries: `UKACD`, `YAWL`, `ABLE`, `Moby`, `PDL`, `BNC`, `Broda`, `Union`. the default is `PDL`. ')
                