from discord.ext import commands
from discord import app_commands
import discord

from bot import Bot


class SendEmbedModal(discord.ui.Modal):
    def __init__(self, bot: Bot, channel: discord.TextChannel) -> None:
        super().__init__(
            title='Send Embed', timeout=None, custom_id='send-embed'
        )
        self.bot = bot
        self.channel = channel

    _title = discord.ui.TextInput(
        label='Title', style=discord.TextStyle.short
    )

    description = discord.ui.TextInput(
        label='Description', style=discord.TextStyle.long
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(
            title=self._title.value, description=self.description.value,
            color=self.bot.color
        )
        await interaction.response.send_message(
            f'Embed sent at <#{self.channel.id}>', ephemeral=True
        )
        await self.channel.send(embed=embed)


class Embed(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @app_commands.command(name='embed')
    async def send_embed(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ) -> None:
        """Send an embedded message to the selected text channel"""
        await interaction.response.send_modal(
            SendEmbedModal(self.bot, channel)
        )
