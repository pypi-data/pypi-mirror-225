from dataclasses import dataclass
from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


_KAFKA_WRAPPER = 'KAFKA_WRAPPER'


@dataclass
class KafkaSettings(object):
    servers: list[str]
    version: tuple
    consumer_timeout: timedelta = timedelta(milliseconds=100)


def build_settings():
    project_settings = getattr(settings, _KAFKA_WRAPPER)
    if not project_settings:
        raise ImproperlyConfigured(f'{_KAFKA_WRAPPER} settings not found.')
    return KafkaSettings(**project_settings)

kafka_settings = build_settings()
