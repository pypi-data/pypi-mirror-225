# Copyright Log10, Inc 2023

import logging
import os
from pathlib import Path
import shutil
import errno

import click

folder_name = "examples"


def copyExampleFolder(source: str, dest: str):
    try:
        if not Path(source).exists():
            print(f"The source directory is not existed: {source}")
            return
        os.makedirs(dest, exist_ok=True)
        shutil.copytree(source, dest, dirs_exist_ok=True)
        click.echo(f"Copied examples folder to {dest}.")
    except OSError as exc:
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(source, dest)
        else:
            print(exc.strerror)
