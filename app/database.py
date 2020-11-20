from databases import Database
from sqlalchemy import (
    Binary,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    MetaData,
    String,
    Table,
    create_engine,
    func,
)
from sqlalchemy.dialects.postgresql import UUID

from .config import DATABASE_URL

engine = create_engine(DATABASE_URL)
metadata = MetaData()

database = Database(DATABASE_URL)

users = Table(
    "users",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("phone", String, unique=True),
    Column("email", String, unique=True),
    Column("password", Binary),
    Column("is_active", Boolean, server_default="true"),
    Column("is_superuser", Boolean, server_default="false"),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, onupdate=func.now()),
    Column("deleted_at", DateTime, default=None),
)

videos = Table(
    "videos",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("file_path", String, unique=True),
    Column("owner", ForeignKey("users.id", ondelete="CASCADE")),
    Column("is_deleted", Boolean, server_default="false"),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, onupdate=func.now()),
    Column("deleted_at", DateTime, default=None),
)

metadata.create_all(engine)
