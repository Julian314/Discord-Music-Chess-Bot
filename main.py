import discord
from discord.ext import commands
import Music_Cog
import Chess_Cog

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.voice_states = True
bot = commands.Bot(command_prefix = '.', description='Development Bot', intents = intents)
music = Music_Cog.Music(bot)
chess = Chess_Cog.Chess(bot)

@bot.event
async def on_ready():
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))
    await bot.add_cog(music)
    await bot.add_cog(chess)

@bot.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is None:
        return
    if len(voice_state.channel.members) == 1:
        await voice_state.disconnect()
        music.leave = True
        del music.voice_states[member.guild.id]

with open('SendHelpPls/Schopp_Bot/token.txt', 'r') as file:
    TOKEN = file.read().strip()

bot.run(TOKEN)
