import os
import random
import tarfile
import hashlib
import string
import socket
import fcntl
import struct
from typing import List
from pathlib import Path

import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.header import Header


def randstr(str_type: str = None, length: int = 8) -> str:
    """
    Generate a random alphabet string or special characters or mixed characters.
    str_type: "alphabet" and "spec_char" are accepted. "str_type=None" indicate all alphabets and special characters.
    length: the length of random string.
    Return: the random string.
    """
    if str_type == "alphabet":
        char_group = string.ascii_letters
    elif str_type == "spec_char":
        char_group = string.punctuation
    else:
        char_group = string.ascii_letters + string.punctuation
    return ''.join(random.choices(char_group, k=length))


def send_email(
        smtp_svr: str, account: str, account_pwd: str=None, via_ssl:bool = False, smtp_svr_port: int = 25,
        from_: str=None, to: (str, list) = None, cc: (str, list) = None, bcc: (str, list) = None,
        subject: str = '', content: str = '', attachments: List[Path] = None, timeout: int = 5
) -> None:
    """发送邮件

    :param smtp_svr: SMTP服务器
    :param account: 发件人帐号
    :param account_pwd: 发件人帐号的密码
    :param via_ssl: 是否通过SSL
    :param smtp_svr_port: SMTP服务端口号，默认25
    :param from_: 代发帐号
    :param to: 收件人列表
    :param cc: 抄送人列表
    :param bcc: 密送人列表
    :param subject: 邮件主题
    :param content: 邮件内容
    :param attachments: 附件列表，列表为附件的路径
    :param timeout: smtp服务连接超时时间，默认：5s
    :return: None
    """
    to = to or []
    cc = cc or []
    bcc = bcc or []
    if isinstance(to, str):
        to = [to]
    if isinstance(cc, str):
        cc = [cc]
    if isinstance(bcc, str):
        bcc = [bcc]
    msg = MIMEMultipart()
    msg['From'] = from_ or account
    msg['To'] = ",".join(to)
    msg['Cc'] = ",".join(cc)
    msg['Bcc'] = ",".join(bcc)
    msg['Subject'] = Header(subject, 'utf-8').encode()

    msg.attach(MIMEText(content, 'plain', 'utf-8'))

    for fp in attachments or list():
        with open(fp, 'rb') as f:
            # 设置附件的MIME和文件名:
            if fp.name.endswith('zip'):
                mime = MIMEBase('application', 'x-zip-compressed', filename=fp.name)
                mime.add_header('Content-Disposition', 'attachment', filename=fp.name)
            elif fp.name.endswith('html'):
                mime = MIMEBase('text', 'html', filename=fp.name)
                mime.add_header('Content-Disposition', 'attachment', filename=fp.name)
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            msg.attach(mime)
    try:
        if via_ssl:
            smtp_obj = smtplib.SMTP_SSL(smtp_svr, smtp_svr_port, timeout=timeout)
        else:
            smtp_obj = smtplib.SMTP(smtp_svr, smtp_svr_port, timeout=timeout)
        if account_pwd:
            smtp_obj.login(account, account_pwd)
        smtp_obj.sendmail(account, to + cc + bcc, msg.as_string())
    except smtplib.SMTPException as e:
        raise Exception('Fail to send email!')


def tar_files(archive_fp: Path, files: List[Path]):
    with tarfile.open(archive_fp, mode='w:gz') as archive:
        for f in files:
            archive.add(f, recursive=True, arcname=f.name)


def md5(s: (str, bytes)) -> str:
    m = hashlib.md5()
    m.update(isinstance(s, bytes) and s or s.encode())
    return m.hexdigest()


def get_file_md5(fp: str):
    """
    获取文件md5值
    :param fp: 文件路径名
    :return: 文件md5值
    """
    with open(fp, 'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        _hash = md5obj.hexdigest()
    return str(_hash).upper()


def get_ip_address(ifname: (str, bytes)) -> str:
    """
    Get the IP address of current system
    note: this method tested on Linux ONLY
    :param ifname: interface name(you cae check all interfaces using 'ifconfig' command in console.)
    :return: the IP address of specified interface
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ifname = isinstance(ifname, bytes) and ifname or ifname.encode()
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])


def safe_get_dict(dictionary: dict, keys: str, separator: str = '.'):
    """
    适用于从嵌套比较多的字典中取数据，
    :param dictionary: 目标字典.
    :param keys: 目标数据所在的字典路径，是一个字符串，多个key可用指定符号分隔。
    :param separator: 分隔符，用于分隔多个key，默认值','
    :return: 指定字典路径的数据，如果路径不存在，返回 None
    """
    keys = keys.split(separator)
    for key in keys:
        try:
            dictionary = dictionary[key]
        except Exception:
            return None
    return dictionary


def get_file_list(target_dir, suffix=None):
    root, _, files = next(os.walk(target_dir))
    if suffix:
        files = [os.path.join(root, file) for file in files if os.path.splitext(file)[1] == f'.{suffix}']
    else:
        files = [os.path.join(root, file) for file in files]
    return files
