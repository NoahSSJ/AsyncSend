import base64
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class MyAES:
    def __init__(self, key, iv="", text="", mode="CBC"):
        self.key = key
        self.iv = iv
        self.text = text
        self.mode = mode.upper()

        if self.mode not in ("CBC", "ECB"):
            raise ValueError("mode 只支持 CBC 或 ECB")

    def _get_key(self):
        """把密钥补齐到 AES 支持的 16、24 或 32 字节。"""
        key = self.key.encode("utf-8")

        if len(key) <= 16:
            return key.ljust(16, b"\x00")
        elif len(key) <= 24:
            return key.ljust(24, b"\x00")
        elif len(key) <= 32:
            return key.ljust(32, b"\x00")

        raise ValueError("UTF-8 编码后的密钥不能超过 32 字节")

    def _get_iv(self):
        """CBC 模式的 IV 必须正好为 16 字节。"""
        iv = self.iv.encode("utf-8")

        if len(iv) != AES.block_size:
            raise ValueError("CBC 模式的 IV 必须正好是 16 字节")

        return iv

    def _create_cipher(self):
        key = self._get_key()

        if self.mode == "CBC":
            return AES.new(key, AES.MODE_CBC, self._get_iv())

        return AES.new(key, AES.MODE_ECB)

    def encrypt(self, text=None):
        """
        加密字符串。

        返回：
            Base64 编码的字符串。
        """
        if text is None:
            text = self.text

        if not isinstance(text, str):
            raise TypeError("待加密内容必须是字符串")

        cipher = self._create_cipher()
        plaintext = text.encode("utf-8")
        encrypted = cipher.encrypt(pad(plaintext, AES.block_size))

        return base64.b64encode(encrypted).decode("utf-8")

    def decrypt(self, encrypted_text=None):
        """
        解密 Base64 字符串。

        返回：
            UTF-8 明文字符串。
        """
        if encrypted_text is None:
            encrypted_text = self.text

        if not isinstance(encrypted_text, (str, bytes)):
            raise TypeError("密文必须是 Base64 字符串或 bytes")

        try:
            encrypted_data = base64.b64decode(
                encrypted_text,
                validate=True
            )
        except Exception as exc:
            raise ValueError("密文不是有效的 Base64 数据") from exc

        if not encrypted_data or len(encrypted_data) % AES.block_size != 0:
            raise ValueError("AES 密文长度必须是 16 字节的整数倍")

        cipher = self._create_cipher()

        try:
            plaintext = unpad(
                cipher.decrypt(encrypted_data),
                AES.block_size
            )
            return plaintext.decode("utf-8")
        except (ValueError, UnicodeDecodeError) as exc:
            raise ValueError("解密失败，请检查密钥、IV、模式或密文") from exc

    def encrypt_file(self, input_file, output_file, chunk_size=1024 * 1024):
        """
        流式加密文件。

        输出文件为原始二进制密文，不进行 Base64 编码。
        """
        input_path = Path(input_file)
        output_path = Path(output_file)

        self._validate_file_paths(input_path, output_path)
        chunk_size = self._normalize_chunk_size(chunk_size)

        cipher = self._create_cipher()
        buffer = b""

        output_path.parent.mkdir(parents=True, exist_ok=True)

        with input_path.open("rb") as source, output_path.open("wb") as target:
            while chunk := source.read(chunk_size):
                buffer += chunk

                # 保留最后一部分数据，最后统一添加 PKCS#7 填充。
                process_length = (len(buffer) // AES.block_size) * AES.block_size

                if process_length:
                    target.write(cipher.encrypt(buffer[:process_length]))
                    buffer = buffer[process_length:]

            target.write(cipher.encrypt(pad(buffer, AES.block_size)))

        return str(output_path)

    def decrypt_file(self, input_file, output_file, chunk_size=1024 * 1024):
        """
        流式解密文件。

        输入文件应为 encrypt_file() 生成的二进制密文。
        """
        input_path = Path(input_file)
        output_path = Path(output_file)

        self._validate_file_paths(input_path, output_path)
        chunk_size = self._normalize_chunk_size(chunk_size)

        file_size = input_path.stat().st_size

        if file_size == 0 or file_size % AES.block_size != 0:
            raise ValueError("加密文件长度必须是 16 字节的整数倍")

        cipher = self._create_cipher()
        buffer = b""

        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with input_path.open("rb") as source, output_path.open("wb") as target:
                while chunk := source.read(chunk_size):
                    buffer += chunk

                    # 最后一个区块包含填充，必须留到循环结束后处理。
                    process_length = (
                        (len(buffer) - AES.block_size)
                        // AES.block_size
                        * AES.block_size
                    )

                    if process_length > 0:
                        target.write(cipher.decrypt(buffer[:process_length]))
                        buffer = buffer[process_length:]

                decrypted_last_block = cipher.decrypt(buffer)
                target.write(unpad(decrypted_last_block, AES.block_size))

        except ValueError as exc:
            # 避免保留解密失败后生成的不完整文件。
            output_path.unlink(missing_ok=True)
            raise ValueError(
                "文件解密失败，请检查密钥、IV、模式或文件内容"
            ) from exc

        return str(output_path)

    @staticmethod
    def _normalize_chunk_size(chunk_size):
        if not isinstance(chunk_size, int) or chunk_size <= 0:
            raise ValueError("chunk_size 必须是正整数")

        # 读取区块调整为 AES 区块大小的整数倍。
        return max(
            AES.block_size,
            chunk_size - chunk_size % AES.block_size
        )

    @staticmethod
    def _validate_file_paths(input_path, output_path):
        if not input_path.is_file():
            raise FileNotFoundError(f"输入文件不存在：{input_path}")

        if input_path.resolve() == output_path.resolve():
            raise ValueError("输入文件和输出文件不能是同一个文件")

