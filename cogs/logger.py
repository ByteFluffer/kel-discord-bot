import disnake
from disnake.ext import commands

# Logging colors:
LOGGING_DANGER = 0xFF0000
LOGGING_GOOD = 0x00FF00
LOGGING_ORANGE = 0xFFA500

class PingCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Message logging
        @bot.event
        async def on_raw_message_delete(messageDeleted):
                
                embed=disnake.Embed(title="Bericht verwijderd door:", description="KomtNog", color=LOGGING_DANGER)
                embed.add_field(name=f"Verwijderde bericht:", value=messageDeleted, inline=False)

                await send_to_log(embed)
                
        # On bulk message deletion
        @bot.event
        async def on_raw_bulk_message_delete(BulkMessageDeleted):
            
                embed=disnake.Embed(title="Bulk berichten verwijderd door:", description="Komtnog", color=LOGGING_DANGER)
                embed.add_field(name=f"Verwijderde berichten:", value="Komtnog", inline=False)

                await send_to_log(embed)
                
        # When a message is edited        
        @bot.event
        async def on_raw_message_edit(messageEdited):

                embed=disnake.Embed(title="Bericht edited door:", description="KomtNog", color=LOGGING_ORANGE)
                embed.add_field(name=f"Geedited bericht:", value=messageEdited, inline=False)
                print(messageEdited)

                await send_to_log(embed)



        # Channel logging
        @bot.event
        async def on_guild_channel_delete(channelDeleted):
            async for entry in channelDeleted.guild.audit_logs(limit=1, action=disnake.AuditLogAction.channel_delete):

                embed=disnake.Embed(title="Channel verwijderd door:", description=entry.user.mention, color=LOGGING_DANGER)
                embed.add_field(name=f"Kanaalnaam:", value=channelDeleted, inline=False)

                await send_to_log(embed)
                
        # When new channel is created
        @bot.event
        async def on_guild_channel_create(channelMaked):
            async for entry in channelMaked.guild.audit_logs(limit=1, action=disnake.AuditLogAction.channel_delete):

                embed=disnake.Embed(title="Channel gemaakt door:", description=entry.user.mention, color=LOGGING_GOOD)
                embed.add_field(name=f"Kanaalnaam:", value=channelMaked, inline=False)

                await send_to_log(embed)
                
        # When channel name is edited
        @bot.event
        async def on_raw_guild_channel_edit(channelEdited):
            async for entry in channelEdited.guild.audit_logs(limit=1, action=disnake.AuditLogAction.channel_delete):

                embed=disnake.Embed(title="Channel Geedit door:", description=entry.user.mention, color=LOGGING_ORANGE)
                embed.add_field(name=f"Kanaalnaam:", value=channelEdited, inline=False)
                
                await send_to_log(embed)


        # Sending to log channel
        async def send_to_log(embed):
            LogChannel = bot.get_channel(1033152626507923507)
            await LogChannel.send(embed=embed) 





def setup(bot: commands.Bot):
    bot.add_cog(PingCommand(bot))