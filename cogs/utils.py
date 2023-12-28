import disnake
from disnake.ext import commands

from ext.timeparser import parse_time
from datetime import timedelta
from asyncio import gather

import os
import aiofiles
from random import randint

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

    @commands.slash_command(name="clear", description="Очистить последние сообщения от пользователя", guild_ids=(355656045600964609,))
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

    @commands.slash_command(name="permissions", description="Посмотреть распределения прав доступа для канала", guild_ids=(355656045600964609,))
    @commands.has_permissions(manage_roles=True)
    async def permissions_view(
            self,
            interaction: disnake.ApplicationCommandInteraction,
            channel: disnake.abc.GuildChannel = commands.Param(name="channel", description="Канал")
    ):
        await interaction.response.defer(ephemeral=True)

        file_id = randint(1000000, 999999999)

        async with aiofiles.open(file=f"./tmp/permissions_overwrites_{file_id}.txt", mode="w", encoding="utf-8") as file:
            for k, v in channel.overwrites.items():
                if isinstance(k, disnake.Role):
                    await file.write(f"Переопределения прав для роли \"{k.name}\" ({k.id})\n\n")
                    await file.write(f"""\
Добавлять реакции: {v.add_reactions}
Прикреплять файлы: {v.attach_files}
Подключаться: {v.connect}
Создавать приглашения: {v.create_instant_invite}
Создавать приватные ветки: {v.create_private_threads}
Создавать публичные ветки: {v.create_public_threads}
Вставлять ссылки: {v.embed_links}
Использовать внешние эмодзи: {v.external_emojis}
Использовать внешние стикеры: {v.external_stickers}
Управлять каналом: {v.manage_channels}
Управлять сообщениями: {v.manage_messages}
Управлять правами: {v.manage_permissions}
Управлять ветками: {v.manage_threads}
Управлять вебхуками: {v.manage_webhooks}
Упоминать @everyone, @here и всех ролей: {v.mention_everyone}
Перемещать участников: {v.move_members}
Отключать участникам микрофон: {v.mute_members}
Приоритет в голосовом канале: {v.priority_speaker}
Читать историю сообщений: {v.read_message_history}
Читать сообщения: {v.read_messages}
Запрос на выступление (трибуна): {v.request_to_speak}
Отправлять сообщения: {v.send_messages}
Отправлять сообщения в ветках: {v.send_messages_in_threads}
Отправлять tts сообщения: {v.send_tts_messages}
Отправлять голосовые сообщения: {v.send_voice_messages}
Говорить: {v.speak}
Начинать активности: {v.start_embedded_activities}
Использовать внешние звуки: {v.use_external_sounds}
Использовать команды приложений: {v.use_application_commands}
Использовать звуковую панель: {v.use_soundboard}
Использовать активацию по голосу: {v.use_voice_activation}
Просматривать канал: {v.view_channel}\n\n""")

                elif isinstance(k, disnake.Member):
                    await file.write(f"Переопределения прав для пользователя \"{k.display_name}\" ({k.id})\n\n")
                    await file.write(f"""\
Добавлять реакции: {v.add_reactions}
Прикреплять файлы: {v.attach_files}
Подключаться: {v.connect}
Создавать приглашения: {v.create_instant_invite}
Создавать приватные ветки: {v.create_private_threads}
Создавать публичные ветки: {v.create_public_threads}
Вставлять ссылки: {v.embed_links}
Использовать внешние эмодзи: {v.external_emojis}
Использовать внешние стикеры: {v.external_stickers}
Управлять каналом: {v.manage_channels}
Управлять сообщениями: {v.manage_messages}
Управлять правами: {v.manage_permissions}
Управлять ветками: {v.manage_threads}
Управлять вебхуками: {v.manage_webhooks}
Упоминать @everyone, @here и всех ролей: {v.mention_everyone}
Перемещать участников: {v.move_members}
Отключать участникам микрофон: {v.mute_members}
Приоритет в голосовом канале: {v.priority_speaker}
Читать историю сообщений: {v.read_message_history}
Читать сообщения: {v.read_messages}
Запрос на выступление (трибуна): {v.request_to_speak}
Отправлять сообщения: {v.send_messages}
Отправлять сообщения в ветках: {v.send_messages_in_threads}
Отправлять tts сообщения: {v.send_tts_messages}
Отправлять голосовые сообщения: {v.send_voice_messages}
Говорить: {v.speak}
Начинать активности: {v.start_embedded_activities}
Использовать внешние звуки: {v.use_external_sounds}
Использовать команды приложений: {v.use_application_commands}
Использовать звуковую панель: {v.use_soundboard}
Использовать активацию по голосу: {v.use_voice_activation}
Просматривать канал: {v.view_channel}\n\n""")

        _file = disnake.File(fp=f"./tmp/permissions_overwrites_{file_id}.txt", filename="permissions.txt")

        await interaction.edit_original_response(
            content=f"Список распределений прав для канала {channel.mention}",
            file=_file
        )

        os.remove(f"./tmp/permissions_overwrites_{file_id}.txt")


def setup(bot: commands.InteractionBot):
    bot.add_cog(cog=Utils(bot=bot))
