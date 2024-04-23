from xml.dom.minidom import parse, Document
import zipfile
import hashlib

from allnotes.tools.odt2html import convert_xml_dom_to_html
from allnotes.kb.crud import session, NoteRepo


tmp_odt = 'tmp/tmp.odt'


def extract_xml_content_from_odt(filename) -> Document:
    with zipfile.ZipFile(filename) as myzip:
        with myzip.open('content.xml') as content:
            return parse(content)


def generate_hash(content: str) -> str:
    result = hashlib.md5(content.encode())
    return result.hexdigest()


def prepare_note():
    title = 'tmp'
    xml_doc = extract_xml_content_from_odt(tmp_odt)
    html = convert_xml_dom_to_html(xml_doc)
    html_hash = generate_hash(html)


    new_note = NoteRepo(session).add_note(title, html, html_hash)