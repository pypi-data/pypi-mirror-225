import os
import shutil
import subprocess
from pathlib import Path
from typing import List


class ProtoBuild:
    """
    This command automatically compiles all .proto files with `protoc` compiler
    and places generated files near them -- i.e. in the same directory.
    """

    PROTOBUFF_COMPILER_ENV = "PROTOC"
    PROTOBUFF_COMPILER_EXECUTABLE = "protoc"
    PROTOBUFF_PROTO_FILE_SUFFIX = ".proto"
    PROTOBUFF_COMPILED_FILE_SUFFIX = "_pb2.py"
    PYTHON_FILE_SUFFIX = ".py"

    def __init__(self, proto_files: List[str]) -> None:
        """
        :param proto_files: Paths of proto files
        :type proto_files: List[str]
        """
        self.proto_files = proto_files

    def find_protoc_complier(self) -> str:
        """Locates protoc executable

        :raises Exception: if protoc is not found
        :return: protoc path
        :rtype: str
        """
        if self.PROTOBUFF_COMPILER_ENV in os.environ and os.path.exists(
            os.environ[self.PROTOBUFF_COMPILER_ENV]
        ):
            protoc = os.environ[self.PROTOBUFF_COMPILER_ENV]
        else:
            protoc = shutil.which(self.PROTOBUFF_COMPILER_EXECUTABLE)

        if not protoc:
            raise Exception(  # pylint: disable=broad-exception-raised
                "protoc not found. Is protobuf-compiler installed? \n"
                "Alternatively, you can point the PROTOC environment variable at a local version."
            )
        return protoc

    def run(self) -> None:
        """Compile all .proto files"""
        for proto_file in self.proto_files:
            print(f"Protobuf-compiling {proto_file}")
            proto_file_path = Path(proto_file)
            proto_file_directory = proto_file_path.parent
            subprocess.check_call(
                [
                    self.find_protoc_complier(),
                    f"--proto_path={proto_file_directory}",
                    f"--python_betterproto_out={proto_file_directory}",
                    proto_file,
                ]
            )
