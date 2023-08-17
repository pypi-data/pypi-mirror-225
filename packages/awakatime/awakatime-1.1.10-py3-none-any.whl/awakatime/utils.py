from base64 import b64encode


def encode_base64(string: str) -> str:
    string_bytes = string.encode()
    base64_bytes = b64encode(string_bytes)
    return base64_bytes.decode()
