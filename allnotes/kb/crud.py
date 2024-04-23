import os

from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

from dotenv import load_dotenv

from sqlalchemy import create_engine, URL, text
# from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import sessionmaker, Session

from allnotes.kb.models import Note, Version, CurrentVersion
from allnotes.tools.errors import ConflictError, UniqueViolationError

# take environment variables from .env.
load_dotenv()


url_object = URL.create(
    "postgresql+psycopg2",
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),  # plain (unescaped) text
    host="localhost",
    database=os.getenv("POSTGRES_DB"),
)

engine = create_engine(url_object)

# session = sessionmaker(engine)
session = Session(engine)


class NoteRepo():

    def __init__(self, session: Session) -> None:
        self.session = session

    def add_note(self, title: str, content: str, content_hash: str) -> int:
        with self.session.begin():
            try:
                new_note = Note(title=title)
                self.session.add(new_note)
                self.session.flush()

                new_version = Version(
                    note_id=new_note.note_id,
                    content=content,
                    content_hash=content_hash,
                    version=1,
                )
                self.session.add(new_version)
                self.session.flush()

                current_version = CurrentVersion(
                    note_id=new_note.note_id,
                    version_id=new_version.version_id
                )
                self.session.add(current_version)

            except IntegrityError as e: 
                if isinstance(e.orig, UniqueViolation):
                    constraint = e.orig.diag.constraint_name
                    table = e.orig.diag.table_name
                    # breakpoint()
                    match constraint:
                        case 'notes_title_key':
                            raise UniqueViolationError(entity=table, field='title') from e  
                        case 'note_versions_pkey':
                            raise UniqueViolationError(entity=table, field='note_version') from e
                        case 'note_versions_content_hash_key':
                            raise UniqueViolationError(entity=table, field='content_hash') from e
                        
                raise ConflictError('some_entity', 'some_reason')

        return new_note.note_id

    def update_note(self, note_id: int, new_content: str, new_content_hash: str):
        with self.session.begin():
            pass










