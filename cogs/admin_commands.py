
import disnake
from disnake.ext import commands, tasks
from env import *
from database import Database
#         levelxpcap = int(8.196 * pow(level + 1, 2.65) + 200)


class Admin_commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Delete multiple messages
    @commands.default_member_permissions(moderate_members=True)
    @commands.slash_command(description="Verwijder meerdere berichten tegelijk!")
    async def purge(inter, berichten_aantal: int):

        await inter.channel.purge(limit=berichten_aantal)
        await inter.response.send_message(f"Ik heb {berichten_aantal} berichten verwijderd!", delete_after=4.0)  
            

def setup(bot: commands.Bot):
    bot.add_cog(Admin_commands(bot))