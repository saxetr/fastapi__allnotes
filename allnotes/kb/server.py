from typing import Annotated

from fastapi import FastAPI
from fastapi import Request, Response


from allnotes.routers import api


app = FastAPI()


app.include_router(api.router)


@app.get("/")
def root():
    return "ALL NOTES"

