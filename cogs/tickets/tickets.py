from discord.ext import commands
from discord import app_commands
import discord
import os

from bot import Bot


class CloseTicketButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(emoji='📕', custom_id='close-ticket')

    async def callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer(thinking=True)

        folder_path = f'{os.getcwd()}/tickets/'
        if os.path.exists(folder_path) is False:
            os.mkdir(folder_path)

        file_name = f'transcript-{interaction.channel.name}.txt'
        with open(folder_path + file_name, 'w+') as file_txt:
            history = interaction.channel.history(
                limit=None, oldest_first=True
            )
            async for message in history:
                created_at = message.created_at
                timestamp = f'[{created_at.date()} {created_at.time()}]'

                author = message.author
                name = f'[{author.name}#{author.discriminator}]'

                content = f'{timestamp} {name} {message.content}'
                file_txt.write(content)

        with open(folder_path + file_name) as file_txt:
            members = interaction.channel.members
            for member in members:
                try:
                    await member.send(
                        file=discord.File(file_txt, file_name)
                    )
                except Exception:
                    pass
            os.remove(file_txt.name)

        await interaction.channel.delete()


class CloseTicketView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.add_item(CloseTicketButton())


class OpenTicketButton(discord.ui.Button):
    def __init__(self) -> None:
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
        channel = await guild.create_text_channel(
            channel_name, category=category, overwrites=permissions
        )

        content = (
            'Thanks for reaching out, <@{}>! We will assist '
            'you as soon as we are available.\nClick the button '
            'bellow to close the current ticket.'
        ).format(user.id)
        view = CloseTicketView()
        await channel.send(content, view=view)

        content = f'You can find your ticket at <#{channel.id}>'
        await interaction.response.send_message(content, ephemeral=True)


class TicketPanelView(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.add_item(OpenTicketButton())


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
        view = TicketPanelView()
        await channel.send(embed=embed, view=view)
        content = f'Panel created at <#{channel.id}>'
        await interaction.response.send_message(content, ephemeral=True)

    @app_commands.command(name='add')
    async def add_member(
        self, interaction: discord.Interaction, member: discord.Member
    ) -> None:
        """Add a new member to the current ticket"""
        await interaction.channel.set_permissions(member, view_channel=True)
        content = f'Member <@{member.id}> has been added to the ticket'
        await interaction.response.send_message(content)
