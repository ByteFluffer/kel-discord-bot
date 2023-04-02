import disnake
from disnake.ext import commands
from env import *

class on_member(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Member 
    @commands.Cog.listener()
    async def on_member_join(self, user):
        print("Er is een member erbij gekomen!")

        # Welcome message
        verify_and_role_channel = self.bot.get_channel(1091452292584177744)

        embed=disnake.Embed(title=f"Welcome!", description=f"{user.mention}, please verify yourself by clicking the verify button in {verify_and_role_channel.mention}.", color=disnake.Color.orange())
        channel_to_send = self.bot.get_channel(ChannelIDs.WELCOME)
        msg = await channel_to_send.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(on_member(bot))