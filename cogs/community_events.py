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
        await self.welcome_member(self, user)


    async def welcome_member(self, user):
        embed=disnake.Embed(title=f"A member has joined us!", description=f"Welcome {user.mention}", color=disnake.Color.orange())
        channel_to_send = self.bot.get_channel(ChannelIDs.GENERAL)
        await channel_to_send.send(embed=embed)




def setup(bot: commands.Bot):
    bot.add_cog(on_member(bot))