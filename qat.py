import re
import requests
import sys

# thx kube

class qat:

    async def run(self, message):
        if message.content.lower().startswith("!qat "):
            s = message.content[5:]
            r = requests.post("https://www.quinapalus.com/cgi-bin/qat", params={"ent": "Search", "pat": s, "dict": 0})
            allText = r.text

            if ("Error: pattern too long or too complex" in allText):
                await message.channel.send("qat says `Error: pattern too long or too complex`")
                return

            if ("Error: unexpected character in pattern" in allText):
                await message.channel.send("qat says `Error: unexpected character in pattern`")
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
