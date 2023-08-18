import multiprocessing
import os
import uuid
from functools import partial
from multiprocessing import Pool
from typing import Dict, List, Optional

import fsspec
import pandas as pd
import requests
from loguru import logger
from tqdm import tqdm


def get_uid_from_str(string: str) -> str:
    """Generates a UUID from a string.

    Args:
        string (str): String to generate a UUID from.

    Returns:
        str: UUID generated from the string.
    """
    namespace = uuid.NAMESPACE_DNS
    return str(uuid.uuid5(namespace, string))


def load_smithsonian_metadata(
    download_dir: str = "~/.objaverse-xl",
) -> pd.DataFrame:
    """Loads the Smithsonian Object Metadata dataset as a Pandas DataFrame.

    Args:
        download_dir (str, optional): Directory to download the parquet metadata file.
            Supports all file systems supported by fsspec. Defaults to
            "~/.objaverse-xl".

    Returns:
        pd.DataFrame: Smithsonian Object Metadata dataset as a Pandas DataFrame with
            columns for the object "title", "url", "quality", "file_type", "uid", and
            "license". The quality is always Medium and the file_type is always glb.
    """
    dirname = os.path.expanduser(os.path.join(download_dir, "smithsonian"))
    filename = os.path.join(dirname, "object-metadata.parquet")
    fs, path = fsspec.core.url_to_fs(filename)
    if fs.protocol == "file":
        os.makedirs(dirname, exist_ok=True)

    if fs.exists(filename):
        df = pd.read_parquet(filename)
        return df
    else:
        url = "https://huggingface.co/datasets/allenai/objaverse-xl/resolve/main/smithsonian/object-metadata.parquet"
        response = requests.get(url)
        response.raise_for_status()
        with fs.open(filename, "wb") as file:
            file.write(response.content)
        df = pd.read_parquet(filename)

    df["uid"] = df["url"].apply(get_uid_from_str)
    df["license"] = "CC0"
    return df


def download_smithsonian_object(url: str, download_dir: str = "~/.objaverse-xl") -> str:
    """Downloads a Smithsonian Object from a URL.

    Args:
        url (str): URL to download the Smithsonian Object from.
        download_dir (str, optional): Directory to download the Smithsonian Object to.
            Supports all file systems supported by fsspec. Defaults to
            "~/.objaverse-xl".

    Returns:
        str: Path to the downloaded Smithsonian Object.
    """
    uid = get_uid_from_str(url)

    dirname = os.path.expanduser(os.path.join(download_dir, "smithsonian", "objects"))
    filename = os.path.join(dirname, f"{uid}.glb")
    fs, path = fsspec.core.url_to_fs(filename)
    if fs.protocol == "file":
        os.makedirs(dirname, exist_ok=True)

    if not fs.exists(filename):
        tmp_path = os.path.join(dirname, f"{uid}.glb.tmp")
        response = requests.get(url)

        # check if the path is valid
        if response.status_code == 404:
            logger.warning(f"404 for {url}")
            return None

        # write to tmp path
        with fs.open(tmp_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        # rename to final path
        fs.rename(tmp_path, filename)

    return filename


def download_smithsonian_objects(
    urls: Optional[str] = None,
    processes: Optional[int] = None,
    download_dir: str = "~/.objaverse-xl",
) -> List[Dict[str, str]]:
    """Downloads all Smithsonian Objects.

    Args:
        urls (Optional[str], optional): List of URLs to download the Smithsonian Objects
            from. If None, all Smithsonian Objects will be downloaded. Defaults to None.
        processes (Optional[int], optional): Number of processes to use for downloading
            the Smithsonian Objects. If None, the number of processes will be set to the
            number of CPUs on the machine (multiprocessing.cpu_count()). Defaults to
            None.
        download_dir (str, optional): Directory to download the Smithsonian Objects to.
            Supports all file systems supported by fsspec. Defaults to
            "~/.objaverse-xl".

    Returns:
        List[Dict[str, str]]: List of dictionaries with keys "download_path" and "url"
            for each downloaded object.
    """
    if processes is None:
        processes = multiprocessing.cpu_count()
    if urls is None:
        df = load_smithsonian_metadata(download_dir=download_dir)
        urls = df["url"].tolist()

    logger.info(f"Downloading {len(urls)} Smithsonian Objects with {processes=}")
    with Pool(processes=processes) as pool:
        results = list(
            tqdm(
                pool.imap_unordered(
                    partial(download_smithsonian_object, download_dir=download_dir),
                    urls,
                ),
                total=len(urls),
                desc="Downloading Smithsonian Objects",
            )
        )
    out = [
        {"download_path": download_path, "url": url}
        for download_path, url in zip(results, urls)
        if download_path is not None
    ]
    return out
