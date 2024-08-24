import tempfile

import pytest
from django.core.management import call_command

from app.enums import CollectionCommandRunStatus
from app.models import CollectionCommandRun, NginxLog


@pytest.mark.django_db
def test_collect_logs_command__ok():
    file_content = [
        '{"time": "17/May/2015:08:05:32 +0000", "remote_ip": "93.180.71.3", "remote_user": "-",'
        '"request": "GET /downloads/product_1 HTTP/1.1", "response": 304, "bytes": 0, "referrer": "-", '
        '"agent": "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"}\n',
        '{"time": "17/May/2015:08:06:32 +0000", "remote_ip": "93.180.71.4", "remote_user": "-", '
        '"request": "GET /downloads/product_2 HTTP/1.1", "response": 200, "bytes": 1024, "referrer": "-", '
        '"agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/58.0.3029.110 Safari/537.3"}\n',
    ]

    temp_file_name = None
    with tempfile.NamedTemporaryFile(mode="w+", delete=True) as temp_file:
        temp_file.writelines(file_content)
        temp_file.seek(0)
        temp_file_name = temp_file.name
        call_command("import_logs", temp_file_name)
    run = CollectionCommandRun.objects.first()

    assert CollectionCommandRun.objects.count() == 1
    assert NginxLog.objects.count() == len(file_content)
    assert run.status == CollectionCommandRunStatus.SUCCESS
    assert run.filename == temp_file_name


@pytest.mark.django_db
def test_collect_logs_command__fail(mocker):
    file_content = [
        '{"time": "17/May/2015:08:05:32 +0000", "remote_ip": "93.180.71.3", "remote_user": "-",'
        '"request": "GET /downloads/product_1 HTTP/1.1", "response": 304, "bytes": 0, "referrer": "-", '
        '"agent": "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"}\n',
        '{"time": "17/May/2015:08:06:32 +0000", "remote_ip": "93.180.71.4", "remote_user": "-", '
        '"request": "GET /downloads/product_2 HTTP/1.1", "response": 200, "bytes": 1024, "referrer": "-", '
        '"agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/58.0.3029.110 Safari/537.3"}\n',
    ]

    temp_file_name = None
    with tempfile.NamedTemporaryFile(mode="w+", delete=True) as temp_file:
        temp_file.writelines(file_content)
        temp_file.seek(0)
        temp_file_name = temp_file.name
        mocker.patch("app.logic.loader.load_nginx_logs", return_value=Exception("Mocked exception"))
        call_command("import_logs", temp_file_name)

    run = CollectionCommandRun.objects.first()

    assert CollectionCommandRun.objects.count() == 1
    assert NginxLog.objects.count() == 0
    assert run.status == CollectionCommandRunStatus.FAILED
    assert run.filename == temp_file_name
