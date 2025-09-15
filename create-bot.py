import discord
#Set up token
from dotenv import load_dotenv
import os
import csv
import reader 
import re
import datetime  

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

    all_rows = []
    max_colors = 0

    # Fetch history
    async for message in channel.history(limit=None, oldest_first=True):
        if message.author == client.user:
            continue  # skip bot’s own messages
        if "," in message.content:
            colors = [c.strip() for c in message.content.split(",")]

            # Track max number of colors seen
            if len(colors) > max_colors:
                max_colors = len(colors)

            # Format date and time
            date = message.created_at.strftime("%Y-%m-%d")
            time = message.created_at.strftime("%H:%M")

            row = [message.author.name, date, time] + colors
            all_rows.append(row)

    # Write to CSV
    with open("colors.csv", "w", newline="") as f:
        writer = csv.writer(f)

        # Header: Sender, Date, Time, Color 1...Color N
        header = ["Sender", "Date", "Time"] + [f"Color {i+1}" for i in range(max_colors)]
        writer.writerow(header)

        # Pad shorter color lists with blanks
        for row in all_rows:
            row += [""] * (max_colors - (len(row) - 3))
            writer.writerow(row)

    print("💾 Finished writing colors.csv")
    await client.close()

    # Load crosswalk
    crosswalk = {}
    with open("crosswalk.csv", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            username = row["Username"].strip()
            real_name = row["Real Name"].strip()
            location = row["Location"].strip()
            crosswalk[username] = [real_name, location]

    # Write to CSV
    with open("colors_names.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Header: Username, Real Name, Location, Date, Time, Color 1...Color N
        header = ["Username", "Real Name", "Location", "Date", "Time"] + [
            f"Color {i+1}" for i in range(max_colors)
        ]
        writer.writerow(header)

        for row in all_rows:
            username = row[0]
            date = row[1]
            time = row[2]
            colors = row[3:]
            real_name, location = crosswalk.get(username, ("", ""))
            out_row = [username, real_name, location, date, time] + colors
            out_row += [""] * (max_colors - len(colors))
            writer.writerow(out_row)
            
    print("💾 Finished writing colors_names.csv")

client.run(TOKEN)