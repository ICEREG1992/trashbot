import datetime as dt
import io
from io import BytesIO
import string
import requests
from PIL import Image, ImageDraw, ImageFont, ImageSequence, ImageColor
import random
import helperfunctions
from permissions import permissions
from wonderwords import RandomWord
import discord
import boto3
import json
from zoneinfo import ZoneInfo

CENTRAL = ZoneInfo("America/Chicago")

global db
db = boto3.client('dynamodb', region_name='us-east-2')

global stats
stats = {}

class dailies:

    pastels = [
        "#FBF8CC", "#FDE4CF", "#FFCFD2", "#F1C0E8", "#CFBAF0",
        "#A3C4F3", "#90DBF4", "#8EECF5", "#98F5E1", "#B9FBC0"
    ]

    def init():
        d = db.get_item(TableName="trashbot", Key={'name':{'S':'dailies'}})
        global stats
        if ('data' in d['Item']):
            data = json.loads(d['Item']['data']['S'])
            stats = data

    async def run(self, message):
        global stats
        if message.content == "!daily" or message.content == "!dailies":
            seed = dt.datetime.now().strftime("%Y%m%d")
            random.seed(seed)

            number_of_games = 7
            result = random.randint(1, number_of_games)

            match result:
                case 1:
                    img = dailies.base_daily_image("Connect the dots!")
                    draw = ImageDraw.Draw(img)
                    # Generate random points
                    if random.random() < 0.2:
                        points = random.choice([
                            [(256, 140), (311, 103), (378, 92), (424, 122), (443, 182), (422, 261), (262, 464), (86, 247), (82, 167), (121, 110)],
                            [(43, 491), (51, 478), (76, 480), (54, 461), (72, 453), (95, 457), (108, 474), (125, 469), (115, 453), (140, 453), (115, 436), (90, 407), (83, 368), (96, 320), (68, 306), (65, 329), (42, 342), (29, 364), (12, 354), (14, 341), (23, 328), (29, 303), (42, 283), (48, 262), (40, 249), (55, 257), (59, 275), (74, 264), (107, 254), (80, 277), (108, 270), (132, 286), (105, 283), (123, 294), (145, 320), (130, 311), (139, 339), (131, 367), (128, 349), (119, 360), (123, 383), (140, 403), (172, 414), (206, 417), (215, 395), (189, 368), (164, 339), (150, 307), (144, 271), (153, 240), (161, 205), (151, 174), (113, 160), (90, 167), (70, 147), (42, 138), (36, 127), (46, 118), (63, 118), (93, 116), (126, 124), (147, 121), (166, 109), (144, 135), (166, 142), (189, 151), (200, 157), (175, 155), (198, 169), (211, 180), (215, 193), (192, 183), (207, 199), (211, 220), (208, 243), (200, 215), (202, 246), (200, 264), (190, 278), (190, 251), (184, 271), (181, 293), (194, 333), (229, 363), (272, 385), (290, 390), (312, 375), (318, 341), (311, 295), (288, 250), (246, 210), (244, 244), (231, 219), (232, 187), (237, 154), (213, 168), (238, 137), (275, 119), (284, 114), (260, 111), (235, 117), (258, 105), (289, 105), (319, 112), (295, 82), (319, 94), (340, 115), (361, 128), (352, 102), (350, 77), (359, 94), (366, 112), (383, 132), (399, 145), (407, 164), (438, 190), (434, 215), (418, 212), (390, 195), (357, 188), (344, 154), (318, 142), (290, 148), (284, 167), (290, 188), (312, 221), (331, 247), (348, 272), (363, 339), (358, 389), (338, 433), (355, 435), (379, 429), (396, 412), (386, 381), (383, 399), (377, 380), (385, 356), (368, 367), (380, 343), (400, 326), (380, 332), (389, 320), (404, 313), (421, 309), (395, 301), (421, 302), (440, 313), (440, 296), (456, 287), (449, 302), (459, 320), (473, 337), (482, 359), (491, 376), (477, 384), (461, 367), (440, 360), (435, 339), (419, 341), (413, 357), (427, 392), (425, 425), (404, 449), (387, 461), (417, 461), (400, 473), (415, 482), (392, 483), (392, 491), (285, 489), (178, 491), (91, 493)],
                            [(256, 106), (299, 240), (443, 248), (325, 317), (372, 452), (258, 365), (147, 451), (193, 318), (77, 239), (219, 241)],
                            [(100, 200), (200, 200), (200, 300), (100, 300)], # square
                            [(115, 432), (117, 248), (49, 248), (258, 103), (465, 250), (400, 251), (400, 433), (290, 433), (290, 322), (229, 322), (228, 432), (128, 433)], #house
                            [(69, 392), (187, 440), (249, 282), (326, 279), (343, 219), (494, 208), (492, 122), (128, 129), (111, 106), (100, 130), (78, 142), (101, 214), (44, 385)],
                            [(260, 281), (275, 246), (322, 238), (346, 264), (342, 313), (314, 354), (247, 369), (181, 345), (160, 278), (168, 210), (225, 162), (308, 154), (390, 182), (434, 287), (414, 379), (356, 425), (260, 445), (138, 427), (77, 345), (76, 244), (121, 121)],
                            [(53, 345), (74, 179), (54, 233), (90, 345), (127, 203), (102, 238), (129, 344), (162, 273), (144, 285), (162, 335), (185, 271), (206, 340), (242, 272), (216, 280), (241, 338), (266, 272), (266, 342), (295, 272), (313, 342), (339, 275), (356, 345), (370, 274), (385, 347), (405, 346), (418, 272), (420, 348), (441, 275), (451, 343), (471, 274), (485, 345)] # minimum
                            ])
                    else:
                        points = [(random.randint(20, 492), random.randint(70, 492)) for _ in range(random.randint(8,13))]
                    
                    for idx, point in enumerate(points):
                        draw.ellipse((point[0]-5, point[1]-5, point[0]+5, point[1]+5), fill="blue")
                        draw.text((point[0]+8, point[1]-8), str(idx+1), fill="black")
                    await dailies.send_image(img, message.channel, "Connect the dots")

                case 2:
                    # Guess the hex
                    img = dailies.base_daily_image("Guess the color name!")
                    draw = ImageDraw.Draw(img)

                    c = ImageColor.colormap[random.choice(list(ImageColor.colormap.keys()))]
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
                
                case 3:
                    # Sudoku
                    img = dailies.base_daily_image("Solve sudoku!")
                    board = dailies.generate_sudoku()
                    img = dailies.draw_sudoku(img, board)
                    await dailies.send_image(img, message.channel, "Solve sudoku")

                case 4:
                    # Guess the rot
                    img = dailies.base_daily_image("Guess the rot!")
                    draw = ImageDraw.Draw(img)
                    img = dailies.draw_rot_puzzle(img, draw)
                    await dailies.send_image(img, message.channel, "Guess the rot")
                
                case 5:
                    # word ladder
                    img = dailies.base_daily_image("Word ladder!")
                    draw = ImageDraw.Draw(img)
                    img = dailies.draw_word_ladder(img, draw)
                    await dailies.send_image(img, message.channel, "Word ladder")

                case 6:
                    # Activity day
                    if random.random() < 0.1:
                        # Not a daily
                        options = 2
                        result = random.randint(1, options)

                        match result:
                            case 1:
                                # random noise
                                pixels = [random.randint(0, 255) for _ in range(512 * 512)]
                                img = Image.new('L', (512, 512))
                                img.putdata(pixels)
                                await dailies.send_image(img, message.channel, "Randomly generated daily")

                            case 2:
                                # no daily today
                                img = dailies.base_daily_image("No daily today")
                                await dailies.send_image(img, message.channel, "No daily today")
                    else:
                        activities = [("Hot dog eating contest!", "u1f32d"),
                                    ("High jump!", "u1f574"),
                                    ("Ping pong!", "u1f3d3"),
                                    ("Let's go gambling!", "u1f3b0"),
                                    ("Let's sing the song of your life.", "u1f3b6"),
                                    ("Eat a cheeseburger!", "u1f354"),
                                    ("Eat a butter!", "u1f9c8"),
                                    ("Go silly mode!", "u1f92a")]
                        activity = random.choice(activities)
                        img = dailies.base_daily_image(activity[0])
                        draw = ImageDraw.Draw(img)
                        # Fetch and paste emoji
                        url = f"https://raw.githubusercontent.com/googlefonts/noto-emoji/main/png/512/emoji_{activity[1]}.png"
                        r = requests.get(url)
                        size = random.randint(100, 400)
                        emoji = Image.open(BytesIO(r.content)).convert("RGBA")
                        emoji.thumbnail((size, size), Image.LANCZOS)
                        img.paste(emoji, ((512 - size) // 2, (512 - size) // 2 + 20), emoji)

                        await dailies.send_image(img, message.channel, activity[0])
                    
                case 7:
                    # mc challenge
                    objectives = ["Find diamonds!", "Get wood!", "Build a house!", "Find iron!", "Reach bedrock!", "Reach build limit!", "Die!", "Make stone tools!", "Sleep in a bed!", "Kill a creeper!"]
                    objective = random.choice(objectives)
                    img = dailies.base_daily_image(objective)
                    draw = ImageDraw.Draw(img)
                    word = RandomWord(rng=random).word(word_min_length=4, word_max_length=12)
                    msg = "!hostmc seed:" + word

                    font = ImageFont.truetype("ARLRDBD.TTF", 40)
                    text_bbox = draw.textbbox((0, 0), msg, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                    x = (512 - text_width) // 2
                    y = (512 - text_height) // 2
                    draw.text((x, y), msg, font=font, fill="black")

                    await dailies.send_image(img, message.channel, objective)
                
                case _:
                    await message.channel.send("Error: No daily game found")
        
        # Handle !claim on a !daily image
        if message.content.lower() in ["!claim", "!clum", "!clam", "!clom", "!clamb", "!clab", "!clem", "!clym"]:
            ref = message.reference
            if ref:
                referenced = await message.channel.fetch_message(ref.message_id)
                is_daily = (
                    referenced.author == self.user
                    and any(a.filename == "daily.png" for a in referenced.attachments)
                )
                if is_daily:
                    daily_date = referenced.created_at.astimezone(CENTRAL).strftime("%Y-%m-%d")
                    claim_date = message.created_at.astimezone(CENTRAL).strftime("%Y-%m-%d")
                    if daily_date != claim_date:
                        await message.channel.send(helperfunctions.pick_string(["neener neener neener", "cold mold on a slate plate", "wrong", "you are NOT affirmed."]))
                    else:
                        uid = str(message.author.id)
                        if uid not in stats:
                            stats[uid] = []
                        if daily_date not in stats[uid]:
                            stats[uid].append(daily_date)
                        else:
                            await message.channel.send("yessssssss more more more keep claiming keep claiming")
                            return
                        await message.channel.send(helperfunctions.pick_string(["so true bestie", "you are SO affirmed", "facts", "so proud of you girl", "so happy for u", "this is ur \"popping off\" era"]))
                        dailies.save(stats)
            return
        
        if message.content.lower() == "!dailyboard":
            entries = []
            for uid, dates in stats.items():
                count = len(dates)
                streak = dailies.get_streak(dates)
                entries.append((uid, count, streak))
            entries.sort(key=lambda x: x[1], reverse=True)

            embed = discord.Embed(title=helperfunctions.pick_string(["da Dailyboard", "Dailies Leaderboard", "Daily daily daily", "Daileaderboard", "Dailyboard"]))
            for uid, count, streak in entries[:5]:
                user = await self.fetch_user(int(uid))
                name = user.display_name if user else uid
                embed.add_field(
                    name=name,
                    value=f"**{count}** claims" + (f" | 🔥 {streak} day streak" if streak >= 3 else ""),
                    inline=False
                )
            await message.channel.send(embed=embed)
            return
        
        if message.content.lower() == "!cleardailies" and permissions.allowed(message.author.id, "blue"):
            await message.channel.send("wiped clean baby")
            stats = {}
            dailies.save(stats)
            
    def get_streak(dates):
        if not dates:
            return 0
        parsed = sorted(set(dt.date.fromisoformat(d) for d in dates), reverse=True)
        today = dt.date.today()
        # streak must include today or yesterday to be active
        if parsed[0] < today - dt.timedelta(days=1):
            return 0
        streak = 1
        for i in range(1, len(parsed)):
            if parsed[i - 1] - parsed[i] == dt.timedelta(days=1):
                streak += 1
            else:
                break
        return streak

    def generate_sudoku():
        """Generate a random valid solved sudoku board, then remove numbers to create a puzzle."""
        def is_valid(board, row, col, num):
            if num in board[row]:
                return False
            if num in [board[r][col] for r in range(9)]:
                return False
            box_r, box_c = 3 * (row // 3), 3 * (col // 3)
            for r in range(box_r, box_r + 3):
                for c in range(box_c, box_c + 3):
                    if board[r][c] == num:
                        return False
            return True

        def solve(board):
            for row in range(9):
                for col in range(9):
                    if board[row][col] == 0:
                        nums = list(range(1, 10))
                        random.shuffle(nums)
                        for num in nums:
                            if is_valid(board, row, col, num):
                                board[row][col] = num
                                if solve(board):
                                    return True
                                board[row][col] = 0
                        return False
            return True

        # Generate solved board
        board = [[0] * 9 for _ in range(9)]
        solve(board)

        # Remove numbers to create puzzle (remove ~50 cells)
        puzzle = [row[:] for row in board]
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        difficulty = random.randint(35,60)
        for r, c in cells[:difficulty]:
            puzzle[r][c] = 0

        # hehe
        if random.random() < 0.2:
            empty_cells = [(r, c) for r in range(9) for c in range(9) if puzzle[r][c] == 0]
            if empty_cells:
                r, c = random.choice(empty_cells)
                rule = random.choice(['row', 'col', 'box'])
                if rule == 'row':
                    conflicts = [puzzle[r][cc] for cc in range(9) if puzzle[r][cc] != 0]
                elif rule == 'col':
                    conflicts = [puzzle[rr][c] for rr in range(9) if puzzle[rr][c] != 0]
                else:
                    box_r, box_c = 3 * (r // 3), 3 * (c // 3)
                    conflicts = [puzzle[rr][cc] for rr in range(box_r, box_r + 3)
                                for cc in range(box_c, box_c + 3) if puzzle[rr][cc] != 0]
                if conflicts:
                    puzzle[r][c] = random.choice(conflicts)
        
        # hehehe
        if random.random() < 0.05:
            num = random.randint(0, 9)
            puzzle = [[num] * 9 for _ in range(9)]
        
        # hehehehe
        if random.random() < 0.05:
            puzzle = [[random.randint(1, 9) if cell != 0 else 0 for cell in row] for row in puzzle]

        return puzzle

    def draw_sudoku(img, board):
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("ARLRDBD.TTF", 18)

        # Push grid down to clear the title, and tighten the right/bottom margins
        margin_left = 40
        margin_top = 80   # was 40 — gives room for title
        grid_size = 424   # divisible by 9 = 47.1px per cell, fits within 512 - 40 - ~48 margin
        cell_size = grid_size // 9  # 47

        # Draw filled cells
        for row in range(9):
            for col in range(9):
                num = board[row][col]
                if num != 0:
                    x = margin_left + col * cell_size
                    y = margin_top + row * cell_size
                    bbox = draw.textbbox((0, 0), str(num), font=font)
                    tw = bbox[2] - bbox[0]
                    th = bbox[3] - bbox[1] + 8
                    draw.text(
                        (x + (cell_size - tw) // 2, y + (cell_size - th) // 2),
                        str(num), font=font, fill="black"
                    )

        # Draw grid lines
        for i in range(10):
            thickness = 3 if i % 3 == 0 else 2
            x = margin_left + i * cell_size
            y = margin_top + i * cell_size
            # Vertical lines: from margin_top to margin_top + grid_size exactly
            draw.line([(x, margin_top), (x, margin_top + cell_size * 9)], fill="black", width=thickness)
            # Horizontal lines: from margin_left to margin_left + grid_size exactly
            draw.line([(margin_left, y), (margin_left + cell_size * 9, y)], fill="black", width=thickness)

        return img
    
    def generate_rot_puzzle():
        if random.random() < 0.1:
            length = random.randint(5, 8)
            chars = ''.join(random.choice(string.ascii_uppercase) for _ in range(length))
            return chars, -1

        rw = RandomWord(rng=random)
        word = None
        for _ in range(200):  # safety cap in case no word ever matches
            candidate = rw.word(word_min_length=5, word_max_length=10).upper()
            if any(candidate.count(c) >= 3 for c in candidate):
                word = candidate
                break
        if word is None:
            word = candidate  # fall back to whatever we last got

        rot = random.randint(1, 25)
        rotated = ''.join(
            chr((ord(c) - ord('A') + rot) % 26 + ord('A')) if c.isalpha() else c
            for c in word
        )
        return rotated, rot

    def draw_rot_puzzle(img, draw):
        word, rot = dailies.generate_rot_puzzle()
        font_large = ImageFont.truetype("ARLRDBD.TTF", 48)
        font_small = ImageFont.truetype("ARLRDBD.TTF", 16)

        # 3% chance to just be a rotting image
        if random.random() < 0.03:
            url = random.choice(["https://upload.wikimedia.org/wikipedia/commons/7/7f/Bitter_rot_on_a_Honeycrisp_apple.jpg",
                                 "https://www.weatherall.com/cdn/shop/articles/Weatherall_-_3_Types_of_Log_Rot_and_How_to_Treat_Each_One_1.jpg?v=1489279005",
                                 "https://www.southernliving.com/thmb/Zuog5BduX0BtWXBFYF84UGUTn4c=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/GettyImages-1192872187-412ebeba29884406837f3fe52a4a810a.jpg"])
            r = requests.get(url)
            rot_img = Image.open(BytesIO(r.content)).convert("RGBA")
            size = random.randint(100, 400)
            rot_img.thumbnail((size, size), Image.LANCZOS)
            img.paste(rot_img, ((512 - size) // 2, (512 - size) // 2 + 20), rot_img)
            return img

        # Draw the rotated word centered
        bbox = draw.textbbox((0, 0), word, font=font_large)
        tw = bbox[2] - bbox[0]
        draw.text(((512 - tw) // 2, 200), word, font=font_large, fill="black")
        # Draw hint
        hint = "ROT-?"
        bbox2 = draw.textbbox((0, 0), hint, font=font_small)
        tw2 = bbox2[2] - bbox2[0]
        draw.text(((512 - tw2) // 2, 280), hint, font=font_small, fill="grey")
        return img

    def draw_word_ladder(img, draw):
        rw = RandomWord(rng=random)

        # 3% chance to just say "LADDER"
        if random.random() < 0.03:
            font = ImageFont.truetype("ARLRDBD.TTF", 64)
            bbox = draw.textbbox((0, 0), "LADDER", font=font)
            tw = bbox[2] - bbox[0]
            draw.text(((512 - tw) // 2, 220), "LADDER", font=font, fill="black")
            return img
        
        # 3% chance to just be a ladder
        if random.random() < 0.03:
            # Fetch and paste ladder
            if random.random() < 0.5:
                url = "https://raw.githubusercontent.com/googlefonts/noto-emoji/main/png/512/emoji_u1fa9c.png"
            else:
                url = "https://wg-assets-s3.s3.eu-west-2.amazonaws.com/wp-content/uploads/2023/05/27120109/1200-026.webp"
            r = requests.get(url)
            size = random.randint(100, 400)
            ladder = Image.open(BytesIO(r.content)).convert("RGBA")
            ladder.thumbnail((size, size), Image.LANCZOS)
            img.paste(ladder, ((512 - size) // 2, (512 - size) // 2 + 20), ladder)
            return img

        # 10% chance for different lengths, otherwise same
        if random.random() < 0.2:
            length1, length2 = random.choice([(4, 5), (5, 4)])
        else:
            length1 = length2 = random.choice([4, 5])

        word1 = rw.word(word_min_length=length1, word_max_length=length1).upper()

        # Regenerate word2 until it shares at least one letter with word1
        while True:
            word2 = rw.word(word_min_length=length2, word_max_length=length2).upper()
            if set(word1) & set(word2):  # intersection: any shared characters?
                break

        font = ImageFont.truetype("ARLRDBD.TTF", 64)

        # Draw word1 centered
        bbox1 = draw.textbbox((0, 0), word1, font=font)
        tw1 = bbox1[2] - bbox1[0]
        draw.text(((512 - tw1) // 2, 160), word1, font=font, fill="black")

        # Draw arrow between words
        arrow_x = 512 // 2
        arrow_top = 245
        arrow_bottom = 275
        draw.line([(arrow_x, arrow_top), (arrow_x, arrow_bottom)], fill="black", width=3)
        draw.polygon([
            (arrow_x - 10, arrow_bottom - 10),
            (arrow_x + 10, arrow_bottom - 10),
            (arrow_x, arrow_bottom + 5)
        ], fill="black")

        # Draw word2 centered below
        bbox2 = draw.textbbox((0, 0), word2, font=font)
        tw2 = bbox2[2] - bbox2[0]
        draw.text(((512 - tw2) // 2, 295), word2, font=font, fill="black")

        return img

    def base_daily_image(title):
        bg_color = (255, 255, 255)
        if random.random() < 0.25:
            bg_color = random.choice(dailies.pastels)
        img = Image.new('RGB', (512, 512), color=bg_color)
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("ARLRDBD.TTF", 28)
        date_font = ImageFont.truetype("ARLRDBD.TTF", 16)

        # Draw date in top left corner
        date_str = dt.datetime.today().strftime('%Y-%m-%d')
        draw.text((10, 6), date_str, font=date_font, fill="black")

        # Add !claim
        if random.random() < 0.33:
            claim_word = random.choices(["!CLAIM", "!CLUM", "!CLAM"], weights=[50, 25, 25])[0]
            claim_text = f"REPLY {claim_word} TO AFFIRM"
            claim_font = ImageFont.truetype("ARLRDBD.TTF", 18)
            claim_bbox = draw.textbbox((0, 0), claim_text, font=claim_font)
            claim_width = claim_bbox[2] - claim_bbox[0]
            claim_height = claim_bbox[3] - claim_bbox[1]
            draw.text(((512 - claim_width) // 2, 512 - claim_height - 12), claim_text, font=claim_font, fill="grey")

        # Get text size
        text_bbox = draw.textbbox((0, 0), title, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        # Position centered horizontally, near top
        x = (512 - text_width) // 2
        y = 30
        # Draw title
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
    
    def save(stats):
        db.put_item(TableName="trashbot", Item={'name':{'S':'dailies'}, 'data': {'S': json.dumps(stats)}})
        