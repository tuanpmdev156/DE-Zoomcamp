import time
import duckdb
import requests
from pathlib import Path
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"

# Give up on a connection that stalls instead of crawling forever:
# 10s to connect, 30s without receiving any bytes.
TIMEOUT = (10, 30)
MAX_ATTEMPTS = 5

def make_session():
    session = requests.Session()
    retry = Retry(
        total=MAX_ATTEMPTS,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session

def download(session, url, dest):
    """Download to a .part file, then rename, so an interrupted run never
    leaves a truncated file that looks complete."""
    part = dest.with_suffix(dest.suffix + ".part")

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            with session.get(url, stream=True, timeout=TIMEOUT) as response:
                response.raise_for_status()
                total = int(response.headers.get("Content-Length", 0))

                downloaded = 0
                last_log = time.monotonic()
                started = last_log

                with open(part, "wb") as f:
                    for chunk in response.iter_content(chunk_size=1024 * 256):
                        f.write(chunk)
                        downloaded += len(chunk)

                        now = time.monotonic()
                        if now - last_log >= 5:
                            mb = downloaded / 1024 / 1024
                            speed = downloaded / 1024 / 1024 / (now - started)
                            pct = f" ({downloaded * 100 // total}%)" if total else ""
                            print(f"    {mb:.1f} MB{pct} at {speed:.2f} MB/s", flush=True)
                            last_log = now

            if total and downloaded != total:
                raise IOError(f"incomplete: got {downloaded} of {total} bytes")

            part.rename(dest)
            return

        except (requests.RequestException, IOError) as e:
            part.unlink(missing_ok=True)
            if attempt == MAX_ATTEMPTS:
                raise
            wait = 2 ** attempt
            print(f"    attempt {attempt} failed ({e}); retrying in {wait}s", flush=True)
            time.sleep(wait)

def download_and_convert_files(session, taxi_type):
    data_dir = Path("data") / taxi_type
    data_dir.mkdir(exist_ok=True, parents=True)

    for year in [2019, 2020]:
        for month in range(1, 13):
            parquet_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
            parquet_filepath = data_dir / parquet_filename

            if parquet_filepath.exists():
                print(f"Skipping {parquet_filename} (already exists)", flush=True)
                continue

            csv_gz_filename = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
            csv_gz_filepath = data_dir / csv_gz_filename

            print(f"Downloading {csv_gz_filename}...", flush=True)
            download(session, f"{BASE_URL}/{taxi_type}/{csv_gz_filename}", csv_gz_filepath)

            print(f"Converting {csv_gz_filename} to Parquet...", flush=True)
            con = duckdb.connect()
            con.execute(f"""
                COPY (SELECT * FROM read_csv_auto('{csv_gz_filepath}'))
                TO '{parquet_filepath}' (FORMAT PARQUET)
            """)
            con.close()

            # Remove the CSV.gz file to save space
            csv_gz_filepath.unlink()
            print(f"Completed {parquet_filename}", flush=True)

def update_gitignore():
    gitignore_path = Path(".gitignore")

    # Read existing content or start with empty string
    content = gitignore_path.read_text() if gitignore_path.exists() else ""

    # Add data/ if not already present
    if 'data/' not in content:
        with open(gitignore_path, 'a') as f:
            f.write('\n# Data directory\ndata/\n' if content else '# Data directory\ndata/\n')

if __name__ == "__main__":
    # Update .gitignore to exclude data directory
    update_gitignore()

    session = make_session()
    for taxi_type in ["yellow", "green"]:
        download_and_convert_files(session, taxi_type)

    con = duckdb.connect("taxi_rides_ny.duckdb")
    con.execute("CREATE SCHEMA IF NOT EXISTS prod")

    for taxi_type in ["yellow", "green"]:
        print(f"Loading prod.{taxi_type}_tripdata...", flush=True)
        con.execute(f"""
            CREATE OR REPLACE TABLE prod.{taxi_type}_tripdata AS
            SELECT * FROM read_parquet('data/{taxi_type}/*.parquet', union_by_name=true)
        """)

    con.close()
    print("Done.", flush=True)
