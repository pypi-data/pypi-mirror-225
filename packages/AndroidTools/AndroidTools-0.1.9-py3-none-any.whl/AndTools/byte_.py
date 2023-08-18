import hashlib
import random


def hexFormat(Hex):
    """Hex格式化"""
    Hex = ' '.join(Hex[i:i + 2] for i in range(0, len(Hex), 2))
    return Hex


def get_random_bin(len):
    byte = b""
    for _ in range(len):
        byte += bytes([random.randint(0, 255)])
    return byte


def get_md5(byte_content):
    md5_object = hashlib.md5()
    md5_object.update(byte_content)
    return md5_object.hexdigest()
