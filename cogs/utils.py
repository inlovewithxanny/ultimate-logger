import disnake
from disnake.ext import commands

from ext.timeparser import parse_time
from datetime import timedelta
from asyncio import gather


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
**Сообщение было отправлено:** <t:{int(message.created_at.timestamp())}:f>
**Автор:** <@{message.author.id}>"""
        )

        return await interaction.edit_original_response(
            embed=embed
        )

    @commands.slash_command(name="clear", description="Очистить последние сообщения от пользователя", dm_permission=False, guild_ids=(355656045600964609,))
    # @commands.has_permissions(disnake.Permissions.manage_messages)
    @commands.is_owner()
    async def clear_messages(
            self,
            interaction: disnake.ApplicationCommandInteraction,
            member: disnake.Member = commands.Param(name="user", description="Пользователь"),
            time: str = commands.Param(name="time", description="Время, за которое нужно очистить. Максимум 5 минут"),
            reason: str = commands.Param(name="reason", description="Причина"),
    ):
        await interaction.response.defer(ephemeral=True)

        try:
            endtime, time_delta, endtime_str = parse_time(input_time=time, time_type="backwards")
        except ValueError:
            return await interaction.edit_original_response(
                content="**Неподдерживаемый тип времени. Поддерживаются типы: 's', 'm', 'h', 'd'.**"
            )

        if member.roles[-1].position >= interaction.author.roles[-1].position:
            tasks = [
                interaction.edit_original_response(
                    content="**Вы не можете очистить сообщения от человека, чья высшая роль выше вашей высшей роли.**\n"
                            "**Об этом несанкционированном действии было доложено, ждите небесной кары.**"
                )
            ]

            debug_channel = self.bot.get_channel(797908325361516545)

            tasks.append(
                debug_channel.send(
                    content=f"<@{interaction.author.id}> `{interaction.author.display_name}` попытался очистить сообщения за последние "
                            f"`{endtime_str}` в канале <#{interaction.channel_id}> `{interaction.channel.name}` от пользователя "
                            f"<@{member.id}> `{member.display_name}` с причиной `{reason}`.\n"
                            f"||<@922866312328380437>||"
                )
            )

            return await gather(*tasks)



def setup(bot: commands.InteractionBot):
    bot.add_cog(cog=Utils(bot=bot))
