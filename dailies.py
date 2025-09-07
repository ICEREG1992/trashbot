import datetime as dt
import random

class dailies:
    async def run(self, message):
        if message.content == "!dailies":
            seed = dt.datetime.now().strftime("%Y%m%d")
            # seed the RNG
            random.seed(seed)

            number_of_games = 1
            result = random.randint(1, number_of_games)

            match result:
                case 1:
                    await message.channel.send("Today's daily game is: Chess")
                case _:
                    await message.channel.send("Error: No daily game found")