import os

from dotenv import load_dotenv

from sqlalchemy import create_engine, URL, text
# from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import sessionmaker, Session

from allnotes.kb.models import Note, Version, CurrentVersion
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

session = sessionmaker(engine)


class NoteRepo():

    def __init__(self, session: Session) -> None:
        self.session = session

    def add_note(self, title: str, content: str) -> int:
        with self.session.begin():

            new_note = Note(title=title,)
            self.session.add(new_note)
            self.session.flush()

            new_version = Version(
                note_id=new_note.note_id,
                content=content,
                version=1,
            )  
            self.session.add(new_version)
            self.session.flush()

            current_version = CurrentVersion(
                note_id=new_note.note_id,
                version_id=new_version.version_id
            )
            self.session.add(current_version)

        return new_note.note_id

    def update_note(self, note_id: int, new_content: str):
        with self.session.begin():
            pass










