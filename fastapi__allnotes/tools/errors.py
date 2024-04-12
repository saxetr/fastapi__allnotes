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