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
    proto_modules: str = "src/protos"
    recursive_remove(proto_modules)
    mkdir(proto_modules)

    for proto_path in {"chainkit", "invoices", "lightning", "signer", "walletkit"}:
        compile_args: List[str] = [
            "--proto_path=src",
            "--grpc_python_out=src",
            "--python_out=src",
            f"protos/{ proto_path }.proto",
        ]
        compile(compile_args)

    with open(f"./{ proto_modules }/__init__.py", "w+") as f:
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

    for module_path in {
        "chainkit_pb2_grpc",
        "invoices_pb2",
        "invoices_pb2_grpc",
        "lightning_pb2_grpc",
        "signer_pb2_grpc",
        "walletkit_pb2",
        "walletkit_pb2_grpc",
    }:
        old_text: str = ""
        with open(f"./{ proto_modules }/{ module_path }.py", "rt") as ink:
            old_text = ink.read()
        with open(f"./{ proto_modules }/{ module_path }.py", "wt") as quill:
            new_text: str = old_text.replace("from protos", "from src.protos")
            quill.write(new_text)


if __name__ == "__main__":
    main()
