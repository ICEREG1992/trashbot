import datetime as dt
import io
from PIL import Image, ImageDraw, ImageFont, ImageSequence, ImageColor
import random

import discord

class dailies:
    async def run(self, message):
        if message.content == "!daily":
            seed = dt.datetime.now().strftime("%Y%m%d")
            # seed the RNG
            random.seed(seed)

            number_of_games = 1
            result = random.randint(1, number_of_games)

            match result:
                case 1:
                    # Connect the dots
                    img = Image.new('RGB', (512, 512), color = (255, 255, 255))
                    draw = ImageDraw.Draw(img)
                    text = "Connect the dots!"
                    font = ImageFont.truetype("ARLRDBD.TTF", 28)

                    # Get text size
                    text_bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]

                    # Position centered horizontally, near top
                    x = (512 - text_width) // 2
                    y = 30

                    # Draw text
                    draw.text((x, y), text, font=font, fill="black")

                    # Draw underline
                    underline_y = y + text_height + 10
                    draw.line((x, underline_y, x + text_width, underline_y), fill="black", width=2)
                    # Generate random points
                    if random.random() < 0.1:
                        points = random.choice([
                            [(256, 140), (311, 103), (378, 92), (424, 122), (443, 182), (422, 261), (262, 464), (86, 247), (82, 167), (121, 110)],
                            [(43, 491), (51, 478), (76, 480), (54, 461), (72, 453), (95, 457), (108, 474), (125, 469), (115, 453), (140, 453), (115, 436), (90, 407), (83, 368), (96, 320), (68, 306), (65, 329), (42, 342), (29, 364), (12, 354), (14, 341), (23, 328), (29, 303), (42, 283), (48, 262), (40, 249), (55, 257), (59, 275), (74, 264), (107, 254), (80, 277), (108, 270), (132, 286), (105, 283), (123, 294), (145, 320), (130, 311), (139, 339), (131, 367), (128, 349), (119, 360), (123, 383), (140, 403), (172, 414), (206, 417), (215, 395), (189, 368), (164, 339), (150, 307), (144, 271), (153, 240), (161, 205), (151, 174), (113, 160), (90, 167), (70, 147), (42, 138), (36, 127), (46, 118), (63, 118), (93, 116), (126, 124), (147, 121), (166, 109), (144, 135), (166, 142), (189, 151), (200, 157), (175, 155), (198, 169), (211, 180), (215, 193), (192, 183), (207, 199), (211, 220), (208, 243), (200, 215), (202, 246), (200, 264), (190, 278), (190, 251), (184, 271), (181, 293), (194, 333), (229, 363), (272, 385), (290, 390), (312, 375), (318, 341), (311, 295), (288, 250), (246, 210), (244, 244), (231, 219), (232, 187), (237, 154), (213, 168), (238, 137), (275, 119), (284, 114), (260, 111), (235, 117), (258, 105), (289, 105), (319, 112), (295, 82), (319, 94), (340, 115), (361, 128), (352, 102), (350, 77), (359, 94), (366, 112), (383, 132), (399, 145), (407, 164), (438, 190), (434, 215), (418, 212), (390, 195), (357, 188), (344, 154), (318, 142), (290, 148), (284, 167), (290, 188), (312, 221), (331, 247), (348, 272), (363, 339), (358, 389), (338, 433), (355, 435), (379, 429), (396, 412), (386, 381), (383, 399), (377, 380), (385, 356), (368, 367), (380, 343), (400, 326), (380, 332), (389, 320), (404, 313), (421, 309), (395, 301), (421, 302), (440, 313), (440, 296), (456, 287), (449, 302), (459, 320), (473, 337), (482, 359), (491, 376), (477, 384), (461, 367), (440, 360), (435, 339), (419, 341), (413, 357), (427, 392), (425, 425), (404, 449), (387, 461), (417, 461), (400, 473), (415, 482), (392, 483), (392, 491), (285, 489), (178, 491), (91, 493)],
                            [(256, 106), (299, 240), (443, 248), (325, 317), (372, 452), (258, 365), (147, 451), (193, 318), (77, 239), (219, 241)]
                            ])
                    else:
                        points = [(random.randint(20, 492), random.randint(50, 492)) for _ in range(random.randint(8,13))]
                    
                    for idx, point in enumerate(points):
                        draw.ellipse((point[0]-5, point[1]-5, point[0]+5, point[1]+5), fill="blue")
                        draw.text((point[0]+8, point[1]-8), str(idx+1), fill="black")
                    await dailies.send_image(img, message.channel, "Connect the dots")

                case 2:
                    # Guess the hex
                    img = dailies.base_daily_image("Guess the color name!")
                    c = ImageColor.colormap[random.choice(list(ImageColor.colormap.keys()))]
                    draw = ImageDraw.Draw(img)
                    if random.random() < 0.5:
                        if random.random() < 0.5:
                            # Draw a filled square
                            draw.rectangle((106, 125, 406, 425), fill=c)
                        else:
                            # Draw a filled circle
                            draw.ellipse((106, 125, 406, 425), fill=c)
                    else:
                        # Write the hex code in black, large and centered                        
                        font = ImageFont.truetype("ARLRDBD.TTF", 80)
                        text_bbox = draw.textbbox((0, 0), c, font=font)
                        text_width = text_bbox[2] - text_bbox[0]
                        text_height = text_bbox[3] - text_bbox[1]
                        x = (512 - text_width) // 2
                        y = (512 - text_height) // 2
                        draw.text((x, y), c, font=font, fill="black")
                    await dailies.send_image(img, message.channel, "Guess the hex color")
                # case 2:
                #     # Sudoku
                # case 3:
                #     # Word ladder
                # case 4:
                #     # Guess the rot
                
                # case 6:
                #     # Hot dog eating contest
                case _:
                    await message.channel.send("Error: No daily game found")


    def base_daily_image(title):
        img = Image.new('RGB', (512, 512), color = (255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("ARLRDBD.TTF", 28)

        # Get text size
        text_bbox = draw.textbbox((0, 0), title, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Position centered horizontally, near top
        x = (512 - text_width) // 2
        y = 30

        # Draw text
        draw.text((x, y), title, font=font, fill="black")

        # Draw underline
        underline_y = y + text_height + 10
        draw.line((x, underline_y, x + text_width, underline_y), fill="black", width=2)
        return img

    async def send_image(img, channel, text):
        with io.BytesIO() as out:
            img.save(out, format="PNG")
            out.seek(0)
            f = discord.File(fp=out, filename="daily.png", description=f"Trashbot daily game for {dt.datetime.now().strftime('%Y-%m-%d')}: {text}")
            await channel.send(file=f)