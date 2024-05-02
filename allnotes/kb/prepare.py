from xml.dom.minidom import parse, Document
import zipfile
import hashlib

from fastapi import UploadFile

from allnotes.tools.odt2html import convert_xml_dom_to_html
from allnotes.kb.crud import NoteRepo
from allnotes.kb.db import get_session


session = get_session()

# tmp_odt = 'tmp/tmp.odt'


def extract_xml_content_from_odt(file) -> Document:
    with zipfile.ZipFile(file) as myzip:
        with myzip.open('content.xml') as content:
            return parse(content)


def generate_hash(content: str) -> str:
    result = hashlib.md5(content.encode())
    return result.hexdigest()


def prepare_note(file: UploadFile) -> int:
    title = file.filename.rstrip(".odt")
    xml_doc = extract_xml_content_from_odt(file.file)
    html = convert_xml_dom_to_html(xml_doc)
    html_hash = generate_hash(html)

    new_note = NoteRepo(session).add_note(title, html, html_hash)

    return new_note
