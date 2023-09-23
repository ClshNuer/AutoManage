#!/usr/bin/env python3
# -*- coding-utf-8 -*-

import os
import fire
from loguru import logger

import base64
import urllib.parse


class StrEncodeDecode(object):
    """
    A class that represents a IP address

    Example:
        python str_encode_decode.py
        # python str_encode_decode.py main
        # python3 str_encode_decode.py main --encoder_filepath /tmp/encoder.txt
        # python str_encode_decode.py encode_decode_str --string='abc' encoding_func=base64_encode
        # python str_encode_decode.py encode_decode_str --string='abc' encoding_func=base64_encode switch=False
    """
    def __init__(self, string = None, encoder_filepath = None, decoder_filepath = None):
        self.string = string
        self.encoder_filepath = encoder_filepath
        self.decoder_filepath = decoder_filepath

    def is_file_exists(self, filename):
        """
        判断文件是否存在
        """
        if not os.path.exists(filename):
            logger.warning(f"{filename} 文件不存在：")
            return False
        return True

    def read_file(self, filename):
        """
        读取文件中的字符串
        """
        if not self.is_file_exists(filename):
            return 
        try:
            with open(filename, 'r') as f:
                lines = [line.strip() for line in f]
        except Exception as e:
            logger.error(f"发生错误：{e}")
        return lines

    def encode_decode_str(self, encoding_func, switch = True):
        """
        对字符串进行 Base64 / URL / Chr 编码
        :param encoding_func: 编码函数类型
        :return: 编码后的字符串
        """
        try:
            return encoding_func(self.string)
        except (TypeError, UnicodeDecodeError) as e:
            if switch:
                logger.info('编码失败，请检查字符串是否正确')
            else:
                logger.info('解码失败，请检查字符串是否正确')
            logger.error(f'Error: {e}')
            return None

    def base64_encode(self):
        """
        对字符串进行 Base64 编码
        :return: 编码后的字符串
        """
        encoded_str = base64.b64encode(self.string.encode('utf-8'))
        return encoded_str.decode('utf-8')

    def url_encode(self):
        """
        对字符串进行 URL 编码
        :return: 编码后的字符串
        """
        encoded_str = urllib.parse.quote(self.string.encode('utf-8'))
        return encoded_str

    def chr_encode(self):
        """
        对字符串进行 Chr 编码
        :return: 编码后的字符串
        """
        encoded_str = ''
        for i in self.string:
            # 编码后的格式 string = 'Chr(64).Chr(105).Chr(110).Chr(105)'
            encoded_str += 'Chr(' + self.string(ord(i)) + ').'
        return encoded_str[:-1]

    def base64_decode(self):
        """
        对 Base64 编码后的字符串进行解码
        :return: 解码后的字符串
        """
        decoded_str = base64.b64decode(self.string.encode('utf-8'))
        return decoded_str.decode('utf-8')

    def url_decode(self):
        """
        对 URL 编码后的字符串进行解码
        :return: 解码后的字符串
        """
        decoded_str = urllib.parse.unquote(self.string.encode('utf-8'))
        return decoded_str

    def chr_decode(self):
        """
        对 Chr 编码后的字符串进行解码
        :return: 解码后的字符串
        """
        decoded_str = ''
        for i in self.string.split('.'):
            if i:
                decoded_str += chr(int(i[4:-1]))
        return decoded_str

    # php code 规范化
    def php_code_format(self):
        pass

    def main(self):
        encoder_file = '..\\data\\encoder.txt'
        decoder_file = '..\\data\\decoder.txt'
        
        encode_lines = self.read_file(encoder_file)[0]
        self.string = encode_lines
        decode_str = self.encode_decode_str(self.chr_decode, False)
        logger.info(decode_str)
        self.php_code_format(decode_str)

        # decode_lines = self.read_file(decoder_file)[0]
        # self.string = decode_lines
        # encode_str = self.encode_decode_str(self.chr_encode)
        # logger.info(encode_str)

if __name__ == '__main__':
    fire.Fire(StrEncodeDecode)

