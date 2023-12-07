import disnake
from disnake.ext import commands

from ext.models.checks import is_guild_admin
from ext.database.methods import *

from aiohttp import ClientSession


class DeveloperCommands(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        super().__init__()
        self.bot = bot

    @commands.slash_command(name="dev", description="[DEV] Команды разработчиков")
    @is_guild_admin()
    async def dev(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @dev.sub_command_group(name="guild", description="[DEV] Управление серверами")
    async def dev_guild(self, interaction: disnake.ApplicationCommandInteraction):
        pass

    @dev_guild.sub_command(name="register", description="[DEV] Зарегистрировать сервер")
    async def dev_guild_register(
            self,
            interaction: disnake.ApplicationCommandInteraction,
            guild_id: commands.LargeInt = commands.Param(name="guild_id", description="Discord ID сервера")
    ):
        await interaction.response.defer()

        await add_guild(discord_id=guild_id)

        return await interaction.edit_original_response(
            content="**Сервер успешно зарегистрирован**"
        )

    @dev_guild.sub_command(name="setlogchannel_roles", description="[DEV] Установить канал для логирования ролей")
    async def dev_guild_set_log_channel_roles(
            self,
            interaction: disnake.ApplicationCommandInteraction,
            guild_id: commands.LargeInt = commands.Param(name="guild_id", description="Discord ID сервера"),
            channel_id: commands.LargeInt = commands.Param(name="channel_id", description="Discord ID канала"),
    ):
        await interaction.response.defer()

        guild = self.bot.get_guild(guild_id)

        if not guild:
            return await interaction.edit_original_response(
                content="**Произошла ошибка, сервер не найден. Возможно бот не является участником сервера или вы ошиблись в ID.**"
            )

        guild_in_database = await get_guild(discord_id=guild_id)

        if not guild_in_database:
            return await interaction.edit_original_response(
                content="**Сервер не зарегистрирован в базе данных.**"
            )

        channel = guild.get_channel(channel_id)

        if not channel:
            return await interaction.edit_original_response(
                content="**Произошла ошибка, не удалось найти канал с указаным ID.**"
            )

        if guild_in_database.roles_log_webhook:
            async with ClientSession() as session:
                old_webhook = disnake.Webhook.from_url(url=str(guild_in_database.roles_log_webhook), session=session)
                await old_webhook.delete(reason="Переназначение канала")

            await update_guild(discord_id=guild_id, column_name="roles_log_webhook", value=None)

        webhook = await channel.create_webhook(name="Ultimate Logger | Роли", reason="Назначение канала для логов")

        await update_guild(discord_id=guild_id, column_name="roles_log_webhook", value=webhook.url)

        return await interaction.edit_original_response(
            content=f"**Канал `{channel.name} [{channel_id}]` успешно установлен для логирования ролей на сервере `{guild.name}`.**"
        )




def setup(bot: commands.InteractionBot):
    bot.add_cog(cog=DeveloperCommands(bot=bot))
