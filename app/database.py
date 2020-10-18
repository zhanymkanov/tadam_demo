from databases import Database
from sqlalchemy import Binary, Boolean, Column, MetaData, String, Table, create_engine
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
)

metadata.create_all(engine)
