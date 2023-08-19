from .lists import ListArg


class DividedArg(ListArg):
    list_separator: str

    def __init__(self, *args, separator: str = '|'):
        super().__init__(
            *args,
            separator=separator,
            prefix='',
            postfix=''
        )
