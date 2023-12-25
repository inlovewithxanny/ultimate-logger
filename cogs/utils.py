import disnake
from disnake.ext import commands


class Utils(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        super().__init__()

    @commands.slash_command(name="message_info", description="Информация о сообщении", dm_permission=False)
    async def message_info(
            self,
            interaction: disnake.ApplicationCommandInteraction,
            message_id: commands.LargeInt = commands.Param(name="message_id", description="ID сообщения")
    ):
        await interaction.response.defer(ephemeral=True)

        message = self.bot.get_message(message_id)

        if not message:
            return await interaction.edit_original_response(
                content="**Сообщение не найдено**"
            )

        embed = disnake.Embed(
            title=f"Информация о сообщении",
            colour=message.author.roles[-1].colour,
            description=f"""\
**Сообщение:** {message.jump_url}
**Сообщение было отправлено:** <t:{int(message.created_at)}:f>
**Автор:** <@{message.author.id}>"""
        )

        return await interaction.edit_original_response(
            embed=embed
        )


def setup(bot: commands.InteractionBot):
    bot.add_cog(cog=Utils(bot=bot))
