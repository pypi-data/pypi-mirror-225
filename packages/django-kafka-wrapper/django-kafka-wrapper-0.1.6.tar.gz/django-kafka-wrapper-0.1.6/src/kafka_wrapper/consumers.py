import json
from typing import Type

import weakref

from kafka import KafkaConsumer
from kafka.consumer.fetcher import ConsumerRecord
from rest_framework.serializers import Serializer

from .base import SerializableMixin, KafkaMessage
from .enum import ConsumerOffsetReset
from .settings import kafka_settings


class KeepRefsMixin(object):
    __refs__ = list()
    def __init__(self, *args, **kwargs):
        self.__refs__.append(weakref.ref(self))
        super().__init__(*args, **kwargs)

    @classmethod
    def get_instances(cls):
        for inst_ref in cls.__refs__:
            inst = inst_ref()
            if inst is not None:
                yield inst


class BaseConsumer(SerializableMixin, KeepRefsMixin, KafkaConsumer):
    topic: str
    auto_offset_reset: ConsumerOffsetReset = ConsumerOffsetReset.EARLIEST

    def get_topic(self, topic: str = None):
        return topic or self.topic

    def __init__(self, topic: str = None, *topics, **configs):
        topic = self.get_topic(topic)
        auto_offset_reset: ConsumerOffsetReset = configs.pop(
            'auto_offset_reset',
            self.auto_offset_reset,
        ).value
        enable_auto_commit = configs.pop('enable_auto_commit', True)
        super().__init__(
            topic,
            bootstrap_servers=kafka_settings.servers,
            api_version=kafka_settings.version,
            value_deserializer=self.get_serializer(),
            auto_offset_reset=auto_offset_reset,
            enable_auto_commit=enable_auto_commit,
            consumer_timeout_ms=kafka_settings.consumer_timeout.microseconds / 1000,
            *topics,
            **configs,
        )

    def process(self, record: ConsumerRecord):
        print(f'{self.__class__.__name__} [{record.offset=}] - {record.key=}')
        print(f'{record.value}')
        print('')


class JSONConsumer(BaseConsumer):
    @classmethod
    def serialize(cls, value):
        if isinstance(value, bytes):
            value = value.decode()
        return json.loads(value)


class DRFConsumer(JSONConsumer):
    drf_serializer: Type[Serializer] = None

    @classmethod
    def serialize(cls, value):
        value = super().serialize(value)
        serializer = cls.drf_serializer(data=value)
        serializer.is_valid(raise_exception=True)
        return serializer.data


class MessageConsumer(JSONConsumer):
    @classmethod
    def serialize(cls, value):
        value = super().serialize(value)
        return KafkaMessage(
            command=value['command'],
            data=value['data'],
        )
