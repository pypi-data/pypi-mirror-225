from collections import OrderedDict
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
from typing import Dict, List, Optional, Tuple, Union

_WORKING_DIR = None


def ensure_dir(dirname):
    dirname = Path(dirname)
    if not dirname.is_dir():
        dirname.mkdir(parents=True, exist_ok=False)


def is_non_zero_file(path: Path) -> bool:
    """Check if file exists and is non-empty.

    Args:
        path (Path): file-path.

    Returns:
        bool: True if file is non-zero.
    """
    return path.is_file() and os.path.getsize(path) > 0


def read_json(fname):
    fname = Path(fname)
    with fname.open("rt") as handle:
        return json.load(handle, object_hook=OrderedDict)


def write_json(content, fname):
    fname = Path(fname)
    with fname.open("wt") as handle:
        json.dump(content, handle, indent=4, sort_keys=False)


def download_url(url, output_path, tmp_path=None, extract_archive=False):
    """
    Download a file from a given url and store it in the specified path.

    :param url: url to download
    :param output_path: path to store the downloaded file
    :param tmp_path: path to the temporary file where the downloaded file is stored before extraction
    :param extract_archive: whether to extract the downloaded file
    """
    import logging
    from os import remove
    import urllib.request
    import zipfile

    from tqdm import tqdm

    class DownloadProgressBar(tqdm):
        def update_to(self, b=1, bsize=1, tsize=None):
            if tsize is not None:
                self.total = tsize
            self.update(b * bsize - self.n)

    logging.info("Downloading from {}".format(url))
    filename = tmp_path if extract_archive else output_path
    with DownloadProgressBar(
        unit="B", unit_scale=True, miniters=1, desc=f"Downloading {url}"
    ) as t:
        tmp_path, _ = urllib.request.urlretrieve(
            url, filename=filename, reporthook=t.update_to
        )
    logging.info("File stored at {}".format(tmp_path))
    if extract_archive:
        logging.info("Extracting {} to {}".format(tmp_path, output_path))
        with zipfile.ZipFile(tmp_path) as zf:
            for member in tqdm(zf.infolist(), desc="Extracting"):
                try:
                    zf.extract(member, output_path)
                except zipfile.error as e:
                    pass
        remove(tmp_path)


def __approx_md5__(path: Path, n_blocks=20, block_size=2**12) -> str:
    m = hashlib.md5()

    with open(path, "rb") as f:
        f.seek(0, os.SEEK_END)
        file_size = f.tell()

        # np.linspace might overflow for large files, standard python int is safer
        start_positions = [
            int(file_size * i / (n_blocks - 1)) for i in range(n_blocks)
        ]  # linearly spaced start positions
        _last_pos = -1  # for early stopping

        for start_pos in start_positions:
            end_pos = start_pos + block_size
            if end_pos > file_size:
                start_pos = max(0, file_size - block_size)
                end_pos = file_size

            if start_pos == _last_pos:
                break  # avoid reading the same block twice

            f.seek(start_pos)  # seek to start position

            _block_size = (
                end_pos - start_pos
            )  # actual block size (might be smaller than block_size)
            buf = f.read(_block_size)  # read block

            m.update(buf)  # update hash

            _last_pos = start_pos

    return m.hexdigest()


def checksum(path: Path) -> str:
    """Return unique ID for the given path. The ID is computed by
    hashing some parts of the file and appending the file-size.
    The runtime of this function is independent of the file-size and only depends on the number of blocks and the block-size.

    Note: This is not a cryptographic hash-function and should not be used as such.

    Args:
        path (Path): Location of the file.
    Returns:
        str: Hash-value computed for the specified file.
    """
    if is_non_zero_file(path):
        _md5 = __approx_md5__(path)
        _size = os.path.getsize(path)
        res = f"{_md5}_{_size}B"
        return res
    else:
        raise FileNotFoundError(f"File {path} does not exist or is empty.")


def setup_working_dir(path: Union[str, Path]) -> Path:
    """Initialize the working directory.

    Args:
        path (Union[str, Path]): Path to the working directory.

    Returns:
        Path: Path to the working directory.
    """
    path = Path(path)

    ensure_dir(path)
    ensure_dir(path / "cache")
    ensure_dir(path / "models")
    ensure_dir(path / "logs")
    ensure_dir(path / "tmp")

    global _WORKING_DIR
    _WORKING_DIR = path

    return path


def _clear_directory(path: Union[str, Path]):
    """Clear the directory.

    Args:
        path (Union[str, Path]): Path to the directory.
    """
    path = Path(path)
    for f in path.glob("*"):
        if f.is_file():
            f.unlink()
        elif f.is_dir():
            shutil.rmtree(f)


def clear_temporary_files():
    """Clear the temporary files.

    Args:
        path (Union[str, Path]): Path to the working directory.
    """
    path = get_working_dir()
    _clear_directory(path / "tmp")


def get_working_dir():
    """Get the working directory.

    Returns:
        Path: Path to the working directory.
    """
    return _WORKING_DIR
