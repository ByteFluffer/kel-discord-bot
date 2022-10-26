from pydactyl import PterodactylClient
import os
from dotenv import load_dotenv

# Loading envirement keys
load_dotenv()

# Get Game_manager env keys
gamemanager_url = os.getenv("gamemanager_ptero_url")
gamemanager_client_password = os.getenv("client_api_key")

# Create a client to connect to the panel and authenticate with your API key.
api = PterodactylClient(gamemanager_url, gamemanager_client_password)

# Get a list of all servers
my_servers = api.client.servers.list_servers()

# Get the 4 server server by ID
srv_id = my_servers[3]["attributes"]["identifier"]

# Rebooting the individual server
api.client.servers.send_power_action(srv_id, "restart")