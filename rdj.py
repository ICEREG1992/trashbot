from PIL import Image, ImageDraw, ImageFont
import helperfunctions
import logcommand, logging
import textwrap
import io
import discord

class rdj:

    async def run(self, message):
        if (message.content.startswith("!rdj ")):
            rdj_img = Image.open("rdj.png")
            color = "black"
            if ('nightmare' in message.content.lower()):
                rdj_img = Image.open("evilrdj.png")
                color = "white"
            draw = ImageDraw.Draw(rdj_img)
            font = ImageFont.truetype('ARLRDBD.TTF', 36)
            text = message.content[5:]
            offset = 100
            for line in textwrap.wrap(text, width=20):
                draw.text((60, offset), line, font=font, fill=color)
                bbox = font.getbbox(line)
                offset += bbox[3]-bbox[1]
            await rdj.send_image(rdj_img, message.channel, text)
        elif (message.content.startswith("!rdj")):
            rdj_img = Image.open("rdj.png")
            draw = ImageDraw.Draw(rdj_img)
            font = ImageFont.truetype('ARLRDBD.TTF', 36)
            text = helperfunctions.pick_string([
                "funny funny message laugh now please",
                "robert downy junior",
                "R.I.P. Tupac",
                "This is so sad",
                "i hid the last of the rations for myself my children are going to starve to death",
                "spongbob squarepants",
                "Peter Griffin would not say something like this",
                "rdj meme generator no watermark",
                "smash that like and subscribe button and be sure to ring that bell"
            ])
            offset = 100
            for line in textwrap.wrap(text, width=20):
                draw.text((60, offset), line, font=font, fill="black")
                bbox = font.getbbox(line)
                offset += bbox[3]-bbox[1]
            await rdj.send_image(rdj_img, message.channel, text)
        elif (message.content.startswith("!ithinkitis ")):
            ithink_img = Image.open("ithink.png")
            draw = ImageDraw.Draw(ithink_img)
            font = ImageFont.truetype('arialbd.ttf', 46)
            text = message.content[12:]
            draw.text((321, 6), text, font=font, fill="black")
            await rdj.send_image(ithink_img, message.channel, text)
    async def send_image(img, channel, text):
        with io.BytesIO() as out:
            img.save(out, format="PNG")
            out.seek(0)
            f = discord.File(fp=out, filename="rdj.png", description="robert downy junior meme that says \"" + text + "\"")
            await channel.send(file=f)
