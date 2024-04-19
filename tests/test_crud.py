import pytest

from allnotes.kb.crud import NoteRepo
from allnotes.kb.models import Note, Version, CurrentVersion


#

def test__add_note__success_added_title(test_session, valid_note, valid_version):
    note_id = NoteRepo(test_session).add_note(valid_note.title, valid_version.content)

    created_note = test_session.query(Note).filter_by(note_id=note_id).first()

    assert created_note is not None
    assert created_note.title == valid_note.title


@pytest.mark.xfail()
def test__add_note__fail_if_title_not_unique(test_session, valid_note, valid_version):
    NoteRepo(test_session).add_note(valid_note.title, valid_version.content)
    NoteRepo(test_session).add_note(valid_note.title, valid_version.content)


#

def test__add_note__success_added_content(test_session, valid_note, valid_version):
    note_id = NoteRepo(test_session).add_note(valid_note.title, valid_version.content)

    created_version = test_session.query(Version).filter_by(note_id=note_id, version=1).first()

    assert created_version is not None
    assert created_version.content == valid_version.content


def test__add_note__link_title_with_first_content_version(test_session, valid_note, valid_version):
    note_id = NoteRepo(test_session).add_note(valid_note.title, valid_version.content)

    note_link = test_session.query(CurrentVersion).filter_by(note_id=note_id).first()
    content = test_session.query(Version).filter_by(version_id=note_link.version_id).first()
    
    assert content.version == 1


#

def test__update_note__add_new_content_version_and_increment_version_number(test_session, valid_note, valid_version):
    new_content = '<p>moooOOOOOOO</p>'
    note_id = NoteRepo(test_session).add_note(valid_note.title, valid_version.content)
    version_id = NoteRepo(test_session).update_note(note_id, new_content)

    new_version = test_session.query(Version).filter_by(version_id=version_id).first()

    assert new_version.content == new_content
    assert new_version.version == 2

    
