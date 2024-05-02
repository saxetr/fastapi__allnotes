from fastapi import APIRouter
from fastapi import Form, File, UploadFile
from fastapi.responses import RedirectResponse

from allnotes.kb.prepare import prepare_note 


router = APIRouter(
    prefix="/api"
)


@router.get("/v1/")
def list_v1_api():
    return "API"


# kb
@router.get("/v1/kb/")
def api_list_notes():
    return "Notes"


@router.post("/v1/kb/")
def create_note(file: UploadFile):
    new_note_id = prepare_note(file)

    return {"note_id": new_note_id}


# kb/title
@router.get("/v1/kb/{title}")
def read_note():
    return "read Note"


@router.put("/v1/kb/{title}")
def update_note():
    return "Notes"