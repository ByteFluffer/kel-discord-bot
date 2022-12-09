import disnake
from disnake.ext import commands

# EMBED colors
EMBED_DANGER = 0xFF0000
EMBED_GOOD = 0x00FF00
EMBED_ORANGE = 0xFFA500

intents = disnake.Intents.all()
bot = commands.Bot(intents=intents)

def webhook_uptime_handling(data):
    embed=disnake.Embed(title="Uptime change!", description="Name: " + str(data["monitor"]["name"]), color=EMBED_GOOD)
    if data ["heartbeat"]["status"] == 0:
        status = "Down"
    else:
        status = "Up"
    embed.add_field(name="Status:", value=status, inline=False)
    embed.add_field(name="Message:", value=data["heartbeat"]["msg"], inline=False)
    embed.set_footer(text = "Made by KelvinCodes", icon_url = "https://itkelvin.nl/CustomCPULOGO.png")

    return embed

def webhook_github_handling(type, data):
    print("DEBUG: ", data)
    if type == "issue":
        embed=disnake.Embed(title="GitHub issue", description="Repository: " + str(data["repository"]["name"]), color=EMBED_GOOD)
        print(data)
        embed.add_field(name="Type:", value=data["action"], inline=False)
        embed.add_field(name="Title:", value=data["issue"]["title"], inline=False)
        embed.add_field(name="Issue text:", value=data["comment"]["body"], inline=False)
        embed.set_footer(text = "Made by KelvinCodes", icon_url = "https://itkelvin.nl/CustomCPULOGO.png")

    elif type == "pull":
        embed=disnake.Embed(title="GitHub pull", description="Repository: " + str(data["repository"]["name"]), color=EMBED_GOOD)
        print(data)
        #embed.add_field(name="Type:", value=type, inline=False)
        #embed.add_field(name="Title:", value=data["issue"]["title"], inline=False)
        #embed.add_field(name="Issue text:", value=data["comment"]["body"], inline=False)
        embed.set_footer(text = "Made by KelvinCodes", icon_url = "https://itkelvin.nl/CustomCPULOGO.png")

    elif type == "push":
        embed=disnake.Embed(title="GitHub push", description="Repository: " + str(data["repository"]["name"]), color=EMBED_GOOD)
        print(data)
        #embed.add_field(name="Type:", value=type, inline=False)
        #embed.add_field(name="Title:", value=data["issue"]["title"], inline=False)
        #embed.add_field(name="Issue text:", value=data["comment"]["body"], inline=False)
        embed.set_footer(text = "Made by KelvinCodes", icon_url = "https://itkelvin.nl/CustomCPULOGO.png")

    return embed

def webhook_server_login_handling(data):
    print(data)
    for key in data:
        if key == "server_login_content":
            data_splitted = data['server_login_content'].split()
            embed=disnake.Embed(title=f"Server login!", description="Server: " + str(data_splitted[2]) , color=EMBED_GOOD)
            embed.add_field(name="User:", value=data_splitted[0], inline=False)
            embed.add_field(name="IP:", value=data_splitted, inline=False)
        else:
            data_splitted = data['server_logout_content'].split()
            embed=disnake.Embed(title=f"Server log-out!", description="Server: " + str(data_splitted[2]) , color=EMBED_GOOD)
            embed.add_field(name="User:", value=data_splitted[0], inline=False)
            embed.add_field(name="IP:", value=data_splitted[1], inline=False)            

    embed.set_footer(text = "Made by KelvinCodes", icon_url = "https://itkelvin.nl/CustomCPULOGO.png")

    return embed