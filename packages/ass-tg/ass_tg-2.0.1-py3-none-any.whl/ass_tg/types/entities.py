from ass_tg.entities import ArgEntities
from ass_tg.types.wrapped import WrappedArgFabricABC


class CutCommandEntitiesArg(WrappedArgFabricABC):
    """
    Cuts entities that are in command text.
    Used to be the first arg for ArgsMiddleware.
    """

    def pre_parse(
            self,
            text: str,
            offset: int,
            entities: ArgEntities,
            **_kwargs
    ):
        if 'command' not in _kwargs:
            raise ValueError('Must provide a command kwarg!')

        if command := _kwargs['command']:
            # Let's assume that we have only one space before the arguments text
            real_offset = len(command.prefix) + len(command.command) + 1
            offset = 0

            entities = entities.cut_before(real_offset)

        return super().pre_parse(text, offset, entities, **_kwargs)
