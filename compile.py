from pathlib import Path
import subprocess
import os
import shutil
import re

def get_protobuf_files() -> list[str]:
    return [str(path) for path in Path("messages").rglob("*.proto")]

def compile_protobuf_files(files: list[str]) -> None:
    for file in files:
        command = ["protoc", "--python_out=py_generated", "--mypy_out=py_generated", file]
        subprocess.check_call(command)

def rename_compiled_files() -> None:
    for file in Path("py_generated").rglob("*.py"):
        pyi_file = file.parent / file.name.replace(".py", ".pyi")
        shutil.move(file, Path("akatsuki_proto/messages") / file.name)
        shutil.move(pyi_file, Path("akatsuki_proto/messages") / pyi_file.name)

PY_PATTERN = r"from messages import ([a-z_0-9]+)_pb2 as ([a-z_0-9]+)__pb2"
PY_REPLACEMENT = r"from akatsuki_proto.messages import \g<1> as \g<2>"

BUILDER_PATTERN = r"('messages\.)([a-z_0-9]+)_pb2"
BUILDER_REPLACEMENT = r"\g<1>\g<2>"

PYI_PATTERN = r"(messages\.)([a-z_0-9]+)_pb2"
PYI_REPLACEMENT = r"akatsuki_proto.\g<1>\g<2>"

def fix_imports() -> None:
    for file in Path("akatsuki_proto/messages").rglob("*.py"):
        pyi_file = file.parent / file.name.replace(".py", ".pyi")
        if not pyi_file.exists():
            continue

        file = file.rename(file.parent / file.name.replace("_pb2", ""))
        pyi_file = pyi_file.rename(pyi_file.parent / pyi_file.name.replace("_pb2", ""))

        file_data = file.read_text()
        output_text = re.sub(PY_PATTERN, PY_REPLACEMENT, file_data)
        output_text = re.sub(BUILDER_PATTERN, BUILDER_REPLACEMENT, output_text)

        pyi_file_data = pyi_file.read_text()
        pyi_output_text = re.sub(PYI_PATTERN, PYI_REPLACEMENT, pyi_file_data)
    
        file.write_text(output_text)
        pyi_file.write_text(pyi_output_text)

def generate_python_folder() -> None:
    shutil.rmtree("akatsuki_proto", ignore_errors=True)

    os.makedirs("akatsuki_proto")
    os.makedirs("akatsuki_proto/messages")

    Path("akatsuki_proto/__init__.py").write_bytes(b"")
    Path("akatsuki_proto/messages/__init__.py").write_bytes(b"")

def main() -> None:
    files = get_protobuf_files()

    generate_python_folder()

    shutil.rmtree("py_generated", ignore_errors=True)
    os.makedirs("py_generated")

    compile_protobuf_files(files)
    rename_compiled_files()
    fix_imports()

    shutil.rmtree("py_generated")

if __name__ == "__main__":
    main()