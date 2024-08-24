import random
from datetime import datetime

import polars as pl
from faker import Faker

# Initialize Faker for generating random data
faker = Faker()

# Define the size of the data to generate
target_size_mb = 100  # Target size in MB
approx_row_size_bytes = 200  # Approximate size of one row in bytes
total_rows = (target_size_mb * 1024 * 1024) // approx_row_size_bytes


# Function to generate a random IP address
def random_ip():
    return faker.ipv4()


# Function to generate a random request
def random_request():
    products = [f"product_{i}" for i in range(1, 101)]
    return f"GET /downloads/{random.choice(products)} HTTP/1.1"  # noqa: S311


# Function to generate a random timestamp
def random_timestamp():
    start = datetime(2022, 1, 1)  # noqa: DTZ001
    end = datetime(2023, 12, 31)  # noqa: DTZ001
    return faker.date_time_between(start_date=start, end_date=end).strftime("%d/%b/%Y:%H:%M:%S +0000")


# Function to generate a random log entry
def generate_log_entry():
    return {
        "time": random_timestamp(),
        "remote_ip": random_ip(),
        "remote_user": "-",
        "request": random_request(),
        "response": random.choice([200, 301, 302, 404, 500, 304]),  # noqa: S311
        "bytes": random.randint(0, 10000),  # noqa: S311
        "referrer": "-",
        "agent": faker.user_agent(),
    }


# Generate the data
rows = [generate_log_entry() for _ in range(total_rows)]

# Convert to Polars DataFrame
data_df = pl.DataFrame(rows)

# Write to a text file in NDJSON format (each row as a separate JSON object)
output_file = "random_nginx_logs.txt"
data_df.write_ndjson(output_file)

print(f"Generated {total_rows} rows of data and saved to {output_file}")  # noqa: T201
