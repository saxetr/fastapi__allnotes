from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation

from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session

from allnotes.kb.models import Note, Version, CurrentVersion
from allnotes.tools.errors import ConflictError, UniqueViolationError


class NoteRepo():

    def __init__(self, session: Session) -> None:
        self.session = session

    def add_note(self, title: str, content: str, content_hash: str) -> int:
        with self.session as session, session.begin():
            try:
                new_note = Note(title=title)
                session.add(new_note)
                session.flush()

                new_version = Version(
                    note_id=new_note.note_id,
                    content=content,
                    content_hash=content_hash,
                    version=1,
                )
                session.add(new_version)
                session.flush()

                current_version = CurrentVersion(
                    note_id=new_note.note_id,
                    version_id=new_version.version_id
                )
                session.add(current_version)

            except IntegrityError as e: 
                if isinstance(e.orig, UniqueViolation):
                    constraint = e.orig.diag.constraint_name
                    table = e.orig.diag.table_name
                    # breakpoint()
                    match constraint:
                        case 'notes_title_key':
                            raise UniqueViolationError(entity=table, field='title') from e  
                        case 'note_versions_pkey':
                            raise UniqueViolationError(entity=table, field='note_version') from e
                        case 'note_versions_content_hash_key':
                            raise UniqueViolationError(entity=table, field='content_hash') from e
                        
                raise ConflictError('some_entity', 'some_reason')

            return new_note.note_id

    def update_note(self, note_id: int, new_content: str, new_content_hash: str):
        with self.session as session, session.begin():
            try:
                select_cur_ver_stmt = (
                    select(
                        Version.version
                    ).join_from(
                        CurrentVersion, Version
                    ).where(
                        CurrentVersion.note_id == note_id
                    )
                )
                current_version = session.scalar(select_cur_ver_stmt)

                new_version = Version(
                    note_id=note_id,
                    content=new_content,
                    content_hash=new_content_hash,
                    version=current_version + 1
                )
                session.add(new_version)
                session.flush()

                update_cur_ver_stmt = (
                    update(
                        CurrentVersion
                    ).where(
                        CurrentVersion.note_id == note_id
                    ).values(
                        version_id=new_version.version_id
                    )
                )
                session.execute(update_cur_ver_stmt)

            except IntegrityError as e: 
                if isinstance(e.orig, UniqueViolation):
                    constraint = e.orig.diag.constraint_name
                    table = e.orig.diag.table_name
                    match constraint:
                        case 'note_versions_content_hash_key':
                            raise UniqueViolationError(entity=table, field='content_hash') from e
                        
                raise ConflictError('some_entity', 'some_reason')

            return new_version.version_id










