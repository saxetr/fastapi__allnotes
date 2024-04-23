import pytest

from sqlalchemy.exc import IntegrityError

from allnotes.kb.models import Note, Version, CurrentVersion
from allnotes.tools.errors import ConflictError, UniqueViolationError


#

def test__add_note__success_added_title(session, valid_note, valid_version, note_repo):
    note_id = note_repo.add_note(valid_note.title, valid_version.content, valid_version.content_hash)

    created_note = session.query(Note).filter_by(note_id=note_id).first()

    assert created_note is not None
    assert created_note.title == valid_note.title


def test__add_note__raise_error_if_title_not_unique(valid_note, valid_version, note_repo, make_note):
    make_note(valid_note.title)
    # make_note('valid_note')

    with pytest.raises(UniqueViolationError) as e:
        note_repo.add_note(valid_note.title, valid_version.content, valid_version.content_hash)

    assert e.value.field == 'title'


#

def test__add_note__success_added_content(session, valid_note, valid_version, note_repo):
    note_id = note_repo.add_note(valid_note.title, valid_version.content, valid_version.content_hash)

    created_version = session.query(Version).filter_by(note_id=note_id, version=1).first()

    assert created_version is not None
    assert created_version.content == valid_version.content


def test__add_note_raise_error_if_content_hash_not_unique(valid_note, valid_version, note_repo, make_note, session):
    make_note(content=valid_version.content)

    with pytest.raises(UniqueViolationError) as e:
        note_repo.add_note(valid_note.title, valid_version.content, valid_version.content_hash)

    assert e.value.field == 'content_hash'


#

def test__add_note__link_title_with_first_content_version(session, valid_note, valid_version, note_repo):
    note_id = note_repo.add_note(valid_note.title, valid_version.content, valid_version.content_hash)

    note_link = session.query(CurrentVersion).filter_by(note_id=note_id).first()
    content = session.query(Version).filter_by(version_id=note_link.version_id).first()
    
    assert content.version == 1


#

# def test__update_note__add_new_content_version_and_increment_version_number(session, note_repo, make_note):
#     old_content = '<p>aaaaaaaaaaaaF</p>'
#     new_content = '<p>moooOOOOOOO</p>'
#     note = make_note(content=old_content)
#     assert note["version"].version == 1
#     version_id = note_repo.update_note(note_id=note["note"].note_id, content=new_content)

#     new_version = session.query(Version).filter_by(version_id=version_id).first()

#     assert new_version.content == new_content
#     assert new_version.version == note["version"].version + 1

    
