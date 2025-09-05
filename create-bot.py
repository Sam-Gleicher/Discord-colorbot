import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTQxMzUxMjY3MDE3NDI1MzA2OA.GHNpLT.VVIP_coS5iOAmdkMUTVo5iT8PfufIg18UdxgWU')
