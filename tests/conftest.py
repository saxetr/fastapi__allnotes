import pytest

from sqlalchemy.orm import Session

from allnotes.kb.crud import engine
from allnotes.kb.models import Base, Note, Version


@pytest.fixture()
def test_session():
    Base.metadata.create_all(engine)

    connection = engine.connect()

    trans = connection.begin()

    session = Session(bind=connection, join_transaction_mode="create_savepoint") 

    yield session

    session.close()

    trans.rollback()

    connection.close()


@pytest.fixture
def valid_note():
    valid_note = Note(
        title='test_note',
    )

    return valid_note


@pytest.fixture
def valid_version():
    valid_version = Version(
        content='<p>AAAAAAAAAAAf</p>',  # update_note(1, '<p>moooOOOOOOO</p>')
        version=1,
    )
    return valid_version




@pytest.fixture()
def make_xml_tag_a():
    return (
            '<text:a xlink:type="simple" xlink:href="https://docs.python.org/3/library/xml.html" ' \
            'text:style-name="Internet_20_link" ' \
            'text:visited-style-name="Visited_20_Internet_20_Link">' \
            'https://docs.python.org/3/library/xml.html' \
            '</text:a>'
    )


@pytest.fixture()
def make_xml(make_xml_tag_a):
    open_office = '<office:text ' \
        'xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" ' \
        'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" ' \
        'xmlns:xlink="http://www.w3.org/1999/xlink">'
    close_office = '</office:text>'
    
    def inner(
            tag_name,       # h or p
            tag_style_k=None,
            tag_style_v=None,
            tag_value="swesh etih majgkih", 
            nested_tag_a=False
    ):
        
        tag_style = '' if not tag_style_k else f' {tag_style_k}="{tag_style_v}"'
        
        tag_a = '' if not nested_tag_a else make_xml_tag_a

        xml_src = (
                f'{open_office}'
                    f'<text:{tag_name} {tag_style}>'
                        f'{tag_value}{tag_a}'
                    f'</text:{tag_name}>'
                f'{close_office}'
        )
        
        return xml_src
    
    return inner


