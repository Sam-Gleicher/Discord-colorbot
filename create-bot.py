import discord
#Set up token
from dotenv import load_dotenv
import os
import csv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TARGET_CHANNEL_ID = int(os.getenv('TARGET_CHANNEL_ID'))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

    channel = client.get_channel(TARGET_CHANNEL_ID)
    if not channel:
        print("❌ Channel not found — check the ID")
        await client.close()
        return

    # Open CSV file
    with open("colors.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Sender", "Colors"])

        # Fetch history (limit=None means all available)
        async for message in channel.history(limit=None, oldest_first=True):
            if message.author == client.user:
                continue  # skip bot messages
            if "," in message.content:
                colors = [c.strip() for c in message.content.split(",")]
                writer.writerow([message.created_at, message.author.name, ", ".join(colors)])

    print("💾 Finished writing colors.csv")
    await client.close()  # Exit after one run


client.run(TOKEN)