#!/usr/bin/env python3.9
# coding:utf-8
# Copyright (C) 2023 All rights reserved.
# FILENAME:    ~~/protoc.py
# VERSION: 	   0.1.0
# CREATED: 	   2023-10-06 08:59
# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>
# DESCRIPTION:
#
# HISTORY:
# *************************************************************

### Standard packages ###
from os import mkdir, remove, rmdir, walk
from os.path import exists, join
from typing import List

### Third-party packages
from grpc_tools.protoc import main as compile
from pendulum import now


def recursive_remove(directory: str) -> None:
    if exists(directory):
        for root, dirs, files in walk(directory):
            list(map(lambda file: remove(join(root, file)), files))
            list(map(lambda dir: recursive_remove(join(root, dir)), dirs))
        rmdir(directory)


def main() -> None:
    target_dir: str = "src/protos"
    recursive_remove(target_dir)
    mkdir(target_dir)

    compile_args: List[str] = [
        "--proto_path=src",
        "--grpc_python_out=src",
        "--python_out=src",
        "protos/lightning.proto",
    ]
    compile(compile_args)
    compile_args = [
        "--proto_path=src",
        "--grpc_python_out=src",
        "--python_out=src",
        "protos/signer.proto",
    ]
    compile(compile_args)
    compile_args = [
        "--proto_path=src",
        "--grpc_python_out=src",
        "--python_out=src",
        "protos/walletkit.proto",
    ]
    compile(compile_args)

    with open(f"./{ target_dir }/__init__.py", "w+") as f:
        f.write("#!/usr/bin/env python3.9\n")
        f.write("# coding:utf-8\n")
        f.write("# Copyright (C) 2023 All rights reserved.\n")
        f.write("# FILENAME:    ~~/src/protos/__init__.py\n")
        f.write("# VERSION: 	   0.1.0\n")
        f.write(f"# CREATED: 	   { now().format('YYYY-MM-DD HH:mm') }\n")  # type: ignore[no-untyped-call]
        f.write("# AUTHOR: 	   Sitt Guruvanich <aekazitt+github@gmail.com>\n")
        f.write("# DESCRIPTION:\n")
        f.write("#\n")
        f.write("# HISTORY:\n")
        f.write("# *************************************************************\n")

    old_text: str = ""
    with open(f"./{ target_dir }/lightning_pb2_grpc.py", "rt") as ink:
        old_text = ink.read()
    with open(f"./{ target_dir }/lightning_pb2_grpc.py", "wt") as quill:
        new_text: str = old_text.replace("from protos", "from src.protos")
        quill.write(new_text)
    with open(f"./{ target_dir }/signer_pb2_grpc.py", "rt") as ink:
        old_text = ink.read()
    with open(f"./{ target_dir }/signer_pb2_grpc.py", "wt") as quill:
        new_text: str = old_text.replace("from protos", "from src.protos")
        quill.write(new_text)
    with open(f"./{ target_dir }/walletkit_pb2_grpc.py", "rt") as ink:
        old_text = ink.read()
    with open(f"./{ target_dir }/walletkit_pb2_grpc.py", "wt") as quill:
        new_text: str = old_text.replace("from protos", "from src.protos")
        quill.write(new_text)


if __name__ == "__main__":
    main()
