import os
from pathlib import Path
import re
import subprocess
import datetime

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d")


def get_tcl_files(out_dir):
    output_file = os.path.join(out_dir, "tcl_interface_files.txt")
    output_stream = open(output_file, "w")
    print(f"{os.path.basename(__file__)}: Generating {output_file}")
    for root, subdir, files in os.walk("./src"):
        for file in files:
            if re.match(r"\./src/[A-z]+/src/[A-z]+\.tcl", os.path.join(root, file)):
                print(os.path.join(root, file), file=output_stream)
    return output_file


def generate_commands(files_list_file, output_dir):
    tcl_script = "./commands_to_tree.tcl"
    cmd = ["tclsh", tcl_script, files_list_file, output_dir]
    output = subprocess.run(cmd, stdout=subprocess.PIPE, encoding="utf-8")
    for line in output.stdout.split("\n"):
        print(f"{tcl_script}: {line}")


def get_output_dir():
    output_dir = f"commands/{now}_"
    output_dir += (
        subprocess.run(
            "git rev-parse --short HEAD".split(),
            encoding="utf-8",
            stdout=subprocess.PIPE,
        )
        .stdout.lstrip()
        .rstrip()
    )
    return output_dir


output_dir = get_output_dir()
Path(output_dir).mkdir(parents=True, exist_ok=True)
tcl_files_list = get_tcl_files(output_dir)
commands_dir = generate_commands(files_list_file=tcl_files_list, output_dir=output_dir)
