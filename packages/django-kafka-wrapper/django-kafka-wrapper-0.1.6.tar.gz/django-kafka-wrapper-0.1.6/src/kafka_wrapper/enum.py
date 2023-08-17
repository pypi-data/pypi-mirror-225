import enum


class ConsumerOffsetReset(enum.Enum):
    EARLIEST = 'earliest'
    LATEST = 'latest'
