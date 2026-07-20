import importlib.util
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

import httpx
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

# Placeholder or import for notify if it lives elsewhere,
# though it's defined at the bottom.


def download(
    url: str,
    filename: str,
    verify: bool = True,
    notify_flag: bool = False,
    timeout: int = 60,
    progress: Optional[Progress] = None,
) -> None:
    """
    Pulls a file from a URL and saves it in the filename using httpx and rich.
    """
    # Use a local progress bar if a global one wasn't passed in
    progress = Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
    )
    progress.start()
    local_progress = True

    try:
        # Added follow_redirects=True here to automatically follow HTTP 302 redirects
        with httpx.Client(
            verify=verify, follow_redirects=True, timeout=timeout
        ) as client:
            with client.stream("GET", url) as response:
                response.raise_for_status()
                total_size = int(response.headers.get("content-length", 0))

                task_id = progress.add_task(
                    description=f"Downloading {os.path.basename(filename)}",
                    total=total_size if total_size > 0 else None,
                )

                with open(filename, "wb") as file:
                    for chunk in response.iter_bytes(chunk_size=1024 * 1024):
                        file.write(chunk)
                        progress.update(task_id, advance=len(chunk))
    finally:
        if local_progress:
            progress.stop()

    if notify_flag:
        notify(
            url=str(os.environ.get("URL")),
            auth=str(os.environ.get("AUTH")),
            msg=f"Successfully downloaded {filename} from {url}",
        )


def parse_download(
    url: str,
    filename: str,
    verify: bool = True,
    notify_flag: bool = False,
    progress: Optional[Progress] = None,
) -> None:
    """
    Downloads a CSV file from a given URL, parses it with Polars, and saves it as a Parquet file.
    """
    if importlib.util.find_spec("polars") is None:
        raise ModuleNotFoundError("need to install extra packages (polars)")

    import polars as pl

    temp_filename = f"{tempfile.gettempdir()}/{hash(filename)}.csv"

    # Pass progress down to avoid breaking the UI layout
    download(url=url, filename=temp_filename, verify=verify, progress=progress)

    df = pl.read_csv(temp_filename, ignore_errors=True)
    if df.is_empty():
        print(filename)
        raise ValueError("File Did not download correctly")
    df.write_parquet(filename)

    if notify_flag:
        notify(
            url=str(os.environ.get("URL")),
            auth=str(os.environ.get("AUTH")),
            msg=f"Successfully parsed and saved {filename} from {url}",
        )


def batch_download(
    file_map: dict,
    max_workers: int = 4,
    verify: bool = True,
    notify_flag: bool = False,
    parse: bool = False,
):
    """
    Downloads multiple files concurrently, utilizing Rich's multi-progress bars.
    """
    if parse:
        if importlib.util.find_spec("polars") is None:
            raise ModuleNotFoundError("need to install extra packages (polars)")
        download_func = parse_download
    else:
        download_func = download

    # Manage a single Progress display context for all concurrent threads
    with Progress(
        TextColumn("[bold green]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
    ) as progress:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(
                    download_func, url, filename, verify, notify_flag, progress
                ): (url, filename)
                # Note: changed key-value order to match .items() unpacking order safely
                for url, filename in file_map.items()
            }

            for future in as_completed(futures):
                url, filename = futures[future]
                try:
                    future.result()
                except Exception as e:
                    progress.print(
                        f"[bold red]Failed to download {url}: {e}[/bold red]"
                    )


def notify(url: str, auth: str, msg: str):
    with httpx.Client() as client:
        client.post(
            url,
            content=msg,
            headers={"Authorization": auth},
        )
