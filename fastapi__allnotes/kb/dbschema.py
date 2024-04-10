from uuid import uuid4

from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID


metadata_obj = MetaData()

note_table = Table(
    "note_meta",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement="auto"),
    Column("title", String(50), nullable=False, unique=True),
    Column("version", Integer, nullable=False, unique=True, default=1),   # ColumnDefault?
    Column("tags", String),
)


version_table = Table(
    "note_version",
    metadata_obj,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4()),     # as_uuid=True?
    Column("note", ForeignKey("note_meta.title"), nullable=False),
    Column("body", String, nullable=False),
    Column("version", ForeignKey("note_meta.version"), nullable=False)
)


tag_table = Table(
    "note_tag",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("tag_name", String, nullable=False)
)