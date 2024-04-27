# ODT Errors
class OdtParseError(Exception):

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class OdtUnknownTagError(OdtParseError):

    def __init__(self, tag: str) -> None:
        super().__init__(reason=f'unknown tag: {tag}')
        self.tag = tag


class OdtMissedElementAttrError(OdtParseError):

    def __init__(self, attr: str) -> None:
        super().__init__(reason=f'missed attribute: {attr}')
        self.attr = attr


class OdtUnknownHeaderError(OdtParseError):

    def __init__(self, header: str) -> None:
        super().__init__(reason=f'header style is unknown: {header}')
        self.header = header


#
# App Erorrs
class AppError(Exception):

    def __init__(self, reason: str, status_code=500) -> None:
        super().__init__(reason, status_code)
        self.reason = reason
        self.status_code = status_code


class ConflictError(AppError):
    def __init__(self, entity, reason) -> None:
        super().__init__(reason, status_code=409)
        self.entity = entity


class UniqueViolationError(ConflictError):
    def __init__(self, entity, field) -> None:
        super().__init__(entity, reason=f'{field} constraint')
        self.field = field
