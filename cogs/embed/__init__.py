from .embed import Embed
from bot import Bot


async def setup(bot: Bot) -> None:
    await bot.add_cog(Embed(bot))
