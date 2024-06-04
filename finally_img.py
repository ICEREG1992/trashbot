from PIL import Image, ImageDraw, ImageFont
import helperfunctions
import logcommand, logging
import datetime as dt
import textwrap
import io
import base64
import discord
import requests
import os

global t
t = dt.datetime.utcnow()

global token
if os.path.exists("img.txt"):
    f = open("img.txt", "r")
    token = f.read().split('\n')
    f.close()

class finally_img:

    async def run(self, message):
        global t
        if (message.content.startswith("!finally ")):
            print('finally')
            if (t < dt.datetime.utcnow() - dt.timedelta(seconds=30)):
                if helperfunctions.chance(5):
                    template_img = Image.open("finally2.png")
                else:
                    template_img = Image.open("finally.png")
                text = message.content[9:]
                # add image
                google_image = finally_img.get_google_image(text)
                match google_image:
                    case 2:
                        await message.channel.send("couldn't get a suitable image for that")
                    case 1:
                        await message.channel.send("couldn't find any images for that")
                    case 0:
                        await message.channel.send("google didn't like when i asked for that")
                # open the image url pulled
                google_image_request = requests.get(google_image)
                if google_image_request.status_code == 200:
                    image_stream = io.BytesIO(google_image_request.content)
                    google_image = Image.open(image_stream)
                else:
                    await message.channel.send("whoops couldn't get the full image")
                    return
                # paste image onto template
                template_img.paste(google_image, (150,70))
                # add text
                shadowcolor = "black"
                fillcolor = "white"
                x = 100
                y = 320
                font = ImageFont.truetype('IMPACT.TTF', 46)
                # no need for textwrap here
                draw = ImageDraw.Draw(template_img)
                # thicker border
                text = text.upper()
                draw.text((x-2, y-2), text, font=font, fill=shadowcolor)
                draw.text((x+2, y-2), text, font=font, fill=shadowcolor)
                draw.text((x-2, y+2), text, font=font, fill=shadowcolor)
                draw.text((x+2, y+2), text, font=font, fill=shadowcolor)
                # now draw the text over it
                draw.text((x, y), text, font=font, fill=fillcolor)
                t = dt.datetime.utcnow()
                await finally_img.send_image(template_img, message.channel, text)
            else:
                print("not yet")
                await message.add_reaction("🚫")

    async def send_image(img, channel, text):
        with io.BytesIO() as out:
            img.save(out, format="PNG")
            out.seek(0)
            f = discord.File(fp=out, filename="finally.png", description="man holding test tube finally meme that says \"FINALLY, " + text + "\"")
            await channel.send(file=f)

    def get_google_image(query):
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&num=1&start=1&imgSize=huge&searchType=image&key={token[1]}&cx={token[0]}"
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
        # }
        response = requests.get(url)
        if response.status_code == 200:
            if len(response.json()['items']) > 0:
                return response.json()['items'][0]['image']['thumbnailLink'] 
            else:
                return 1
        else:
            return 0
