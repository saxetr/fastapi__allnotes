import os

from dotenv import load_dotenv

from sqlalchemy import create_engine, URL, text

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


def add_note():
    return True







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