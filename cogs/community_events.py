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
        embed=disnake.Embed(title=f"A member has joined us!", description=f"Welcome {user}", color=disnake.Color.orange())
        channel_to_send = self.bot.get_channel(ChannelIDs.GENERAL)
        await channel_to_send.send(embed=embed)

        # Welcome message
        embed=disnake.Embed(title=f"Hi {user.mention}, welcome! Please verify yourself by clicking the verify button in verification-and-roles!", description=f"Also: while youre there: Assign yourself some roles!", color=disnake.Color.orange())
        channel_to_send = self.bot.get_channel(ChannelIDs.WELCOME)
        await channel_to_send.send(embed=embed)



def setup(bot: commands.Bot):
    bot.add_cog(on_member(bot))