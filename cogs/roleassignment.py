import disnake
from disnake.ext import commands, tasks
from env import *
from database import Database


class roleassignment(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.message_id_one = 1091764040092626994


    # Listening to reactions added
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):

        # First reaction role message
        REACTION_ROLE_MSG_ONE = 1091764040092626994
        
        guild = await self.bot.fetch_guild(1002208148930691172)
        user = await guild.fetch_member(reaction.user_id)

        # Reaction role one
        if reaction.message_id == REACTION_ROLE_MSG_ONE:
            type= "add"
            await self.reaction_roles_one(guild, user, reaction, type)


    # Listening to reactions removed
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction):
        print("1")
        # First reaction role message
        REACTION_ROLE_MSG_ONE = 1091779444626178209
        
        guild = await self.bot.fetch_guild(1002208148930691172)
        user = await guild.fetch_member(reaction.user_id)

        # Reaction role one
        if reaction.message_id == REACTION_ROLE_MSG_ONE:
            print("2")
            type= "remove"
            await self.reaction_roles_one(guild, user, reaction, type)


    # Mother command
    @commands.default_member_permissions(moderate_members=True)
    @commands.slash_command()
    async def reaction_roles(self, inter):
        pass
    

    # Adding a message to reaction roles
    @reaction_roles.sub_command(description="Add a reaction role to a excisting message")
    async def add(self, inter, msg_id, emoji_one= None, emoji_two= None, emoji_three= None, emoji_four= None, emoji_five= None):
        msg = await inter.channel.fetch_message(msg_id)
        
        if emoji_one != None:
            await msg.add_reaction(emoji_one)
        if emoji_two != None:
            await msg.add_reaction(emoji_two)
        if emoji_three != None:
            await msg.add_reaction(emoji_three)
        if emoji_four != None:
            await msg.add_reaction(emoji_four)
        if emoji_five != None:
            await msg.add_reaction(emoji_five)        

        await inter.response.send_message("Done!", ephemeral=True)


    # First reaction role
    async def reaction_roles_one(self, guild, user, reaction, type):

        if str(reaction.emoji) == "💻":
            role = guild.get_role(1091490645719388301)
            if type == "add":
                await user.add_roles(role)
            else:
                await user.remove_roles(role)

        if str(reaction.emoji) == "🚀":
            role = guild.get_role(1091490529511997440)
            if type == "add":
                await user.add_roles(role)     
            else:
                await user.remove_roles(role)






def setup(bot: commands.Bot):
    bot.add_cog(roleassignment(bot))