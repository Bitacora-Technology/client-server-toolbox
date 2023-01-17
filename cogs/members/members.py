from discord.ext import commands
import discord

from bot import Bot


class Members(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    def arrival_embed(self, member: discord.Member) -> discord.Embed:
        embed = discord.Embed(title='New Arrival', color=self.bot.color)
        member_name = f'{member.name}#{member.discriminator}'
        embed.add_field(name='Member', value=member_name, inline=False)
        embed.add_field(name='Identifier', value=member.id, inline=False)
        embed.set_thumbnail(url=member.avatar)
        return embed

    @commands.Cog.listener(name='on_member_join')
    async def member_arrival(self, member: discord.Member) -> None:
        text_channels = member.guild.text_channels
        channel = discord.utils.get(text_channels, name='arrivals')
        if not channel:
            return
        embed = self.arrival_embed(member)
        await channel.send(embed=embed)
