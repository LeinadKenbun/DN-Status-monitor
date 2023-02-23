import discord
import asyncio
import socket
import os

# Define the server and port to check
SERVER = os.getenv("SERVER")
PORT = int(os.getenv("PORT"))

# Define the Discord bot token and channel ID
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# Create a Discord client object
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# Define a function to ping the server using TCP
async def ping_server():
    while True:
        try:
            # Create a TCP socket and attempt to connect to the server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER, PORT))
            s.close()

            # If the connection succeeded, update the server status and send an embedded message to Discord
            server_status = "up"
            await send_embed(client, CHANNEL_ID, server_status)

        except Exception:
            # If the connection failed, update the server status and send an embedded message to Discord
            server_status = "down"
            await send_embed(client, CHANNEL_ID, server_status)

        # Wait for 5 minutes before checking the server again
        await asyncio.sleep(300)

# Define a function to send an embedded message to Discord
async def send_embed(client, channel_id, status):
    channel = client.get_channel(channel_id)
    embed = discord.Embed(title="Server Status", description="The server is currently " + status + ".")
    if status == "up":
        embed.colour = discord.Colour.green()
    else:
        embed.colour = discord.Colour.red()
    message = await channel.send(embed=embed)

    # Store the message ID in a file for later updates
    with open("message_id.txt", "w") as f:
        f.write(str(message.id))

# Define an event handler for when the client is ready
@client.event
async def on_ready():
    print("Logged in as", client.user.name)
    # Load the message ID from the file
    with open("message_id.txt", "r") as f:
        message_id = int(f.read())
    # Send an initial embedded message to Discord
    server_status = "up"
    await send_embed(client, CHANNEL_ID, server_status)

# Define a function to update the embedded message in Discord
async def update_embed(client, channel_id, message_id, status):
    channel = client.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    embed = message.embeds[0]
    embed.description = "The server is currently " + status + "."
    if status == "up":
        embed.colour = discord.Colour.green()
    else:
        embed.colour = discord.Colour.red()
    await message.edit(embed=embed)



# Define the asynchronous main function
async def main():
    # Start the Discord bot and ping the server
    await client.start(TOKEN)
    await ping_server()

# Run the main function using asyncio
if __name__ == "__main__":
    asyncio.run(main())
