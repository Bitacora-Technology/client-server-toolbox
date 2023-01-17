from .tickets import Tickets
from bot import Bot


async def setup(bot: Bot) -> None:
    await bot.add_cog(Tickets(Bot))
