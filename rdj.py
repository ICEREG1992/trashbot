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
                offset += font.getsize(line)[1]
            await rdj.send_image(rdj_img, message.channel)
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
                offset += font.getsize(line)[1]
            await rdj.send_image(rdj_img, message.channel)

    async def send_image(img, channel):
        with io.BytesIO() as out:
            img.save(out, format="PNG")
            out.seek(0)
            f = discord.File(fp=out, filename="rdj.png")
            await channel.send(file=f)
