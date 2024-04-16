import os

from dotenv import load_dotenv

from sqlalchemy import create_engine, URL, text
from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session

from allnotes.kb.models import Notes, Versions, CurrentVersions
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


def add_note(title: str, content: str):
    with Session(engine) as session:
        session.begin()

        new_note = Notes(title=title,)
        session.add(new_note)
        session.commit()





        # try:
        #     # new note
        #     new_note = Notes(title=title,)
        #     session.add(new_note)
        #     session.flush()
            
        #     # new version
        #     new_version = Versions(
        #         note_id=new_note.note_id,
        #         content=content,
        #         version=1,
        #     )  
        #     session.add(new_version)
        #     session.flush()

        #     # add current version
        #     current_version = CurrentVersions(
        #         note_id=new_note.note_id,
        #         version_id=new_version.version_id
        #     )
        #     session.add(current_version)

        # except:
        #     session.rollback()
        #     raise
        # else:
        #     session.commit()



















# from sqlalchemy.orm.session import Session
# from .kb__models import Subject, Subtheme, Article
# from sqlalchemy.orm import Session


# def add_subject(db: Session, name):
#     new_subject = Subject(
#         name=name,
#     )
#     db.add(new_subject)
#     db.commit()
#     db.refresh(new_subject)

#     return new_subject

# def add_subtheme(db: Session, name, subject):
#     new_subtheme = Subtheme(
#         name=name,
#         subject=subject,
#     )
#     db.add(new_subtheme)
#     db.commit()
#     db.refresh(new_subtheme)

#     return new_subtheme


# def add_article(db: Session, name, subtheme):
#     new_article = Article(
#         name=name,
#         subtheme=subtheme
#     )
#     db.add(new_article)
#     db.commit()
#     db.refresh(new_article)

#     return new_article