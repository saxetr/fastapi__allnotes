import typer

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import Session

from allnotes.kb.models import Base
from allnotes.config import config


url_object = URL.create(
    "postgresql+psycopg2",
    username=config.db.username,
    password=config.db.password,
    host=config.db.host,
    database=config.db.database
)

engine = create_engine(url_object, echo=True)


def get_session():
    # session = sessionmaker(engine)
    return Session(engine)


app = typer.Typer()


@app.command()
def meta_print():
    print(Base.metadata.tables)


@app.command()
def migrate():
    Base.metadata.create_all(engine)


@app.command()
def drop():
    Base.metadata.drop_all(engine)


@app.command()
def reset():
    drop()
    migrate()


if __name__ == "__main__":
    app()