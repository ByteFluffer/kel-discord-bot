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
        
        # Admin management commands
        @bot.slash_command(description="Verwijder meerdere berichten tegelijk! (admin only!)")
        async def purge_admin(inter, berichten_aantal: int):
            if not inter.author.guild_permissions.administrator:
                await inter.response.send_message("Sorry, deze functie is niet toegankelijk voor non-admins!")
            channel = inter.channel    
            await channel.purge(limit=berichten_aantal)
            await inter.response.send_message(f"Ik heb {berichten_aantal} berichten verwijderd!", delete_after=4.0)  

        # Admin community commands
        @bot.slash_command(description="Maak een announcement! (admin only!)")
        async def announce_admin(inter, kanaal: disnake.TextChannel, announcement: str):
            if not inter.author.guild_permissions.administrator:
                await inter.response.send_message("Sorry, deze functie is niet toegankelijk voor non-admins!")
            
            embed=disnake.Embed(title="Announcement!", description=f"Door: {inter.author.mention}", color=EMBED_GOOD)
            embed.add_field(name="Announcement:", value=announcement, inline=False)
            Announce_channel = bot.get_channel(kanaal.id)
            await Announce_channel.send(embed=embed) 
            await inter.response.send_message(f"Ik heb {announcement} naar: {kanaal} gestuurd!", delete_after=4.0)  

            
            
def setup(bot: commands.Bot):
    bot.add_cog(AdminFunctions(bot))        