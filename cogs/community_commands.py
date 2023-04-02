import disnake
from disnake.ext import commands, tasks
from env import *


class Community_commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    # Ping and latency command
    @commands.slash_command(description="Get my latency!")
    async def ping(self, inter):
        await inter.response.send_message(f"OMG! I'm still alive! I'm also living with a `{(await Community_commands.get_bot_lantency(self))}` latency!")


    # Get in 
    async def get_bot_lantency(self):
        latency = self.bot.latency
        return round(latency, 2)


def setup(bot: commands.Bot):
    bot.add_cog(Community_commands(bot))