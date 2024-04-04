


class UnknownTagError(Exception):

    def __init__(self, tag: str) -> None:
        super().__init__(f'unknown tag: {tag}')
        self.tag = tag