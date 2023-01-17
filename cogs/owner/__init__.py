from .owner import Owner
from bot import Bot


async def setup(bot: Bot) -> None:
    await bot.add_cog(Owner(Bot))
