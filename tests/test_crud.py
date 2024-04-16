import pytest

from allnotes.kb.crud import add_note

# протестировать что у новой версии номер увеличен на еденицу


title = 'test_note'
content = '<p>AAAAAAAAAAAf</p>'



def test__add_note__success_added():
    """
    проверить, что успешно добавилась запись в бд
    ???
    сделать выборку по тайтлу? по айди?
    """
    

    assert add_note(title, content) == 1


# test__update_note__increase_note_version_number():


