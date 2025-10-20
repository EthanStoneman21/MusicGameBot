import discord
import os
from dotenv import load_dotenv

#load token
load_dotenv()
token = os.getenv("DISCORD_TOKEN")

song = "b"
artist = "b"

guesses = {1429642609177006080}
leaderboard = {1429645537635991583}

class MyClient(discord.Client):
    def __init__ (self, *, intents):
        super().__init__(intents = intents)
        self.winner_declared = False
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self,message):
        #Prevent bot from replying to itself
        if message.author == self.user:
            return

        #react if song is correct
        if message.channel.id in guesses:
            guess_parts = message.content.lower().split(" by ")
            if len(guess_parts) == 2:
                guessed_song = guess_parts[0].strip()
                guessed_artist = guess_parts[1].strip()
                if guessed_song == song.lower() and guessed_artist == artist.lower():
                    await message.add_reaction("✅")
                    if not self.winner_declared:
                        self.winner_declared = True

                        #update leaderboard
                        leader_channel = self.get_channel(list(leaderboard)[0])
                        leader_message = await leader_channel.fetch_message(1429868226556465172)

                        user_tag = message.author.mention
                        lines = leader_message.content.splitlines()
                        new_lines = []
                        updated = False

                        for line in lines:
                            if line.startswith(user_tag):
                                try:
                                    count = int(line.split(":")[1].strip())
                                except ValueError:
                                    count = 0
                                new_lines.append(f"{user_tag}: {count + 1}")
                                updated = True
                            else:
                                new_lines.append(line)
                        if not updated:
                            new_lines.append(f"{user_tag}: 1")

                        new_content = "\n".join(new_lines)
                        await leader_message.edit(content=new_content)

                elif guessed_artist == artist.lower():
                    await message.add_reaction("🟦")



intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)