from dataclasses import dataclass
from typing import Any


class SerializableMixin(object):
    serializer: callable = None

    def get_serializer(self) -> callable:
        return self.serializer or self.serialize

    @classmethod
    def serialize(cls, value):
        raise NotImplementedError


@dataclass
class KafkaMessage:
    command: str = '.'  # `.` is a default command
    data: Any = None
