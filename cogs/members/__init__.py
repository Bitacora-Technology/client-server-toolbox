from .members import Members
from bot import Bot


async def setup(bot: Bot) -> None:
    await bot.add_cog(Members(bot))
