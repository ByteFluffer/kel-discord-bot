
import disnake
from disnake.ext import commands, tasks
from env import *
from database import Database
#         levelxpcap = int(8.196 * pow(level + 1, 2.65) + 200)


class roleassignment(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    

    # Mother command
    @commands.default_member_permissions(moderate_members=True)
    @commands.slash_command()
    async def reaction_roles(self, inter):
        pass


    # Adding a message to reaction roles
    @reaction_roles.sub_command(description="Add a reaction role to a excisting message")
    async def add(self, inter, msg_id, emoji_one= None, emoji_two= None, emoji_three= None, emoji_four= None, emoji_five= None):
        msg = await inter.channel.fetch_message(msg_id)
        print(emoji_one)
        
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

        content = '🥳🥳 Content to be save in 🥳🥳 Database 🥳🥳'
        encoded_content = content.encode('unicode-escape').decode('ASCII')             


        try:
            Database.cursor.execute(f"INSERT INTO reaction_roles (msg_id, emoji_one, emoji_two, emoji_three, emoji_four, emoji_five) VALUES ('{msg_id}', '{emoji_one}', '{emoji_two}', '{emoji_three}', '{emoji_four}', '{emoji_five}')")
            Database.db.commit()
        except Exception as error:
            print(error)

        await inter.response.send_message("Done!", ephemeral=True)

    
    # Adding a message to reaction roles
    @reaction_roles.sub_command(description="Add a reaction role to a excisting message")
    async def test(self, inter):
        emoji = "🥺"
        #encoded_content = emoji.encode('unicode-escape').decode('ASCII')
        Database.cursor.execute(f"INSERT INTO reaction_roles (msg_id, emoji_one) VALUES ('69', '{emoji}')")
        Database.db.commit()
        #emoji_one = "U0001f97a"
        # = bytes(emoji_one, 'utf-8')
        #original_content = c.decode('unicode-escape')
        await inter.response.send_message(emoji)


def setup(bot: commands.Bot):
    bot.add_cog(roleassignment(bot))