import discord
#Set up token
from dotenv import load_dotenv
import os
import csv
import glob

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GRAPH_CHANNEL_ID = int(os.getenv('GRAPH_CHANNEL_ID'))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    
    channel = client.get_channel(GRAPH_CHANNEL_ID)
    if not channel:
        print("❌ Channel not found")
        await client.close()
        return
    
    # Find all PNG files in current directory
    png_files = glob.glob("*.png")
    
    if not png_files:
        print("No PNG files found")
        await client.close()
        return
    
    # Upload each PNG file
    for png_file in png_files:
        with open(png_file, 'rb') as f:
            file = discord.File(f, filename=png_file)
            await channel.send(file=file)
            print(f"✅ Uploaded {png_file}")
    
    print("All files uploaded!")
    await client.close()

client.run(TOKEN)