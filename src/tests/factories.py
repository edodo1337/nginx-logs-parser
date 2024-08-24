from factory import Faker
from factory.django import DjangoModelFactory

from app.enums import CollectionCommandRunStatus
from app.models import CollectionCommandRun, NginxLog


class NginxLogFactory(DjangoModelFactory):
    class Meta:
        model = NginxLog

    time = Faker("date_time")
    remote_ip = Faker("ipv4")
    remote_user = Faker("user_name")
    request = Faker("uri_path")
    response = Faker("random_int", min=100, max=599)
    bytes = Faker("random_int", min=0, max=10000)
    referrer = Faker("uri")
    agent = Faker("user_agent")


class CollectionCommandRunFactory(DjangoModelFactory):
    class Meta:
        model = CollectionCommandRun

    filename = Faker("file_name", extension="ndjson")
    status = Faker("random_element", elements=[status.value for status in CollectionCommandRunStatus])
