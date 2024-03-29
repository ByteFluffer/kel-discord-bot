
import disnake
from disnake.ext import commands, tasks
from env import *
from database import Database
#         levelxpcap = int(8.196 * pow(level + 1, 2.65) + 200)


class leveling(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Starting tasks
        self.scoreboard_loop.start()



    # On message 
    @commands.Cog.listener()
    async def on_message(self, message):
        # Leveling
        if not message.author.bot:
            # If user id isn't in the list, add it
            if message.author.id not in self.list_users:
                self.list_users.append(message.author.id)
                print(self.list_users)




    list_users = []
    @tasks.loop(seconds=60) 
    async def scoreboard_loop(self):
        XP = 5

        for user in self.list_users:
            leveling.set_xp(self, user, XP)
        
        # Clearing list
        self.list_users.clear()



                
    # Check if user is in database
    def validate_user(id):
        Database.cursor.execute(f"SELECT * FROM scoreboard WHERE user_id = {id} LIMIT 1")
        res = Database.cursor.fetchone()
        if res == None or res == []:
            return False
        else:
            return True


    # Getting user XP:
    def get_xp(id):
        Database.cursor.execute(f"SELECT xp from scoreboard WHERE user_id = {id} LIMIT 1")
        res = Database.cursor.fetchone()[0]
        return res
    

    # Setting xp
    def set_xp(self, user, XP):
        if leveling.validate_user(user) != False:
            
            get_xp = leveling.get_xp(id=user)
            get_level = leveling.get_level(user)

            Database.cursor.execute(f"UPDATE scoreboard SET xp = {int(get_xp) + XP} WHERE user_id = {user}")
            Database.db.commit()

            if get_xp > int(8.196 * pow(int(get_level) + 1, 2.65) + 200):
                level = get_level + 1
                #self.bot.loop.create_task(leveling.level_embed(self, level, user))
                print(f"User {user} has reached level {level}")
            leveling.set_level(level, user)

            print(f"User {user} gained xp: {int(get_xp) + XP}")
        else:
            Database.cursor.execute(f"INSERT INTO scoreboard (user_id, xp, level) VALUES ({int(user)}, {XP}, 0)")
            Database.db.commit()
            print(f"User {user} gained xp: 7")


    # Get user level
    def get_level(id):
        Database.cursor.execute(f"SELECT level FROM scoreboard WHERE user_id={id} LIMIT 1")
        res = Database.cursor.fetchone()[0]
        if res == None or res == []:
            return 0
        else:
            return res
    
    
    # Level message
    async def level_embed(self, level, user):
        user = await self.bot.get_or_fetch_user(int(user))
        embed=disnake.Embed(title=f"User has leveled up!", description=f"{user.mention}", color=disnake.Color.red())
        embed.add_field(name=f"Level:", value=level, inline=False)
        channel_to_send = self.bot.get_channel(ChannelIDs.KELVINCODES_CHANNEL)
        await channel_to_send.send(embed=embed)


    # Setting user level
    def set_level(level_to_set, id):
        Database.cursor.execute(f"UPDATE scoreboard SET level = {level_to_set} WHERE user_id = {id}")
        Database.db.commit()




def setup(bot: commands.Bot):
    bot.add_cog(leveling(bot))