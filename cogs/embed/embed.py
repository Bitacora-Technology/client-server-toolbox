from discord.ext import commands
from discord import app_commands
import discord

from bot import Bot


class Embed(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @app_commands.command(name='embed')
    async def send_embed(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ) -> None:
        """Send an embedded message to the selected text channel"""
