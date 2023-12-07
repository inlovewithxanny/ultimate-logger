from sqlalchemy import BigInteger, Text
from sqlalchemy.orm import Mapped, mapped_column
from ext.database.database import Base


class Guild(Base):
    __tablename__ = "guilds"

    id: Mapped[int] = mapped_column(primary_key=True)
    discord_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    roles_log_webhook: Mapped[str] = mapped_column(Text(), nullable=True)
    is_admin_guild: Mapped[bool] = mapped_column(server_default="0")
    is_active: Mapped[bool] = mapped_column(server_default="1")
