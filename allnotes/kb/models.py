import uuid
from datetime import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "notes"

    note_id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto")
    title: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    # Column("tags", String),

    def __repr__(self) -> str:
        return f"Note(note_id={self.note_id!r}, title={self.title!r})"


class Version(Base):
    __tablename__ = "note_versions"

    version_id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    note_id = mapped_column(ForeignKey("notes.note_id"), nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    version: Mapped[int] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    content_hash: Mapped[str] = mapped_column(nullable=True, unique=True)

    def __repr__(self) -> str:
        return (
            f"Version(version_id={self.version_id!r}, "
            f"content={self.content!r}, content_hash={self.content_hash!r})"
        )


class CurrentVersion(Base):
    __tablename__ = "current_versions"

    note_id = mapped_column(ForeignKey("notes.note_id"), primary_key=True)
    version_id = mapped_column(ForeignKey("note_versions.version_id"))