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

# for email , csv
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

def CheckCSVFileNames(pdir: Path) -> bool:
    """
    pdir ディレクトリ
    　指定するpathオブジェクトのglob('/*.csv')
    """
    filelist = ['tests/Assertions.csv', 'tests/BadgeClass.csv', 'tests/Issuer.csv']
    if (pdir.is_dir):
        # pdirはディレクトリだ。
        #pprint.pprint([p for p in pdir.iterdir()])
        # pprint.pprint([p for p in pdir.iterdir() if re.search('\w+\.csv', str(p))])
        # dirにあるファイルを \w*\.csv で filter かけて、str にして、filelistと比較可能
        # にして l へ出力する。
        l = list([str(p) for p in pdir.iterdir() if re.search('\w*\.csv', str(p))])

        print("pdir:")
        pprint.pprint(pdir)
        print("l")
        pprint.pprint(l)

        if (filelist == sorted(l)):
            return True
        else:
            return False
    else:
        raise ValueError('pdirはディレクトリではありません。')

def MockWillBeChange() -> typing.Tuple[str, str] :
    return ("aaa", "bbb")


#def ReadAssertionsCsv(dir: str) -> 
