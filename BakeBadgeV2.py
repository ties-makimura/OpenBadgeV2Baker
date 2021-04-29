#!/usr/bin/python3
# -*- encoding: UTF-8 -*-
# vim: fileencode=utf-8

"""
本モジュールは、OpenBadgeV2プロジェクトのために、書いたモジュールです。
下記の機能を持っている。
- ロギング
- CSV読み取り
- 読み取ったデータの Validate 機能
    - 入っているべき固定値のチェック
    - URLのチェック
    - emailのチェック
    - CSVの関係チェック
    - saltのチェック
    - 
- Validate を通過した csvをjsonに変換する
"""
import sys
import os
from logging import Logger
import logging.handlers
import typing

# for email
import re

#
# csv file related
#
from pathlib import Path
import csv
import pprint


def setup_logger(name, logfile = 'OpenBadgeBake.log') -> Logger:
    """
    エラーをログファイルと、標準出力に出す。
    ログファイルには、ERRORレベルのメッセージを出力する。
        ログファイルはローテートする。
    標準エラー出力には、INFOレベルのメッセージを出力する。
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # create file handler which logs even DEBUG messages
    # fh = logging.FileHandler(logfile)
    # fh.setLevel(logging.DEBUG)
    # fh_formatter =
    # logging.Formatter(
    #   '%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s'
    # )
    # fh.setFormatter(fh_formatter)
    #fh = logging.FileHandler(logfile)
    fh = logging.handlers.RotatingFileHandler(logfile, maxBytes=100000, backupCount=3)
    fh.setLevel(logging.ERROR)
    fh_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(name)s - %(funcName)s - %(message)s')
    fh.setFormatter(fh_formatter)

    # create console handler with a INFO log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    ch.setFormatter(ch_formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return typing.cast(Logger,logger)


logger = setup_logger(__name__)


def func() -> bool:
    """
    unittest用のテストケース
    """
    return True

def CheckEmailFormat(email: str) -> bool:
    """
    Emailアドレスのフォーマットをチェックする。
    ask him
    """
    regex = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if(re.search(regex, email)):
        # print("Valid Email")
        return True
    else:
        # print("Invalid Email")
        return False

def CheckSHA256Format(sha256: str) -> bool:
    """
    SHA256のフォーマットをチェックする
    """
    # 先頭にsha256$が、あっても、なくてもa-fと0-9までのhexを組み合わせた64文字である
    regex = r'^((sha256|SHA256)\$|)[a-fA-F0-9]{64}(:.+)?$'
    if (re.search(regex, sha256)):
        return True
    else:
        return False

def CheckContext(context:str) -> bool:
    """
    contextのチェックをする。
    """
    regex = r'^https://w3id.org/openbadges/v2$'
    if (re.search(regex, context)):
        return True
    else:
        return False

def CheckHTTPUrl(url:str) -> bool:
    """
    URLのチェックをする
    """
    regex = r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'
    if (re.search(regex, url)):
        return True
    else:
        return False

def CheckCSVFileNames(p: Path) -> bool:
    """
    指定するpathオブジェクトのglob('/*.csv')
    """
    filelist = ['tests/Assertions.csv', 'tests/BadgeClass.csv', 'tests/Issuer.csv']
    l = list(p.glob('./*csv'))

    pprint.pprint(p)
    pprint.pprint(l)

    if (filelist == sorted(l)):
        return True
    else:
        return False


#def ReadAssertionsCsv(dir: str) -> 
