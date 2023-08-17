from email.header import decode_header
from email.utils import parseaddr


def decode_str(s):
    """解析二进制字符串"""
    value, charset = decode_header(s)[0]
    if charset:
         value = value.decode(charset)
    return value

def parse_mailaddr(rawaddr:str):
    raw_name,addr = parseaddr(rawaddr)
    name = decode_str(raw_name)
    return name,addr