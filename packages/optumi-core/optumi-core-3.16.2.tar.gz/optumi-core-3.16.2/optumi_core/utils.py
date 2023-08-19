##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
##


import os, hashlib

from pathlib import Path

from ._version import __version__

dev_version = "a" in __version__.lower()

split_version = __version__.split(".")
jupyterlab_major = split_version[0]
optumi_major = split_version[1]


# Get a windows path in a format we can use on linux
def split_drive(path):
    # Split the path and return drive, path tuple
    # Normalize the path first just to make sure we have the right format
    return os.path.splitdrive(normalize_path(path))


def hash_file(fileName):
    if os.path.isfile(fileName):
        BLOCKSIZE = 65536
        hasher = hashlib.md5()
        with open(fileName, "rb") as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)
        return hasher.hexdigest().upper()
    return None


def normalize_path(path, strict=True):
    if not path:
        if strict:
            raise FileNotFoundError("Path is empty")
        else:
            return path

    # Expand "~" and relative paths
    # Retrieve correct case from file system in windows paths
    # Replace "\" with "/"
    # strict=True will throw an exception if the file does not exist
    return str(Path(path).expanduser().resolve(strict=strict)).replace("\\", "/")

def expand_path(path: str):
    expanded = []
    normalized_path = normalize_path(path)
    if not os.path.isfile(normalized_path):
        # this is a directory that needs to be expanded
        for path in Path(normalized_path).rglob("*"):
            if os.path.isfile(path): # rglob returns directories as well as files
                expanded.append(path)
    else:
        expanded.append(normalized_path)
    return expanded

def replace_home_with_tilde(path, strict=True):
    # Normalize the path first just to make sure we have the right format
    return normalize_path(path).replace(normalize_path(os.path.expanduser("~"), strict), "~")


def hash_string(string):
    hasher = hashlib.md5()
    hasher.update(string)
    return hasher.hexdigest().upper()


def is_dynamic():
    return "OPTUMI_DSP" in os.environ


def get_portal():
    return "ds.optumi.net" if is_dynamic() else ("portal" + jupyterlab_major + (optumi_major if len(optumi_major) == 2 else "0" + optumi_major) + ".optumi.net")


def get_portal_port():
    return int(os.environ["OPTUMI_DSP"]) if is_dynamic() else 8443


def get_portal_domain_and_port():
    return get_portal() + ":" + str(get_portal_port())
