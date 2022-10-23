import disnake
from disnake.ext import commands

# EMBED colors:
EMBED_DANGER = 0xFF0000
EMBED_GOOD = 0x00FF00
EMBED_ORANGE = 0xFFA500

code_formats = ["py", "css"]
class Community(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # code
        @bot.event
        async def on_message(inter):
            message_ext_check = inter.content.lower()
            channel_msg = inter.channel.id
            if "```" in message_ext_check:
                if message_ext_check in code_formats:
                        print("")
                else:
                    Channel_send_msg = bot.get_channel(channel_msg)
                    await Channel_send_msg.send("Je hebt een codeblock gebruikt, zonder een extensie zoals: py, css etc. Gebruik: ```py etc. ") 

        # Close the forum channel
        @bot.slash_command(description="Sluit dit forum kanaal!")
        @commands.cooldown(1, 3, commands.BucketType.user)
        async def solved(inter):
            channel_msg = inter.channel.id
            Channel_send_msg = bot.get_channel(channel_msg)

            embed=disnake.Embed(title=":white_check_mark: Probleem als opgelost gemarkeerd door:", description=inter.author.mention, color=EMBED_GOOD)
            await send_to_log(channel_msg, embed)

        # Sending to log channel
        async def send_to_log(channel_msg, embed):
            ForumChannel = bot.get_channel(channel_msg)
            await ForumChannel.send(embed=embed) 


def setup(bot: commands.Bot):
    bot.add_cog(Community(bot))