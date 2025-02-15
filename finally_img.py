from PIL import Image, ImageDraw, ImageFont, ImageSequence
import helperfunctions
import logcommand, logging
import datetime as dt
import textwrap
import io
import base64
import discord
import requests
import os
from urllib.parse import quote

global c
c = [dt.datetime.utcnow(), 0]

global token
if os.path.exists("img.txt"):
    f = open("img.txt", "r")
    token = f.read().split('\n')
    f.close()

class finally_img:

    async def run(self, message):
        global t
        global c
        google_image_request = None
        if (message.channel.id == 555540666776813568 or isinstance(message.channel, discord.channel.DMChannel)):
            if (message.content.startswith("!finally ")):
                # reset c if it's time
                if (dt.datetime.utcnow() > c[0] + dt.timedelta(days=1)):
                    c[0] = dt.datetime.utcnow()
                    c[1] = 0
                if (c[1] < 80):
                    if helperfunctions.chance(5):
                        template_img = Image.open("finally2.png")
                    else:
                        template_img = Image.open("finally.png")
                    text = message.content[9:]
                    # add image
                    google_image = finally_img.get_google_image(text, 0)
                    match google_image:
                        case -1:
                            await message.channel.send("google doesn't have that")
                            return
                        case 1:
                            await message.channel.send("couldn't find any images for that")
                        case 0:
                            await message.channel.send("google didn't like when i asked for that")
                    # open the image url pulled
                    try:
                        google_image_request = requests.get(google_image, timeout=5)
                    except:
                        None
                    for i in range(1,5):
                        c[1] = c[1] + 1
                        if google_image_request is not None and google_image_request.status_code == 200:
                            image_stream = io.BytesIO(google_image_request.content)
                            google_image = Image.open(image_stream)
                            break
                        else:
                            google_image = finally_img.get_google_image(text, i)
                            match google_image:
                                case 1:
                                    await message.channel.send("couldn't find any images for that")
                                case 0:
                                    await message.channel.send("google didn't like when i asked for that")
                            # open the image url pulled
                            try:
                                google_image_request = requests.get(google_image, timeout=5)
                            except:
                                None
                    else:
                        await message.channel.send("i tried really hard but there's no image for that")
                        return
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
                    if(google_image.is_animated):
                        imageout = finally_img.process_gif(template_img, google_image)
                        await finally_img.send_gif(imageout, message.channel, text)
                    else:
                        # resize image
                        google_image.thumbnail((300,250))
                        # paste image onto template
                        finally_img.paste_with_transparency(template_img, google_image, (180,70))
                        await finally_img.send_image(template_img, message.channel, text)
                elif (c[1] >= 80):
                    await message.channel.send("out of requests for today, sry")
        elif "!finally " in message.content:
            await message.add_reaction("🚫")

    def process_gif(baseimage, animatedimage):
        iter = ImageSequence.Iterator(animatedimage)
        framesout = []
        #cap to like frames so you dont spend forever processing gifs
        #maybe actually set a timer of some sort instead of doing it like this
        for i in range(0, min(animatedimage.n_frames, 120)):
            frame = iter[i].copy()
            frame.thumbnail((300,250))
            newframe = baseimage.copy()
            
            finally_img.paste_with_transparency(newframe, frame, (180,70))
            framesout.append(newframe)
        return framesout

    def paste_with_transparency(image, secondimage, location):
        if secondimage.mode in ("RGBA", "LA"):
            image.paste(secondimage, location, secondimage)
        else:
            image.paste(secondimage, location)

    async def send_gif(img, channel, text):
        with io.BytesIO() as out:
            img[0].save(out, save_all=True, format="GIF", append_images= img[1:], duration=100, loop=0)
            out.seek(0)
            f = discord.File(fp=out, filename="finally.gif", description="person holding test tube finally meme that says \"FINALLY, " + text + "\"")
            await channel.send(file=f)

    async def send_image(img, channel, text):
        with io.BytesIO() as out:
            img.save(out, format="PNG")
            out.seek(0)
            f = discord.File(fp=out, filename="finally.png", description="person holding test tube finally meme that says \"FINALLY, " + text + "\"")
            await channel.send(file=f)

    def get_google_image(query, n):
        url = f"https://www.googleapis.com/customsearch/v1?q={quote(query)}&num=1&start={n}&safe=active&imgSize=medium&searchType=image&key={token[1]}&cx={token[0]}"
        # headers = {
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0"
        # }
        response = requests.get(url)
        if response.status_code == 200:
            if int(response.json()['searchInformation']['totalResults']) > 0:
                if len(response.json()['items']) > 0:
                    return response.json()['items'][0]['link']
                else:
                    return 1
            else:
                return -1
        else:
            return 0
