# Copyright Log10, Inc 2023

import subprocess
import sys
import click

from pathlib import Path

from llmeval.utils import copyExampleFolder, folder_name


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--destination", default=".", help="The example folder is being copied to."
)
def init(destination):
    srcFolder = f"{Path(__file__).resolve().parent}/{folder_name}"
    destFolder = f"{Path(destination).resolve()}/{folder_name}"
    copyExampleFolder(srcFolder, destFolder)


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.option("--path", default=".", help="The config folder path.")
def run(path):
    config_path = folder_name
    if not path:
        config_path = path

    n_args = 1
    hydra_args = ",".join(sys.argv[n_args + 1 :])

    args = [
        "python",
        f'{Path("llmeval").resolve()}/eval.py',
        f"--config-path={Path(config_path).resolve()}",
    ]
    if hydra_args:
        args.append(f"{hydra_args}")

    subprocess.run(args)

    click.echo(f"Evaluation is completed.")


cli.add_command(init)
cli.add_command(run)
if __name__ == "__main__":
    cli()
