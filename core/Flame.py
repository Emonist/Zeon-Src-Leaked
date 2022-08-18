import discord
from discord.ext import commands
import json
import os
import pymongo
os.system("pip install git+https://github.com/Pycord-Development/pycord")
os.system("pip install pymongo[srv]")
from cogs.ticket import createTicket, closeTicket
# ------------------------------ PREFIX AND INTENTS  -----------------------------------------

OWNER_IDS = [928125031991627816,871260709307158538,877922339382243328,918527734748164128,908723197862621218]
intents = discord.Intents.all()

# ------------------------------ DATABASE  -----------------------------------------
client = pymongo.MongoClient("mongodb+srv://hacker:chetan2004@cluster0.rxh8r.mongodb.net/Flame?retryWrites=true&w=majority")
db = client.get_database("Zeon").get_collection("servers")

# ------------------------------ CODE  -----------------------------------------
class Flame(commands.AutoShardedBot):
  def __init__(self) -> None:
    super().__init__(command_prefix=">", intents=intents, owner_ids=OWNER_IDS)
    self.persistent_views_added = False

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            self.load_extension(f'cogs.{filename[:-3]}')
    
  def run(self, version):
      self.VERSION = version
      with open('./ext/config.json') as f:
        self.config = json.load(f)
      super().run(self.config['token'], reconnect=True)

  async def on_ready(self) -> None:
    if not self.persistent_views_added:
        self.add_view(createTicket())
        self.add_view(closeTicket())
        self.persistent_views_added = True
    print(f'╭────˚♪°𝄞°♪˚─────╮\n{self.user.name} is online.\n╰────˚♪°𝄞°♪˚─────╯')
    await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"@{self.user.name}"))
    self.bot = bot
    bot.lavalink_nodes = [
    {"host": "losingtime.dpaste.org", "port": 2124, "password": "SleepingOnTrains"},
    # Can have multiple nodes here
]

# If you want to use spotify search
    bot.spotify_credentials = {
    'client_id': '6ad677e7f4344a9ebd7958e3d6fa3e56',
    'client_secret': '6405a1b768e841ca8a6cf542b8f24f1d'
}

    
  async def add_owner(self, user: discord.Member):
    OWNER_IDS.append(user)
    await user.send('<a:Ag_heedmode:958710180495908884> | You have been approved as the Co-Owner of Flame')


bot = Flame()

