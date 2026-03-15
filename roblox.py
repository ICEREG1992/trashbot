from helperfunctions import pick_string
import discord

count = 0

class roblox:
    bday_server = 1480091673005658114
    vc_channel_id = 1480091673714360496
    william_id = 132374584086364160

    async def run(self, message):
        global count

        if message.content == "!rtv":
            if message.channel.type == discord.ChannelType.private:
                count += 1
                await message.channel.send(pick_string([
                    "vote has been rocked, thx",
                    "your vote has been tallied",
                    "vote count received, it'll be over soon <3",
                    "you've rocked the vote"
                ]))

                guild = self.bot.get_guild(self.bday_server)
                vc_channel = guild.get_channel(self.vc_channel_id)
                vc_member_count = len(vc_channel.members) if vc_channel else 1

                if count >= vc_member_count / 2:
                    william = await self.bot.fetch_user(self.william_id)
                    dm = await william.create_dm()
                    await dm.send(f"RTV! ({count}/{vc_member_count} votes): send me `!nextmap [link]`")
            else:
                await message.channel.send("anonymous !rtv, take it to dms pls")

        elif message.content.startswith("!nextmap") and message.author.id == self.william_id:
            parts = message.content.split(" ", 1)
            if len(parts) < 2:
                await message.channel.send("usage: `!nextmap [link]`")
                return

            count = 0
            await message.channel.send(f"next map: {parts[1]}")