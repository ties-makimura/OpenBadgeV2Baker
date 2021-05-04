#!/usr/bin/python3
# -*- encoding: UTF-8 -*-
# vim: fileencode=utf-8

"""
本モジュールは、OpenBadgeV2プロジェクトのために、書いたモジュールです。
下記の機能を持っている。
- ロギング
- CSV読み取り
- 読み取ったデータの Validate 機能
    - チェック対象は、
    Open Badges v2.0 https://www.imsglobal.org/sites/default/files/Badges/OBv2p0Final/index.html
    を確認すること。
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

# for check etc, email , csv
import re

# check for ISO8601
import datetime
import iso8601

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

def CheckTypeAssertion(typ: str) -> bool:
    """
    typeが"Assertion"かを判定する。
    """
    regex = r'^Assertion$'
    if (re.search(regex, typ)):
        return True
    else:
        return False

def CheckTypeBadgeClass(typ: str) -> bool:
    """
    typeが、"BadgeClass"かを判定する。
    """
    regex = r'^BadgeClass$'
    if re.search(regex, typ):
        return True
    else:
        return False

def CheckTypeIssuer(typ: str) -> bool:
    """
    typeが、"Issuer"かを判定する
    """
    regex = r'^Issuer$'
    if re.search(regex, typ):
        return True
    else:
        return False


def CheckRecipientType(typ: str) -> bool:
    """
    recipient:typeがemailかを判定する。
    """
    regex = r'^email'
    if (re.search(regex, typ)):
        return True
    else:
        return False

def CheckRecipientHashed(param: str) -> bool:
    """
    Trueかどうかを判定する。
    """
    regex = r'^True'
    if (re.search(regex, param)):
        return True
    else:
        return False

def CheckRecipientSalt(salt: str) -> bool:
    """
    saltの形式をチェックする。定義ではtextとのみ規定している。
    32桁の英数とする。
    """
    # regex = r'^[a-fA-F0-9]{32}(:.+)?$'
    regex = r"^[A-Z0-9]{32}(:.+)?$"
    if (re.search(regex, salt)):
        return True
    else:
        return False

def CheckTypeHosted(typ: str) -> bool:
    """
    hosted type かどうかを判定する
    """
    regex = r'^hosted'
    if (re.search(regex, typ)):
        return True
    else:
        return False

def CheckHTTPUrl(url: str) -> bool:
    """
    URLのチェックをする
    """
    regex = r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'
    if (re.search(regex, url)):
        return True
    else:
        return False

def CheckIssuedOn(str_val: str) -> bool:
    """
    Badgeの発行日を設定する。ISO8601の形式に従う。
    ただし、
    YYYY-MM-DDTHH:MM:SSZ
    YYYY-MM-DDTHH:MM:SS+HH:MM
    YYYY-MM-DDTHH:MM:SS-HH:MM
    Open Badges v2.0 https://www.imsglobal.org/sites/default/files/Badges/OBv2p0Final/index.html#dateTime
    によると、timezone付きの形式を要求している。必須ではないけども。あと、UTCの時間にすることを勧めている
    そのため、ローカルタイムはタイムゾーン付きが望ましいといえる。
    """
    regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
    match_iso8601 = re.compile(regex).match
    try:            
        if match_iso8601( str_val ) is not None:
            return True
    except:
        pass
    return False

def CheckExpires(str_val: str) -> bool:
    """
    Expiresは必須項目ではない。
    なにも入っていない。または、ISO8601の形式が入っている。
    """
    if len(str_val) == 0:
        # 文字サイズ==0 つまり、なにも入っていないか?
        return True
    
    return CheckIssuedOn(str_val)

def CheckDateTimeOrder(issuedOn: str, expires: str) -> bool:
    """
    strで受けた文字列をdatetimeに変換して、
    issuedOn < expires を確認する。そうならTrue, 
    そうでないなら、False

    expires は、有効な日付が入っていること具体的には
    ””でないこと。そうでなかったら例外を上げる。
    """
    if len(expires) == 0:
        raise TypeError("expiresが\"\"です。")

    first = iso8601.parse_date(issuedOn)
    second = iso8601.parse_date(expires)
    if first < second :
        return True
    else:
        return False

"""
CheckAssertionsDataのテストケースを作ろう
"""

def CheckBadgeName(name: str) -> bool:
    """
    BadgeNameの検証を行う。
    文字列長?
    漢字ひらかな、かたかなのチェック?
    いまは、とくに何もしない。hookのみ
    """
    return True

def CheckBadgeDescription(desc: str) -> bool:
    """
    BadgeのDescriptionの検証を行う。
    いまは、特に何もしない。
    """
    return True

def CheckBadgeImage(url: str) -> bool:
    """
    url+最後の拡張子が、pngまたはsgvである。
    """
    regex = r'^.*\.(PNG|png|SVG|svg)$'
    if CheckHTTPUrl(url):
        # url checkは通った。
        if re.search(regex, url):
            return True
        else:
            return False
    else:
        return False

def CheckBadgeCriteria(url: str) -> bool:
    """
    criteria は、url
    """
    return CheckHTTPUrl(url)

def CheckBadgeIssuer(url: str) -> bool:
    """
    urlだが、最後は.jsonである。
    """
    regex = r'^.*\.(json|JSON)$'
    if CheckHTTPUrl(url):
        # url check は通った
        if re.search(regex, url):
            return True
        else:
            return False
    else:
        return False

def CheckIssuerName(name: str) -> bool:
    """
    IssuerNameの検証を行う。
    いまは特に何もしない。hookのみ
    """
    return True

def CheckCSVFileNames(pdir: Path) -> bool:
    """
    pdir ディレクトリ
    　指定するpathオブジェクトのglob('/*.csv')
    """
    filelist = ['tests/Assertions.csv', 'tests/BadgeClass.csv', 'tests/Issuer.csv']
    if (pdir.is_dir):
        # pdirはディレクトリだ。
        # dirにあるファイルを \w*\.csv で filter かけて、str にして、filelistと比較可能
        # にして l へ出力する。
        l = list([str(p) for p in pdir.iterdir() if re.search('\w*\.csv', str(p))])

        print("pdir:")
        pprint.pprint(pdir)
        print("l")
        pprint.pprint(l)

        # 3つのファイルがふくまれていればok
        if l.count(filelist[0]) == 1 and l.count(filelist[1]) == 1 and l.count(filelist[2]) == 1:
           return True
        else:
            return False
    else:
        raise ValueError('pdirはディレクトリではありません。')

def CheckAssersionsData(row: typing.List[str], line: int) -> bool:
    """
    Assertions.csvの一行分のデータのチェックを行う。
    エラーなら、ロギングを行う。
    """
    #                                    0     1     2     3     4     5     6     7     8     9     10
    bErrorHappend: typing.List[bool] = [ True, True, True, True, True, True, True, True, True, True, True ] # 初期値はエラーが発生しているとする
    #
    # @context
    #
    if CheckContext(row[0]):
        formatted = f'{line}行目の@contextは合っています。'
        logger.info(formatted)
        bErrorHappend[0] = False
        pass
    else:
        formatted = f'{line}行目の@contextが間違っています。'
        logger.error(formatted)
        bErrorHappend[0] = True
    #
    # id
    #
    if CheckHTTPUrl(row[1]):
        formatted = f'{line}行目のidはURLです。'
        logger.info(formatted)
        bErrorHappend[1] = False
    else:
        formatted = f'{line}行目のidはURLではありません。'
        logger.error(formatted)
        bErrorHappend[1] = True
    #
    # type
    #
    if CheckTypeAssertion(row[2]):
        formatted = f'{line}行目のtypeがAssertionです。'
        logger.info(formatted)
        bErrorHappend[2] = False
    else:
        formatted = f'{line}行目のtypeがAssertionではありません。'
        logger.error(formatted)
        bErrorHappend[2] = True
    #
    #  recipient:type
    #
    if CheckRecipientType(row[3]):
        formatted = f'{line}行目のrecipient:typeはemailです。'
        logger.info(formatted)
        bErrorHappend[3] = False
    else:
        formatted = f'{line}行目のrecipient:typeはemailではありません。'
        logger.error(formatted)
        bErrorHappend[3] = True
    #
    # recipient:hashed
    #
    if CheckRecipientHashed(row[4]):
        formatted = f'{line}行目のrecipient:hashedはTrueです。'
        logger.info(formatted)
        bErrorHappend[4] = False
    else:
        formatted = f'{line}行目のrecipient:hashedはTrueではありません。'
        logger.error(formatted)
        bErrorHappend[4] = True
    #
    # recipient:salt
    #
    if CheckRecipientSalt(row[5]):
        formatted = f'"{row[5]}" - {line}行目のrecipient:saltは32桁の英数字です。'
        logger.info(formatted)
        bErrorHappend[5] = False
    else:
        formatted = f'"{row[5]}" - {line}行目のrecipient:saltは32桁の英数字ではありません。'
        logger.error(formatted)
        bErrorHappend[5] = True
    #
    # recipient:identity
    #
    if CheckSHA256Format(row[6]):
        formatted = f'"{row[6]}" - {line}行目のidentityは、SHA256形式です。'
        logger.info(formatted)
        bErrorHappend[6] = False
    else:
        formatted = f'"{row[6]}" - {line}行目のrecipient:identityは、SHA256形式ではありません'
        logger.error(formatted)
        bErrorHappend[6] = True
    #
    # Badge
    #
    if CheckHTTPUrl(row[7]):
        formatted = f'"{row[7]}" - {line}行目のbadgeは、URLです。'
        logger.info(formatted)
        bErrorHappend[7] = False
    else:
        formatted = f'"{row[7]}" - {line}行目のbadgeは、URLではありません。'
        logger.error(formatted)
        bErrorHappend[7] = True
    #
    # verification:type
    #
    if CheckTypeHosted(row[8]):
        formatted = f'"{row[8]}" - {line}行目のverification:typeは、hostedです。'
        logger.info(formatted)
        bErrorHappend[8] = False
    else:
        formatted = f'"{row[8]}" - {line}行目のverification:typeは、hostedではありません。'
        logger.error(formatted)
        bErrorHappend[8] = True
    #
    # issuedOn
    #
    if CheckIssuedOn(row[9]):
        formatted = f'"{row[9]}" - {line}行目のissuedOnは、iso8601形式です。'
        logger.info(formatted)
        bErrorHappend[9] = False
    else:
        formatted = f'"{row[9]}" - {line}行目のissuedOnは、YYYY-MM-DDTHH:MM:SS+00:00のiso8601形式ではありません。'
        logger.error(formatted)
        bErrorHappend[9] = True
    #
    # Expires
    #
    # Expires は、必須項目ではない。ので、空白なら作らない。
    if CheckExpires(row[10]):
        formatted = f'"{row[10]}" - {line}行目のExpiresは、""またはiso8601形式です。'
        logger.info(formatted)
        bErrorHappend[10] = False
    else:
        formatted = f'"{row[10]}" - {line}行目のExpiresは、""またはiso8601形式ではありません。'
        logger.error(formatted)
        bErrorHappend[10] = True
    #
    #
    #
    # Expiresが""以外なら、issuedOnより後か?
    if bErrorHappend[9] == False and bErrorHappend[10] == False:
        # issuedOn と Expires は、意味のあるiso8601 形式かも
        if len(row[10]) == 0:
            # "" だった。
            pass
        else:
            # なにか意味のある日付だ。
            if CheckDateTimeOrder(row[9], row[10]):
                pass
            else:
                formatted =f'"{row[9]} - {row[10]} - {line}行目の日付の関係が逆です。'
                logger.error(formatted)
                return False
    #
    #
    #
    if any(bErrorHappend):
        # どれかがエラー起きた。
        return False
    else:
        # エラーが起きなかった。
        return True

def CheckBadgeClassData(row:typing.List[str], line:int) -> bool:
    """
    BadgeClass.csvの一行分のデータチェックを行う。
    エラーならロギングを行う。
    """
    #                                   0     1     2     3     4     5     6     7
    bErrorHappend: typing.List[bool] = [True, True, True, True, True, True, True, True]

    # 0. @context
    # 1. id
    # 2. type
    # 3. name
    # 4. description
    # 5. image
    # 6. criteria
    # 7. issuer

    #
    # @context
    #
    if CheckContext(row[0]):
        formatted = f'{line}行目の@contextは合っています。'
        logger.info(formatted)
        bErrorHappend[0] = False
        pass
    else:
        formatted = f'{line}行目の@contextが間違っています。'
        logger.error(formatted)
        bErrorHappend[0] = True
    #
    # id
    #
    if CheckHTTPUrl(row[1]):
        formatted = f'{line}行目のidはURLです。'
        logger.info(formatted)
        bErrorHappend[1] = False
    else:
        formatted = f'{line}行目のidはURLではありません。'
        logger.error(formatted)
        bErrorHappend[1] = True
    #
    # type
    #
    if CheckTypeBadgeClass(row[2]):
        formatted = f'{line}行目のtypeがBadgeClassです。'
        logger.info(formatted)
        bErrorHappend[2] = False
    else:
        formatted = f'{line}行目のtypeがBadgeClassではありません。'
        logger.error(formatted)
        bErrorHappend[2] = True
    #
    # name
    #
    if CheckBadgeName(row[3]):
        formatted = f'"{row[3]}" - {line}行目のname'
        logger.info(formatted)
        bErrorHappend[3] = False
    else:
        formatted = f'"{row[3]}" - {line}行目のnameは不正です。'
        logger.error(formatted)
        bErrorHappend[3] = True
    #
    # description
    #
    if CheckBadgeDescription(row[4]):
        formatted = f'"{row[4]}" - {line}行目のdescription'
        logger.info(formatted)
        bErrorHappend[4] = False
    else:
        formatted = f'"{row[4]}" - {line}行目のdescriptionが不正です。'
        logger.error(formatted)
        bErrorHappend[4] = True
    #
    # image
    #
    if CheckBadgeImage(row[5]):
        formatted = f'"{row[5]}" - {line}行目のBadgeImageはpngまたはsvgです。'
        logger.info(formatted)
        bErrorHappend[5] = False
    else:
        formatted = f'"{row[5]}" - {line}行目のBadgeImageはpngまたはsvgではありません。'
        logger.error(formatted)
        bErrorHappend[5] = True
    #
    # criteria
    #
    # 本来 criteria は違う構造も許すが今回の仕様だとURLを記するのでこれでよい
    if CheckBadgeCriteria(row[6]):
        formatted = f'"{row[6]}" - {line}行目は正しい形式です。'
        logger.info(formatted)
        bErrorHappend[6] = False
    else:
        formatted = f'"{row[6]}" - {line}行目は正しい形式ではありません。'
        logger.error(formatted)
        bErrorHappend[6] = True
    #
    # issuer
    #
    if CheckBadgeIssuer(row[7]):
        formatted = f'"{row[7]}" - {line}行目は正しい形式です。'
        logger.info(formatted)
        bErrorHappend[7] = False
    else:
        formatted = f'"{row[7]}" - {line}行目は正しい形式ではありません。'
        logger.error(formatted)
        bErrorHappend[7] = True
    #
    #
    #
    if any(bErrorHappend):
        # どれかでエラーが起きた。
        return False
    else:
        # エラーは起きなかった。
        return True

def CheckIssuerData(row:typing.List[str], line:int) -> bool:
    """
    Issuer.csvの一行分のデータチェックを行う。
    エラーなら、ロギングを行う。
    """
    #                                   0     1     2     3     4     5
    bErrorHappend: typing.List[bool] = [True, True, True, True, True, True]

    # 0. @context
    # 1. id
    # 2. type
    # 3. name
    # 4. url
    # 5. email

    #
    # @context
    #
    if CheckContext(row[0]):
        formatted = f'"{row[0]}" - {line}行目は正しい形式です。'
        logger.info(formatted)
        bErrorHappend[0] = False
    else:
        formatted = f'"{row[0]}" - {line}行目は正しい形式ではありません。'
        logger.error(formatted)
        bErrorHappend[0] = True
    #
    # id
    #
    if CheckHTTPUrl(row[1]):
        formatted = f'"{row[1]}" - {line}行目は正しい形式です。'
        logger.info(formatted)
        bErrorHappend[1] = False
    else:
        formatted = f'"{row[1]}" - {line}行目は正しい形式ではありません。'
        logger.error(formatted)
        bErrorHappend[1] = True
    #
    # type = Issuer
    #
    if CheckTypeIssuer(row[2]):
        formatted = f'"{row[2]}" - {line}行目は正しい形式です。'
        logger.info(formatted)
        bErrorHappend[2] = False
    else:
        formatted = f'"{row[2]}" - {line}行目は正しい形式ではありません。'
        logger.error(formatted)
        bErrorHappend[2] = True
    #
    # Issuer name
    #
    if CheckIssuerName(row[3]):
        formatted = f'"{row[3]}" - {line}行目は正しい形式です。'
        logger.info(formatted)
        bErrorHappend[3] = False
    else:
        formatted = f'"{row[3]}" - {line}行目は正しい形式ではありません。'
        logger.error(formatted)
        bErrorHappend[3] = True
    #
    # name(url)
    #
    if CheckHTTPUrl(row[4]):
        formatted = f'"{row[4]}" - {line}行目は正しい形式です。'
        logger.info(formatted)
        bErrorHappend[4] = False
    else:
        formatted = f'"{row[4]}" - {line}行目は正しい形式ではありません。'
        logger.error(formatted)
        bErrorHappend[4] = True
    #
    # email
    #
    if CheckEmailFormat(row[5]):
        formatted = f'"{row[5]}" - {line}行目は正しい形式です。'
        logger.info(formatted)
        bErrorHappend[5] = False
    else:
        formatted = f'"{row[5]}" - {line}行目は正しい形式ではありません。'
        logger.error(formatted)
        bErrorHappend[5] = True
    #
    #
    #
    if any(bErrorHappend):
        # どれかがエラー起きた。
        return False
    else:
        # エラーが起きなかった。
        return True


def MockWillBeChange() -> typing.Tuple[str, str] :
    """
    モック用の確認コード
    """
    return ("aaa", "bbb")


def ReadAssertionsCsv(dir: Path) -> bool:
    """
    Assertions.csvを読み取りつつ検査する。検査結果はログと標準出力に書き出す。
    下記の項目について検査を行う。
    """
    # 全部のデータがValidだったら、Trueになるフラグ
    # 初期値は、判定の都合上 Trueとする。一回でも False
    # になったら、Falseのまま
    okData: bool = True

    rpf: Path = dir / "Assertions.csv" # 相対パス付きのファイル名
    logger.info(rpf.__repr__)
    with open(rpf, newline='') as csvfile:
        # 先読みしてどの、dialectかを判定する
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        # logger.info(dialect.__repr__)
        csvfile.seek(0)
        # headerあり?
        # hasHeader = True : あり
        # hasHeader = False: なし
        hasHeader = csv.Sniffer().has_header(csvfile.read(1024))
        if hasHeader:  # header行があるかどうか True/False
            logger.info("%s has a header" % rpf)
        else:
            logger.error("Assertions.csvに、Headerがついていません。")
        csvfile.seek(0)  # 先頭に戻る
        
        reader = csv.reader(csvfile, dialect)
        line: int = 0
        for row in reader:
            if line == 0 and hasHeader:
                # 0 行めで、ヘッダーありなら、スキップする。
                line = line + 1
                continue
            rtn = CheckAssersionsData(row, line)
            # rtn が一回でもFalseになったら、okDataはFalseになる
            # okDataがFalseならupdateしない。ラッチ機構
            if okData == True:
                if rtn == False:
                    okData = False
            line = line + 1
    return okData

def ReadBadgeClassCsv(dir: Path) -> bool:
    """
    BadgeClass.csvを読み取りつつ検査する。検査結果はログと標準出力に書き出す。
    """
    # 全部のデータがValidだったら、Trueになるフラグ
    # 初期値は、判定の都合上 Trueとする。一回でも False
    # になったら、Falseのまま
    okData: bool = True

    rpf: Path = dir / "BadgeClass.csv" # 相対パス付きのファイル名
    logger.info(rpf.__repr__)
    with open(rpf, newline='') as csvfile:
        # 先読みしてどの、dialectかを判定する
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        # pprint.pprint(dialect)
        # logger.info(dialect.__repr__)
        csvfile.seek(0)
        # headerあり?
        # hasHeader = True : あり
        # hasHeader = False: なし
        hasHeader = csv.Sniffer().has_header(csvfile.read(1024))
        if hasHeader:  # header行があるかどうか True/False
            logger.info("%s has a header" % rpf)
        else:
            logger.error("BadgeClass.csvに、Headerがついていません。")
        csvfile.seek(0)  # 先頭に戻る
        
        reader = csv.reader(csvfile, dialect)
        line: int = 0
        for row in reader:
            if line == 0 and hasHeader:
                # 0 行めで、ヘッダーありなら、スキップする。
                line = line + 1
                continue
            rtn = CheckBadgeClassData(row, line)
            # rtn が一回でもFalseになったら、okDataはFalseになる
            # okDataがFalseならupdateしない。ラッチ機構
            if okData == True:
                if rtn == False:
                    okData = False
            line = line + 1

    return okData

def ReadIssuerCsv(dir: Path) -> bool:
    """
    Issuer.csvを読み取りつつ検査する。検査結果はログと標準出力に書き出す。
    """
    # 全部のデータがValidだったら、Trueになるフラグ
    okData: bool = True

    rpf: Path = dir / "Issuer.csv" # 相対パス付きのファイル名
    logger.info(rpf.__repr__)
    with open(rpf, newline='') as csvfile:
        # 先読みしてどの、dialectかを判定する
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        # pprint.pprint(dialect)
        # logger.info(dialect.__repr__)
        csvfile.seek(0)
        # headerあり?
        # hasHeader = True : あり
        # hasHeader = False: なし
        hasHeader = csv.Sniffer().has_header(csvfile.read(1024))
        if hasHeader:  # header行があるかどうか True/False
            logger.info("%s has a header" % rpf)
        else:
            logger.error("Issuer.csvに、Headerがついていません。")
        csvfile.seek(0)  # 先頭に戻る
        
        reader = csv.reader(csvfile, dialect)
        line: int = 0
        for row in reader:
            if line == 0 and hasHeader:
                # 0 行めで、ヘッダーありなら、スキップする。
                line = line + 1
                continue
            rtn = CheckIssuerData(row, line)
            # rtn が一回でもFalseになったら、okDataはFalseになる
            # okDataがFalseならupdateしない。ラッチ機構
            if okData == True:
                if rtn == False:
                    okData = False
            line = line + 1
    return okData

def ControlCenter() -> None:
    """
    読み取り後のメイン処理
    """
    # 下記の3つの戻り値がTrueなら、先へ進む。でなかったら終了
    bAssertions: bool = False
    bBadgeClass: bool = False
    bIssuer: bool = False

    dir: Path = Path('tests')
    bAssertions = ReadAssertionsCsv(dir)
    bBadgeClass = ReadBadgeClassCsv(dir)
    bIssuer = ReadIssuerCsv(dir)


    if bAssertions and bBadgeClass and bIssuer :
        # 3つのファイルは全部、正しい内容だった。
        pass
    else:
        # 3つの入力ファイルのうち、どれか(全部も?)不正な値が
        # 入っている
        pass