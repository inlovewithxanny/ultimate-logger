import disnake
from disnake.ext import commands


class DeveloperCommands(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        super().__init__()
        self.bot = bot


def setup(bot: commands.InteractionBot):
    bot.add_cog(cog=DeveloperCommands(bot=bot))
