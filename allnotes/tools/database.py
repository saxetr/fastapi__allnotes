import typer

from allnotes.kb.crud import engine
from allnotes.kb.models import Base
  

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