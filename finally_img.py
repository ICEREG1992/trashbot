from PIL import Image, ImageDraw, ImageFont
import helperfunctions
import logcommand, logging
import datetime as dt
import textwrap
import io
import base64
import discord
import requests
from bs4 import BeautifulSoup

global t
t = dt.datetime.utcnow()

class finally_img:

    async def run(self, message):
        if (message.content.startswith("!finally ")):
            if (t > dt.datetime.utcnow() - dt.timedelta(seconds=30)):
                template_img = Image.open("finally.png")
                text = message.content[9:]
                # add image
                google_image = finally_img.get_google_image(text)
                # open the image url pulled
                google_image_request = requests.get(google_image)
                if google_image_request.status_code == 200:
                    image_stream = io.BytesIO(google_image_request.content)
                    google_image = Image.open(image_stream)
                else:
                    await channel.send("oops something went wrong back here")
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
                await finally_img.send_image(template_img, message.channel)
            else:
                await message.add_reaction('🚫')

    async def send_image(img, channel):
        with io.BytesIO() as out:
            img.save(out, format="PNG")
            out.seek(0)
            f = discord.File(fp=out, filename="rdj.png")
            await channel.send(file=f)

    def get_google_image(query):
        url = f"https://www.google.com/search?q={query}&tbm=isch"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            img_tags = soup.find_all("img")
            if img_tags:
                for img in img_tags:
                    deferred = img.get("data-deferred")
                    if not deferred:
                        img_height = img.get("height")
                        if img_height and int(img_height) > 48:
                            image_url = img.get("data-src")
                            return image_url
            else:
                return
        else:
            return
