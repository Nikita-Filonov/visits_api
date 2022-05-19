import binascii
import os


async def generate_token():
    return binascii.hexlify(os.urandom(20)).decode()
