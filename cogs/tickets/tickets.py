from discord.ext import commands
import discord

from bot import Bot


class Tickets(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
