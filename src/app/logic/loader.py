import logging
from collections.abc import Generator
from io import BytesIO

import polars as pl
from psycopg.cursor import Cursor

from app.models import CollectionCommandRun, NginxLog

logger = logging.getLogger(__name__)


def set_file_processing_status(filename: str) -> CollectionCommandRun:
    """
    Set the status of the file processing to IN_PROGRESS.

    Args:
    ----
        filename (str): The name of the file being processed.

    Returns:
    -------
        CollectionCommandRun: created file processing model instance.

    """

    return CollectionCommandRun.objects.create(filename=filename)


def get_file_processing_status(filename: str) -> CollectionCommandRun:
    """
    Get the last status of the file processing.

    Args:
    ----
        filename (str): The name of the file being processed.

    Returns:
    -------
        CollectionCommandRun: state of file processing.

    """

    return CollectionCommandRun.objects.order_by("-created_at").filter(filename=filename).first()


def load_nginx_logs(*, filename: str, chunk_size: int, cursor: Cursor) -> Generator[int, None, None]:
    """
    Load nginx logs from a file into a database table.

    Args:
    ----
        filename (str): The path to the file containing the nginx logs.
        chunk_size (int): The number of rows to process at a time.
        cursor (Cursor): The database cursor used for executing queries.


    Yields:
    ------
        int: The number of lines loaded in each iteration.

    """

    logger.info(f"Loading nginx logs from {filename}")
    scan_df = pl.scan_ndjson(filename, infer_schema_length=10, low_memory=True).with_columns(
        pl.col("time").str.strptime(pl.Datetime, "%d/%b/%Y:%H:%M:%S %z", strict=False)
    )

    for chunk in scan_df.collect(streaming=True).iter_slices(chunk_size):
        with cursor.copy(
            f"""
                COPY {NginxLog._meta.db_table}
                (time, remote_ip, remote_user, request, response, bytes, referrer, agent)
                FROM STDIN
            """,  # noqa: SLF001
        ) as copy:
            output = BytesIO()
            chunk.write_csv(output, include_header=False, separator="\t")
            output.seek(0)
            copy.write(output.getvalue())
        yield chunk.shape[0]
    else:
        logger.info("Logs loaded successfully")
