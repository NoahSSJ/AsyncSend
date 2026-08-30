from core.crypto import MyAES
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

class InitFile():
    @staticmethod
    def init(key: str):
        aes = MyAES(
            key=key,
            iv="abcdef1234567890",
            mode="CBC"
        )
        input_file = (Path(__file__).parent / "backup").joinpath('bk.aes')
        output_file = (Path(__file__).parent / "core").joinpath('send_tmp.py')
        aes.decrypt_file(input_file=input_file, output_file=output_file)

    @staticmethod
    def encrypt_file(key: str):
        aes = MyAES(
            key=key,
            iv="abcdef1234567890",
            mode="CBC"
        )
        input_file = (Path(__file__).parent / "core" ).joinpath('send.py')
        output_file = (Path(__file__).parent / "backup").joinpath('bk.aes')
        aes.encrypt_file(input_file=input_file, output_file=output_file)



