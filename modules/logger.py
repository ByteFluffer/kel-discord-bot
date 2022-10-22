async def on_message_delete(message):
    async for entry in message.guild.audit_logs(limit=1,action=disnake.AuditLogAction.message_delete):
        deleter = entry.user
    print(f"{deleter.name} deleted message by {message.author.name}")