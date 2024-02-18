from pathlib import Path
import subprocess
import os
import shutil

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

    shutil.rmtree("py_generated")

if __name__ == "__main__":
    main()