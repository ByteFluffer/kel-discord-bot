import disnake
from disnake.ext import commands
import time

# EMBED colors:
EMBED_DANGER = 0xFF0000
EMBED_GOOD = 0x00FF00
EMBED_ORANGE = 0xFFA500

class AdminFunctions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        # Close the forum channel
        @bot.slash_command(description="Verwijder meerdere berichten tegelijk! (admin only!)")
        @commands.cooldown(1, 3, commands.BucketType.user)
        async def purge_admin(inter, berichten_aantal: int):
            if not inter.author.guild_permissions.administrator:
                await inter.response.send_message("Sorry, deze functie is niet toegankelijk voor non-admins!")
            channel = inter.channel    
            await channel.purge(limit=berichten_aantal)
            await inter.response.send_message(f"Ik heb {berichten_aantal} berichten verwijderd!", delete_after=4.0)  

            
            
def setup(bot: commands.Bot):
    bot.add_cog(AdminFunctions(bot))        