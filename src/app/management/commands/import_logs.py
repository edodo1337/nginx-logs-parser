import logging

from django.core.management.base import BaseCommand
from django.db import connection

from app.enums import CollectionCommandRunStatus
from app.logic.loader import get_file_processing_status, load_nginx_logs, set_file_processing_status

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load nginx logs from a TXT file into the database"
    default_chunk_size = 5000

    def add_arguments(self, parser):
        parser.add_argument("filename", type=str, help="Path to the TXT file")
        parser.add_argument(
            "--chunk_size",
            type=int,
            default=self.default_chunk_size,
            help=f"Number of rows to process at a time (default: {self.default_chunk_size})",
        )

    def handle(self, *_, **kwargs):
        filename = kwargs["filename"]
        chunk_size = kwargs["chunk_size"]

        command_run = get_file_processing_status(filename=filename)
        if command_run and command_run.status == CollectionCommandRunStatus.SUCCESS:
            logger.info(f"File {filename} has already been processed successfully")
            return

        try:
            command_run = set_file_processing_status(filename)
            with connection.cursor() as cursor:
                for lines_loaded in load_nginx_logs(filename=filename, chunk_size=chunk_size, cursor=cursor):
                    logger.info(f"Loaded {lines_loaded} lines")
        except Exception as e:
            command_run.set_failed(str(e))
            logger.exception(f"Failed to load data from {filename}")
        else:
            command_run.set_success()
            logger.info(f"Successfully loaded data from {filename}")
