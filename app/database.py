from databases import Database
from sqlalchemy import (
    Binary,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    MetaData,
    SmallInteger,
    String,
    Table,
    UniqueConstraint,
    create_engine,
    func,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy_utils.types import CountryType, PhoneNumberType

from .config import DATABASE_URL

engine = create_engine(DATABASE_URL)
metadata = MetaData()

database = Database(DATABASE_URL)

users = Table(
    "users",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("phone", PhoneNumberType, unique=True),
    Column("email", String, unique=True),
    Column("password", Binary),
    Column("is_active", Boolean, server_default="true"),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, onupdate=func.now()),
)

categories = Table(
    "categories",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("title", String, unique=True),
    Column("slug", String, unique=True),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, onupdate=func.now()),
)

tags = Table(
    "tags",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("title", String, unique=True),
    Column("slug", String, unique=True),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, onupdate=func.now()),
)

languages = Table(
    "languages",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("code", String, unique=True),
    Column("name", String, unique=True),
)

videos = Table(
    "videos",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("file_path", String, unique=True),
    Column("owner_id", ForeignKey("users.id", ondelete="CASCADE")),
    Column("category_id", ForeignKey("categories.id", ondelete="SET NULL")),
    Column("title", String),
    Column("description", String),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, onupdate=func.now()),
)


video_metadata = Table(
    "video_metadata",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("video_id", ForeignKey("videos.id", ondelete="CASCADE")),
    Column("quality", String),
    Column("size", SmallInteger),
    Column("country", CountryType),
    Column("language_id", ForeignKey("languages.id", ondelete="SET NULL")),
    Column("duration", SmallInteger),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, onupdate=func.now()),
)

video_tags = Table(
    "video_tags",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("video_id", ForeignKey("videos.id", ondelete="CASCADE")),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE")),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, onupdate=func.now()),
)

video_likes = Table(
    "video_likes",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("video_id", ForeignKey("videos.id", ondelete="CASCADE")),
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE")),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, onupdate=func.now()),
    UniqueConstraint("video_id", "user_id", name="video_likes_video_id_user_id_key"),
)

video_comments = Table(
    "video_comments",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("video_id", ForeignKey("videos.id", ondelete="CASCADE")),
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE")),
    Column("text", String),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, onupdate=func.now()),
)

collections = Table(
    "collections",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("title", String, unique=True),
    Column("slug", String, unique=True),
    Column("description", String),
    Column("owner_id", ForeignKey("users.id", ondelete="CASCADE")),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, onupdate=func.now()),
)

collection_videos = Table(
    "collection_videos",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("collection_id", ForeignKey("collections.id", ondelete="CASCADE")),
    Column("video_id", ForeignKey("videos.id", ondelete="CASCADE")),
    Column("video_order", SmallInteger),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, onupdate=func.now()),
)

interests = Table(
    "interests",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("title", String, unique=True),
    Column("slug", String, unique=True),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, onupdate=func.now()),
)

category_interests = Table(
    "category_interests",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("category_id", ForeignKey("categories.id", ondelete="CASCADE")),
    Column("interest_id", ForeignKey("interests.id", ondelete="CASCADE")),
    Column("weight", SmallInteger),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, onupdate=func.now()),
)

user_interests = Table(
    "user_interests",
    metadata,
    Column("id", UUID, primary_key=True),
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE")),
    Column("interest_id", ForeignKey("interests.id", ondelete="CASCADE")),
    Column("created_at", DateTime, server_default=func.now()),
    Column("updated_at", DateTime, onupdate=func.now()),
)

metadata.create_all(engine)
