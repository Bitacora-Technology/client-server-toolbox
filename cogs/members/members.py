from discord.ext import commands
import discord

from bot import Bot


class Members(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
