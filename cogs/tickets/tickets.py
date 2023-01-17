from discord.ext import commands
from discord import app_commands
import discord

from bot import Bot


@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
class Tickets(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
