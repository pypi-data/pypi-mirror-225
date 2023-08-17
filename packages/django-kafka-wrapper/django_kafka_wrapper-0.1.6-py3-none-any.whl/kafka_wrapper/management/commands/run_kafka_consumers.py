import itertools
import sys
import time

from importlib.metadata import version

from django.core.management.base import BaseCommand
from django.utils import timezone

from ...consumers import KeepRefsMixin
from ...settings import kafka_settings


_LOGO = '''
 _   __  ___  ______ _   __  ___    _    _______  ___  ____________ ___________ 
| | / / / _ \ |  ___| | / / / _ \  | |  | | ___ \/ _ \ | ___ \ ___ \  ___| ___ \ 
| |/ / / /_\ \| |_  | |/ / / /_\ \ | |  | | |_/ / /_\ \| |_/ / |_/ / |__ | |_/ /
|    \ |  _  ||  _| |    \ |  _  | | |/\| |    /|  _  ||  __/|  __/|  __||    / 
| |\  \| | | || |   | |\  \| | | | \  /\  / |\ \| | | || |   | |   | |___| |\ \ 
\_| \_/\_| |_/\_|   \_| \_/\_| |_/  \/  \/\_| \_\_| |_/\_|   \_|   \____/\_| \_|
'''


class Command(BaseCommand):
    help = "Fetch and apply Kafka messages"
    consumers = []

    def _msg(self, msg, style=None, ending=None):
        if style:
            msg = style(msg)
        self.stdout.write(msg, ending=ending)

    def _yellow(self, msg, ending=None):
        self._msg(msg, self.style.WARNING, ending)

    def _green(self, msg, ending=None):
        self._msg(msg, self.style.SUCCESS, ending)

    def _red(self, msg, ending=None):
        self._msg(msg, self.style.ERROR, ending)

    def _get_consumer(self, consumer):
        return f'{consumer.__module__}.{consumer.__class__.__name__}'

    def handle(self, *args, **options):
        self._yellow(_LOGO)
        self._yellow(f'Kafka API version: {".".join(map(str, kafka_settings.version))}')
        self._yellow(f'KafkaWrapper version: {version("django-kafka-wrapper")}')
        self._yellow('Servers:')
        for server in kafka_settings.servers:
            self._msg(f'  - {server}')
        self.consumers = list(KeepRefsMixin.get_instances())
        self._yellow('Consumers:')
        for c in self.consumers:
            self._msg(f'  - {self._get_consumer(c)}')
        self._msg('\n')

        self._yellow('Kafka consumers are running...')

        for consumer in itertools.cycle(self.consumers):
            consumer_name = consumer.__class__.__name__
            try:
                try:
                    record = next(consumer)
                except StopIteration:
                    pass
                except Exception as e:
                    self._yellow(f'[{timezone.now()}]: Job {consumer_name} .. [error]:',
                                 ending='')
                    self._red(e)
                else:
                    try:
                        self._yellow(
                            f'[{timezone.now()}]: Starting job {consumer_name} ...')
                        consumer.process(record)
                    except Exception as e:
                        self._yellow(
                            f'[{timezone.now()}]: Job {consumer_name} .. [error]: ',
                            ending='')
                        self._red(e)
                    else:
                        self._yellow(f'[{timezone.now()}]: Job {consumer_name} .. [OK]')
                time.sleep(kafka_settings.consumer_timeout.microseconds / 1_000_000)
            except KeyboardInterrupt:
                self._yellow('\n\n Kafka consumers are shutting down.')
                sys.exit(0)
