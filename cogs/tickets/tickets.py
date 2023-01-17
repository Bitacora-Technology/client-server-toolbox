from discord.ext import commands
from discord import app_commands
import discord

from bot import Bot


class OpenTicketButton(discord.ui.Button):
    def __init__(self, bot: Bot) -> None:
        super().__init__(emoji='🎯', custom_id='open-ticket')

    async def callback(self, interaction: discord.Interaction) -> None:
        user = interaction.user
        user_name = user.name
        user_discriminator = user.discriminator
        channel_name = f'{user_name}-{user_discriminator}'

        default_role = interaction.guild.default_role
        permissions = {
            default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True)
        }

        guild = interaction.guild
        category = discord.utils.get(guild.categories, name='Tickets')

        content = (
            'Thanks for reaching out, <@{}>! We will assist '
            'you as soon as we are available.'
        ).format(user.id)
        channel = await guild.create_text_channel(
            channel_name, category=category, overwrites=permissions
        )
        await channel.send(content)

        content = f'You can find your ticket at <#{channel.id}>'
        await interaction.response.send_message(content, ephemeral=True)


class TicketPanelView(discord.ui.View):
    def __init__(self, bot: Bot) -> None:
        super().__init__(timeout=None)
        self.add_item(OpenTicketButton(bot))


@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
class Tickets(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    def panel_embed(self) -> discord.Embed:
        description = 'Click the button below to open a new ticket.'
        embed = discord.Embed(
            title='Ticket Panel', description=description, color=self.bot.color
        )
        return embed

    @app_commands.command(name='panel')
    async def send_panel(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ) -> None:
        """Send a ticket panel to the selected text channel"""
        embed = self.panel_embed()
        view = TicketPanelView(self.bot)
        await channel.send(embed=embed, view=view)
        content = f'Panel created at <#{channel.id}>'
        await interaction.response.send_message(content, ephemeral=True)
