from typing import Iterable, List

from aiogram.types import MessageEntity


class ArgEntities(List[MessageEntity]):
    """Adequate implementation of the message entity"""

    def __init__(self, entities: Iterable[MessageEntity]):
        super().__init__(entities)

    @staticmethod
    def change_entity(entity: MessageEntity, to_remove: int):
        entity = entity.copy()
        entity.offset -= to_remove
        return entity

    def cut_before(self, offset: int):
        entities = [
            self.change_entity(x, to_remove=offset) for x in self
            if x.offset >= offset
        ]
        return ArgEntities(entities)

    def cut_after(self, offset: int):
        entities = [
            x for x in self
            if x.length <= offset
        ]
        return ArgEntities(entities)

    def get_overlapping(self, offset: int, length: int):
        """Return a list of found entities in this text vector"""

        return [
            entity
            for entity in self
            if (offset <= entity.offset < offset + length) or (entity.offset <= offset < entity.offset + entity.length)
        ]

    def get_non_overlapping_index(self, raw_text: str, to_search: str, start_offset: int = 0) -> int:
        """
        Return the index of the first occurrence of the given text that not being overlapped with any entities
        Returns -1 if not found
        """

        text_length = len(to_search)
        for i in range(start_offset, len(raw_text) - text_length + 1):
            is_overlapping = any(
                (i <= entity.offset < i + text_length)
                or (entity.offset <= i < entity.offset + entity.length)
                for entity in self
            )
            if not is_overlapping and raw_text[i:i + text_length] == to_search:
                return i

        return -1
