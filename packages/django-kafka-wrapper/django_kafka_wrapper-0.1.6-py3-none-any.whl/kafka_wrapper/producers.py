import json
from typing import Type

from django.db.models import Model
from kafka import KafkaProducer
from rest_framework.serializers import Serializer

from .base import SerializableMixin, KafkaMessage
from .settings import kafka_settings


class BaseProducer(SerializableMixin, KafkaProducer):
    topic: str
    disable_callbacks: bool = False

    def __init__(self, **configs):
        super().__init__(
            bootstrap_servers=kafka_settings.servers,
            api_version=kafka_settings.version,
            value_serializer=self.get_serializer(),
            **configs,
        )

    def get_topic(self, topic: str = None):
        return topic or self.topic

    def send(
            self,
            value,
            topic=None,
            key=None,
            headers=None,
            partition=None,
            timestamp_ms=None,
    ):
        topic = self.get_topic(topic)
        future = super().send(
            topic,
            value=value,
            key=key,
            headers=headers,
            partition=partition,
            timestamp_ms=timestamp_ms,
        )
        if not self.disable_callbacks:
            future.add_callback(self.success, value)
            future.add_errback(self.error, value)
        return future

    def success(self, message, kwargs):
        pass

    def error(self, message, kwargs):
        pass


class JSONProducer(BaseProducer):
    @classmethod
    def serialize(cls, value):
        return json.dumps(value).encode()


class DRFProducer(JSONProducer):
    drf_serializer: Type[Serializer] = None

    @classmethod
    def serialize(cls, value):
        if not isinstance(value, Model):
            raise Exception('DRFProducer expects Model instance.')
        serializer = cls.drf_serializer(instance=value)
        return super().serialize(serializer.data)


class MessageProducer(JSONProducer):
    @classmethod
    def serialize(cls, value: KafkaMessage):
        data = {
            'command': value.command,
            'data': value.data,
        }
        return super().serialize(data)
