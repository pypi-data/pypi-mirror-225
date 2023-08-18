import errno
import hashlib
import numbers
import os

import numpy as np
import requests
import torch as th


__all__ = [
    "download",
    "extract_archive",
    "get_download_dir",
    "makedirs",
    "generate_mask_tensor",
]

import warnings


def _get_eg_url(file_url):
    """Get EasyGraph online url for download."""
    eg_repo_url = "https://gitlab.com/easy-graph/"
    repo_url = os.environ.get("DGL_REPO", eg_repo_url)
    if repo_url[-1] != "/":
        repo_url = repo_url + "/"
    return repo_url + file_url


def _get_dgl_url(file_url):
    """Get DGL online url for download."""
    dgl_repo_url = "https://data.dgl.ai/"
    repo_url = os.environ.get("DGL_REPO", dgl_repo_url)
    if repo_url[-1] != "/":
        repo_url = repo_url + "/"
    return repo_url + file_url


def _set_labels(G, labels):
    index = 0
    for node in G.nodes:
        G.add_node(node, label=labels[index])
        index += 1
    return G


def _set_features(G, features):
    index = 0
    for node in G.nodes:
        G.add_node(node, feat=features[index])
        index += 1
    return G


def nonzero_1d(input):
    x = th.nonzero(input, as_tuple=False).squeeze()
    return x if x.dim() == 1 else x.view(-1)


def tensor(data, dtype=None):
    if isinstance(data, numbers.Number):
        data = [data]
    if isinstance(data, list) and len(data) > 0 and isinstance(data[0], th.Tensor):
        # prevent GPU->CPU->GPU copies
        if data[0].ndim == 0:
            # zero dimenion scalar tensors
            return th.stack(data)
    if isinstance(data, th.Tensor):
        return th.as_tensor(data, dtype=dtype, device=data.device)
    else:
        return th.as_tensor(data, dtype=dtype)


def data_type_dict():
    return {
        "float16": th.float16,
        "float32": th.float32,
        "float64": th.float64,
        "uint8": th.uint8,
        "int8": th.int8,
        "int16": th.int16,
        "int32": th.int32,
        "int64": th.int64,
        "bool": th.bool,
    }


def download(
    url,
    path=None,
    overwrite=True,
    sha1_hash=None,
    retries=5,
    verify_ssl=True,
    log=True,
):
    """Download a given URL.

    Codes borrowed from mxnet/gluon/utils.py

    Parameters
    ----------
    url : str
        URL to download.
    path : str, optional
        Destination path to store downloaded file. By default stores to the
        current directory with the same name as in url.
    overwrite : bool, optional
        Whether to overwrite the destination file if it already exists.
        By default always overwrites the downloaded file.
    sha1_hash : str, optional
        Expected sha1 hash in hexadecimal digits. Will ignore existing file when hash is specified
        but doesn't match.
    retries : integer, default 5
        The number of times to attempt downloading in case of failure or non 200 return codes.
    verify_ssl : bool, default True
        Verify SSL certificates.
    log : bool, default True
        Whether to print the progress for download

    Returns
    -------
    str
        The file path of the downloaded file.
    """
    if path is None:
        fname = url.split("/")[-1]
        # Empty filenames are invalid
        assert fname, (
            "Can't construct file-name from this URL. "
            "Please set the `path` option manually."
        )
    else:
        path = os.path.expanduser(path)
        if os.path.isdir(path):
            fname = os.path.join(path, url.split("/")[-1])
        else:
            fname = path
    assert retries >= 0, "Number of retries should be at least 0"

    if not verify_ssl:
        warnings.warn(
            "Unverified HTTPS request is being made (verify_ssl=False). "
            "Adding certificate verification is strongly advised."
        )

    if (
        overwrite
        or not os.path.exists(fname)
        or (sha1_hash and not check_sha1(fname, sha1_hash))
    ):
        dirname = os.path.dirname(os.path.abspath(os.path.expanduser(fname)))
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        while retries + 1 > 0:
            # Disable pyling too broad Exception
            # pylint: disable=W0703
            try:
                if log:
                    print("Downloading %s from %s..." % (fname, url))
                r = requests.get(url, stream=True, verify=verify_ssl)
                if r.status_code != 200:
                    raise RuntimeError("Failed downloading url %s" % url)
                with open(fname, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                if sha1_hash and not check_sha1(fname, sha1_hash):
                    raise UserWarning(
                        "File {} is downloaded but the content hash does not match."
                        " The repo may be outdated or download may be incomplete. "
                        'If the "repo_url" is overridden, consider switching to '
                        "the default repo.".format(fname)
                    )
                break
            except Exception as e:
                retries -= 1
                if retries <= 0:
                    raise e
                else:
                    if log:
                        print(
                            "download failed, retrying, {} attempt{} left".format(
                                retries, "s" if retries > 1 else ""
                            )
                        )

    return fname


def extract_archive(file, target_dir, overwrite=False):
    """Extract archive file.

    Parameters
    ----------
    file : str
        Absolute path of the archive file.
    target_dir : str
        Target directory of the archive to be uncompressed.
    overwrite : bool, default True
        Whether to overwrite the contents inside the directory.
        By default always overwrites.
    """
    if os.path.exists(target_dir) and not overwrite:
        return
    print("Extracting file to {}".format(target_dir))
    if file.endswith(".tar.gz") or file.endswith(".tar") or file.endswith(".tgz"):
        import tarfile

        with tarfile.open(file, "r") as archive:
            archive.extractall(path=target_dir)
    elif file.endswith(".gz"):
        import gzip
        import shutil

        with gzip.open(file, "rb") as f_in:
            target_file = os.path.join(target_dir, os.path.basename(file)[:-3])
            with open(target_file, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
    elif file.endswith(".zip"):
        import zipfile

        with zipfile.ZipFile(file, "r") as archive:
            archive.extractall(path=target_dir)
    else:
        raise Exception("Unrecognized file type: " + file)


def get_download_dir():
    """Get the absolute path to the download directory.

    Returns
    -------
    dirname : str
        Path to the download directory
    """
    default_dir = os.path.join(os.path.expanduser("~"), ".EasyGraphData")
    dirname = os.environ.get("EG_DOWNLOAD_DIR", default_dir)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname


def makedirs(path):
    try:
        os.makedirs(os.path.expanduser(os.path.normpath(path)))
    except OSError as e:
        if e.errno != errno.EEXIST and os.path.isdir(path):
            raise e


def check_sha1(filename, sha1_hash):
    """Check whether the sha1 hash of the file content matches the expected hash.

    Codes borrowed from mxnet/gluon/utils.py

    Parameters
    ----------
    filename : str
        Path to the file.
    sha1_hash : str
        Expected sha1 hash in hexadecimal digits.

    Returns
    -------
    bool
        Whether the file content matches the expected hash.
    """
    sha1 = hashlib.sha1()
    with open(filename, "rb") as f:
        while True:
            data = f.read(1048576)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest() == sha1_hash


def generate_mask_tensor(mask):
    """Generate mask tensor according to different backend
    For torch, it will create a bool tensor
    Parameters
    ----------
    mask: numpy ndarray
        input mask tensor
    """
    assert isinstance(
        mask, np.ndarray
    ), "input for generate_mask_tensorshould be an numpy ndarray"
    return tensor(mask, dtype=data_type_dict()["bool"])


def deprecate_property(old, new):
    warnings.warn(
        "Property {} will be deprecated, please use {} instead.".format(old, new)
    )
