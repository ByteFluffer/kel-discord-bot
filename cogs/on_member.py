import disnake
from disnake.ext import commands


class on_member(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        @bot.event
        async def on_member_ban(guild, user):
            print(f"Aaaah! er is een member/memberina gebanned! Naam: {user}, server: {guild}")



def setup(bot: commands.Bot):
    bot.add_cog(on_member(bot))