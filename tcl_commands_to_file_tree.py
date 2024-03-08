import os
import re
import subprocess
import datetime

import click

from pathlib import Path

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d")


def get_tcl_files(openroad_directory, output_dir):
    output_file = os.path.join(output_dir, "tcl_interface_files.txt")
    output_stream = open(output_file, "w")
    print(f"{os.path.basename(__file__)}: Generating {output_file}")
    src_directory = os.path.join(openroad_directory, "src")
    print(f"{os.path.basename(__file__)}: Using {src_directory}")
    for root, subdir, files in os.walk(src_directory):
        for file in files:
            if re.match(
                rf"{src_directory}/[A-z]+/src/[A-z]+\.tcl", os.path.join(root, file)
            ):
                print(os.path.join(root, file), file=output_stream)
    return output_file


def generate_commands(files_list_file, output_dir):
    tcl_script = "./commands_to_file_tree.tcl"
    cmd = ["tclsh", tcl_script, files_list_file, output_dir]
    output = subprocess.run(cmd, stdout=subprocess.PIPE, check=True, encoding="utf-8")
    for line in output.stdout.split("\n"):
        print(f"{tcl_script}: {line}")


def get_hash(openroad_directory):
    hash = f"{now}_"
    command = f"git -C {openroad_directory} rev-parse --short HEAD"
    hash += (
        subprocess.run(
            command.split(),
            encoding="utf-8",
            stdout=subprocess.PIPE,
        )
        .stdout.lstrip()
        .rstrip()
    )
    return hash


@click.command()
@click.argument("openroad-directory", type=click.Path(exists=True, dir_okay=True))
@click.option("--output-dir", default=".", type=click.Path(file_okay=False))
def main(openroad_directory, output_dir):
    hash = get_hash(openroad_directory)
    output_dir = os.path.join(output_dir, hash)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    tcl_files_list = get_tcl_files(openroad_directory, output_dir=output_dir)
    generate_commands(files_list_file=tcl_files_list, output_dir=output_dir)


if __name__ == "__main__":
    main()
