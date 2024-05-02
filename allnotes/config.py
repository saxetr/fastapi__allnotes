import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class DbConfig:
    username: str
    password: str  # plain (unescaped) text
    host: str
    database: str


@dataclass
class AppConf:
    db: DbConfig


def load() -> AppConf:
    load_dotenv()

    db_conf = DbConfig(
        username=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DB")
    )
    return AppConf(db=db_conf)


config = load()
