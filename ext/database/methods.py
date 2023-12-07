from typing import Literal

from sqlalchemy import select

from ext.database.database import SessionLocal
from ext.database.models import *


async def add_guild(discord_id: int) -> None:
    guild = Guild(discord_id=discord_id)

    async with SessionLocal() as session:
        session.add(guild)
        return await session.commit()


async def get_guild(discord_id: int) -> Guild:
    async with SessionLocal() as session:
        result = await session.execute(select(Guild).filter_by(discord_id=discord_id))
        return result.scalar()


async def get_all_guilds() -> list[Guild]:
    async with SessionLocal() as session:
        result = await session.execute(select(Guild))
        return result.scalars().all()


async def update_guild(
        discord_id: int,
        column_name: Literal[
            "id",
            "discord_id",
            "roles_log_webhook",
            "is_admin_guild",
            "is_active",
        ],
        value
) -> None:
    async with SessionLocal() as session:
        result = await session.execute(select(Guild).filter_by(discord_id=discord_id))
        if result:
            guild = result.scalar()
            setattr(guild, column_name, value)
            await session.commit()