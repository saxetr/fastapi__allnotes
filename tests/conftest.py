import pytest

from sqlalchemy.orm import Session, scoped_session, sessionmaker, Session
from sqlalchemy import event

from allnotes.kb.crud import engine
from allnotes.kb.models import Note, Version
from allnotes.kb.crud import NoteRepo
from allnotes.kb.prepare import generate_hash


@pytest.fixture()
def connection():
    connection = engine.connect()
    yield connection
    connection.close()


@pytest.fixture()
def transaction(connection):
    transaction = connection.begin()
    yield
    transaction.rollback()


@pytest.fixture(
    scope='function',
    autouse=True  # New test DB session for each test todo we need it only for tests with Client fixture
)
def session(connection, transaction):
    """
    SQLAlchemy session started with SAVEPOINT
    After test rollback to this SAVEPOINT
    """
    # connection = engine().connect()

    # begin a non-ORM transaction
    # trans = connection.begin()
    session = sessionmaker()(bind=connection, join_transaction_mode="create_savepoint")

    session.begin_nested()  # SAVEPOINT

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        """
        Each time that SAVEPOINT ends, reopen it
        """
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()

    yield session

    session.close()


# @pytest.fixture()
# def session(connection, transaction):
#     session = Session(bind=connection, join_transaction_mode="create_savepoint") 

#     yield session

#     session.close()

# @pytest.fixture(autouse=True)
# def session(connection, request):
#     """Returns a database session to be used in a test.

#     This fixture also alters the application's database
#     connection to run in a transactional fashion. This means
#     that all tests will run within a transaction, all database
#     operations will be rolled back at the end of each test,
#     and no test data will be persisted after each test.

#     `autouse=True` is used so that session is properly
#     initialized at the beginning of the test suite and
#     factories can use it automatically.
#     """
#     transaction = connection.begin()
#     session = Session(bind=connection)
#     # session.begin_nested()

#     @event.listens_for(session, "after_transaction_end")
#     def restart_savepoint(db_session, transaction):
#         """Support tests with rollbacks.

#         This is required for tests that call some services that issue
#         rollbacks in try-except blocks.

#         With this event the Session always runs all operations within
#         the scope of a SAVEPOINT, which is established at the start of
#         each transaction, so that tests can also rollback the
#         “transaction” as well while still remaining in the scope of a
#         larger “transaction” that’s never committed.
#         """
#         breakpoint()
#         if transaction.nested and not transaction._parent.nested:
#             # ensure that state is expired the way session.commit() at
#             # the top level normally does
#             session.expire_all()
#             session.begin_nested()

#     def teardown():
#         Session.remove()
#         transaction.rollback()

#     request.addfinalizer(teardown)

#     return session


@pytest.fixture()
def note_repo(session): 
    return NoteRepo(session)


@pytest.fixture
def valid_note():
    valid_note = Note(
        title='test_note',
    )

    return valid_note


@pytest.fixture
def valid_version():
    content = '<p>AAAAAAAAAAAf</p>'
    content_hash = '5bfa5ba2690ae9405c467f7492f22957'

    valid_version = Version(
        content=content,
        content_hash=content_hash,
        version=1,
    )
    return valid_version


@pytest.fixture()
def make_note(session):
    def inner(
            # note
            title: str = 'test_title',
            # version
            content: str = '<p>test paragraph</p>',
            version: int = 1
    ):
        content_hash = generate_hash(content)

        note = Note(title=title)
        session.add(note)
        session.commit()
        
        version = Version(
            note_id=note.note_id,
            content=content,
            content_hash=content_hash,
            version=version
        )
        session.add(version)
        session.commit()

        # костыль
        session.query(Note).first()
        session.get_transaction().close()

        return note, version

    return inner




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


