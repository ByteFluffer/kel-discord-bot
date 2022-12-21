import disnake
from disnake.ext import commands
from disnake.enums import ButtonStyle
from database import Database
import matplotlib.pyplot as plt
import numpy as np
import os

# Cog class
class analytics(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Mother Off All Commands
        @bot.slash_command()
        async def analyze(inter):
            pass


        # 'aantal_entrys' slash command
        @analyze.sub_command(description="Krijg de entry count te zien!")
        async def aantal_entrys(inter):
            # Getting the row count and sending message to Discord
            result = total_rows_in_db()

            await inter.response.send_message(f"Totaal aantal entry's: {result}", ephemeral=True)


        # 'woord' slash command
        @analyze.sub_command(description="Komt nog")
        async def woord(inter):
            await plt_make_word_count()
            # Sending plot from 'plt_make_word_count'

            with open('author_msg_count.png', 'rb') as fp:
                await inter.response.send_message(file=disnake.File(fp, 'author_msg_count.png'), ephemeral=True)


        # 'kanalen_graph' slash command
        @analyze.sub_command(description="Krijg een graph van de populairste kanalen te zien")
        async def kanalen_graph(inter):
            # Getting populair channels and sending it
            result = await channel_populair_this_month()
            # Sending plot from 'channel_populairity'
            with open('channel_populairity_this_month.png', 'rb') as fp:
                await inter.response.send_message(file=disnake.File(fp, 'channel_populairity_this_month.png'), ephemeral=True)


        # 'tijd_polulair' slash command
        @analyze.sub_command(description="Krijg een graph van de polpulairste tijden te zien deze maand!")
        async def tijd_polulair(inter):
            # Getting populair channels and sending it
            result = await time_populair_this_month()
            # Sending plot from 'channel_populairity'
            #with open('channel_populairity_this_month.png', 'rb') as fp:
            #    await inter.response.send_message(file=disnake.File(fp, 'channel_populairity_this_month.png'), ephemeral=True)





        
        # Defining stuff
        # 'aantal_entrys' command code
        def total_rows_in_db():
                Database.cursor.execute("SELECT COUNT(*) FROM analytics")
                return Database.cursor.fetchall()[0][0]



        # 'woord' command code
        async def plt_make_word_count():
                # Gets by author the top 10 with most word count
                Database.cursor.execute("SELECT msg_author, msg_word_count FROM analytics ORDER BY msg_word_count DESC")
                author_msg_word_count = Database.cursor.fetchall()

                # Temporary data storage
                data_msg_word_count = {}
                sorted_data_msg_word_count = {}

                # Looping trough entrys, adds username and word-count to above
                for entry in author_msg_word_count:

                    # Getting username from guild
                    username_guild = (await bot.get_or_fetch_user(entry[0])).name
                    if username_guild not in data_msg_word_count.keys():
                        data_msg_word_count[f'{username_guild}'] = entry[1]
                    else:
                        data_msg_word_count[f'{username_guild}'] = data_msg_word_count.get(f'{username_guild}') + entry[1]

                # Sorting 'data_msg_word_count'
                sorted_data_msg_word_count = dict(sorted(data_msg_word_count.items(), key=lambda item: item[-1], reverse=True))

                # Making graph:
                fig = plt.figure(figsize=(10, 5))
                plt.bar(list(sorted_data_msg_word_count.keys())[:5], list(sorted_data_msg_word_count.values())[:5], color="maroon",width=0.4)
                plt.xlabel("Users"), plt.ylabel("Word count")
                plt.title("Top 5 users with the highest word count this month")
                plt.savefig("author_msg_count.png")

                # Clearing stuffies
                data_msg_word_count.clear() and sorted_data_msg_word_count.clear()
                


        # 'kanalen_graph' code
        async def channel_populair_this_month():
            Database.cursor.execute("SELECT * from analytics")
            result = Database.cursor.fetchall()

            channel_data_not_sorted = {}
            channel_data_sorted = {}
            for entry in result:
                if str(bot.get_channel(entry[3])) not in channel_data_not_sorted.keys():
                    channel_data_not_sorted[f'{bot.get_channel(entry[3])}'] = 1
                else:
                    channel_data_not_sorted[f'{bot.get_channel(entry[3])}'] = channel_data_not_sorted.get(f'{bot.get_channel(entry[3])}') + 1

            channel_data_sorted = dict(sorted(channel_data_not_sorted.items(), key=lambda item: item[-1], reverse=True))

            # Making graph:
            fig = plt.figure(figsize=(10, 5))
            plt.bar(list(channel_data_sorted.keys())[:5], list(channel_data_sorted.values())[:5], color="maroon",width=0.4)
            plt.xlabel("Channels"), plt.ylabel("Total messages")
            plt.title("Top 5 channels with the highest message count this month")
            plt.savefig("channel_populairity_this_month.png")

            # Clearing stuffies
            channel_data_not_sorted.clear() and channel_data_sorted.clear()
            


        async def time_populair_this_month():
            Database.cursor.execute("SELECT msg_time FROM analytics")
            result = Database.cursor.fetchall()
            fig, ax = plt.subplots(figsize=(8, 6))
            
            #ax.plot(date, value);

            print(result)


def setup(bot: commands.Bot):
    bot.add_cog(analytics(bot))
