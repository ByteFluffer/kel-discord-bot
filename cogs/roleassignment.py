import disnake
from disnake.ext import commands, tasks
from env import *
from database import Database


class roleassignment(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.REACTION_ONE = 1091779444626178209
        self.VERIFY = 1092028079800582235

    # Listening to reactions added
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        
        guild = await self.bot.fetch_guild(1002208148930691172)
        user = await guild.fetch_member(reaction.user_id)

        # Reaction role one
        if reaction.message_id == self.REACTION_ONE:
            type= "add"
            await self.reaction_roles_one(guild, user, reaction, type)
        
        # Verify reaction
        if reaction.message_id == self.VERIFY:
            type= "add"
            await self.reaction_verify(guild, user, reaction, type)



    # Listening to reactions removed
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction):
        
        guild = await self.bot.fetch_guild(1002208148930691172)
        user = await guild.fetch_member(reaction.user_id)

        # Reaction role one
        if reaction.message_id == self.REACTION_ONE:
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
                await roleassignment.send_dm_for_role(self, user, type, role.name)
            else:
                await user.remove_roles(role)
                await roleassignment.send_dm_for_role(self, user, type, role.name)

        if str(reaction.emoji) == "🚀":
            role = guild.get_role(1091490529511997440)

            if type == "add":
                await user.add_roles(role)     
                await roleassignment.send_dm_for_role(self, user, type, role.name)
            else:
                await user.remove_roles(role)
                await roleassignment.send_dm_for_role(self, user, type, role.name)



    async def reaction_verify(self, guild, user, reaction, type):

        if str(reaction.emoji) == "✅":
            role = guild.get_role(1090649616933994516)

            if type == "add":
                await user.add_roles(role)
                await roleassignment.send_dm_for_role(self, user, type, role.name)



    # Sending dm if user adds or removes a role
    async def send_dm_for_role(self, user, type, role):
        print("Debug send_dm_for_role")
        user = self.bot.get_user(user.id)
        if str(type) == "add":
            print(f"Added role {role} to user {user}" )
            await user.send(f"I added a role with the name '{role}'.")
            return
        else:
            print(f"Removed role {role} to user {user}" )
            await user.send(f"I removed a role with the name '{role}'.")
            return

def setup(bot: commands.Bot):
    bot.add_cog(roleassignment(bot))