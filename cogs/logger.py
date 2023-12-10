import disnake
from disnake.ext import commands

from ext.database.methods import *

from datetime import datetime

from aiohttp import ClientSession


class Logger(commands.Cog):
    def __init__(self, bot: commands.InteractionBot):
        super().__init__()
        self.bot = bot

    @commands.Cog.listener(name=disnake.Event.audit_log_entry_create)
    async def log_role(self, entry: disnake.AuditLogEntry):
        if not entry.action == disnake.AuditLogAction.member_role_update:
            return

        guild = await get_guild(discord_id=entry.guild.id)

        if not guild:
            return
        elif not guild.roles_log_webhook:
            return

        if entry.user.bot:
            description = f"Роли <@{entry.target.id}> были обновлены ботом <@{entry.user.id}>"
            ids = f"""\
```js
User = {entry.target.id}
Perpetrator = {entry.user.id} [BOT]
```"""
        else:
            description = f"Роли <@{entry.target.id}> были обновлены модератором <@{entry.user.id}>"
            ids = f"""\
```js
User = {entry.target.id}
Perpetrator = {entry.user.id}
```"""

        changes = ""

        colour = (entry.before.roles[0] if not len(entry.before.roles) == 0 else entry.after.roles[0]).colour

        taken_role: disnake.Role
        for taken_role in entry.before.roles:
            changes += f"> **`-` {taken_role.name} `[{taken_role.id}]`**\n"

        given_role: disnake.Role
        for given_role in entry.after.roles:
            changes += f"> **`+` {given_role.name} `[{given_role.id}]`**\n"

        embed = disnake.Embed(
            colour=colour,
            timestamp=datetime.now(),
            description=description,
        )

        embed.set_author(name=str(entry.target), icon_url=entry.target.display_avatar.url)
        embed.set_footer(text=str(entry.user), icon_url=entry.user.display_avatar.url)

        embed.add_field(name="Изменения", value=changes, inline=False)

        if entry.reason:
            embed.add_field(name="Причина", value=f"> **{entry.reason}**", inline=False)

        embed.add_field(name="ID", value=ids, inline=False)

        async with ClientSession() as session:
            webhook = disnake.Webhook.from_url(url=str(guild.roles_log_webhook), session=session)
            return await webhook.send(
                username="Ultimate Logger | Роли",
                avatar_url=self.bot.user.display_avatar.url,
                embed=embed
            )


def setup(bot: commands.InteractionBot):
    bot.add_cog(cog=Logger(bot=bot))
