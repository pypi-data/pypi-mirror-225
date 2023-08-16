import base64
import zlib

UTF_8_ENCODING = "utf-8"


def decompress_data(data: str) -> bytes:
    return zlib.decompress(base64.b64decode(data))


def compress_data(data: bytes) -> str:
    return base64.b64encode(zlib.compress(data)).decode(UTF_8_ENCODING)
