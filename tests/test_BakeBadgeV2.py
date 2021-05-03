# import os, sys

import unittest
import unittest.mock

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pathlib import Path

# ~/.profile に 設定を書いているのでヨシとする。
import BakeBadgeV2
#
import pprint


class TestValidation(unittest.TestCase):
    """
    バリデーションをテストするクラス
    """
    def test_1(self):
        """
        UnitTestの試行
        """
        self.assertEqual(BakeBadgeV2.func(), True)

    def test_email(self):
        """
        emailのテストパターン
        """
        test_patterns = [
            ("hoge@gmail.com", True),
            (".hoge@examples.com", True),
            ("..hoge@examples.com", True),
            ("hoge", False),
            ("hoge@local", False)
            ]

        for email, result in test_patterns:
            # subTest()の引数には失敗時に出力したい内容を指定。
            with self.subTest(email=email, result=result):
                self.assertEqual(BakeBadgeV2.CheckEmailFormat(email), result)

    def test_sha256(self):
        """
        sha256のテストパターン
        """
        test_patterns = [
            ("sha256$9b2b7d2c5c82ec6862e7d57d150b9b57165571fe1abe12c773828368f772efa3", True),
            ("SHA256$9b2b7d2c5c82ec6862e7d57d150b9b57165571fe1abe12c773828368f772efa3", True),
            ("9b2b7d2c5c82ec6862e7d57d150b9b57165571fe1abe12c773828368f772efa3", True),
            ("sha256$9b2b7d2c5c82ec6862e7d57d150b9b57165571fe1abe12c773828368f772efa", False),
            ("9b2b7d2c5c82ec6862e7d57d150b9b57165571fe1abe12c773828368f772efa", False)

        ]
        for sha256hash, result in test_patterns:
            with self.subTest(sha256hash=sha256hash, result=result):
                self.assertEqual(BakeBadgeV2.CheckSHA256Format(sha256hash), result)

    def test_context(self):
        """
        @contextのテストパターン
        """
        test_patterns = [
            ("https://w3id.org/openbadges/v2", True),
            ("http://w3id.org/openbadges/v2", False),
            ("https://w3id.org/openbadges/v1", False)
        ]
        for context, result in test_patterns:
            with self.subTest(context=context, result=result):
                self.assertEqual(BakeBadgeV2.CheckContext(context), result)

    def test_HTTP_url(self):
        """
        http(s)から始まるURLをテストするパターン
        """
        test_patterns = [
            ("https://w3id.org/openbadges/v2", True),
            ("ftp://ftp.example.com/", False),
            ("ftp://ftp.example.com/pub/", False),
            ("http://w3id.org/openbadges/v2", True),
            ("https://w3id.org/openbadges/v1", True)
        ]
        for url, result in test_patterns:
            with self.subTest(url=url, result=result):
                self.assertEqual(BakeBadgeV2.CheckHTTPUrl(url), result)

    def test_Issued_On(self):
        """
        issuedOnの発行日は、ISO8601の形式に従う
        """
        test_patterns = [
            ("20210503T210215", False),
            ("20210403210215", False),
            ("2021-05-03 21:02:15", False),
            ("2021-05-03T21:02:15Z", True),
            ("2021-05-03T21:02:15", True),
            ("2021-05-03T21:02:15+00:00", True),
            ("2021-05-03T21:02:15-01:00", True),
            ("2021-05-03T21:02:15-09:00", True),
            ("2021-32-03T21:02:15", False)
        ]
        for str_val, result in test_patterns:
            with self.subTest(str_val=str_val, result=result):
                self.assertEqual(BakeBadgeV2.CheckIssuedOn(str_val), result)

    def testExpires(self):
        """
        空白の場合を含めてテストする
        """
        test_patterns = [
            ("", True),
            ('', True),
            ("20210503T210215", False),
            ("20210403210215", False),
            ("2021-05-03 21:02:15", False),
            ("2021-05-03T21:02:15Z", True),
            ("2021-05-03T21:02:15", True),
            ("2021-05-03T21:02:15+00:00", True),
            ("2021-05-03T21:02:15-01:00", True),
            ("2021-05-03T21:02:15-09:00", True),
            ("2021-32-03T21:02:15", False)
        ]
        for str_val, result in test_patterns:
            with self.subTest(str_val=str_val, result=result):
                self.assertEqual(BakeBadgeV2.CheckExpires(str_val), result)


    def test_csv_file(self):
        """
        csvファイルに関するテストパターン
        """
        test_patterns = [
            (Path('tests'), True),
            (Path('.'), False)
        ]
        p = Path('tests')
        for p, result in test_patterns:
            with self.subTest(p=p, result = result):
                self.assertEqual(BakeBadgeV2.CheckCSVFileNames(p), result)

class TestMock(unittest.TestCase):
    """
    モックのテストを書く
    """
    def test_hoge(self):
        """
        テスト用モック
        """
        m = unittest.mock.MagicMock()

        # モックに戻り値を設定しテストを実行
        m.return_value = ('aaaa', 'bbbb')
        MockWillBeChange = m
        csv = MockWillBeChange()
        print("csv")
        pprint.pprint(csv)

        # 戻り値が正しいことのチェック(mockでわざと書き換えた値なので正しくはないのですが)
        self.assertEqual(csv, ('aaaa','bbbb'))


        # 例外送出を設定したい場合はside_effectに例外を指定する
        m.side_effect = OSError("dummy_error")

        # 例外の試験なのでassertRaisesで囲っておく
        with self.assertRaises(OSError) as cm:
            csv = MockWillBeChange('aaaa', 'bbbb')

        # 例外が想定通りであることを確認
        self.assertEqual(str(cm.exception), str(OSError("dummy_error")))
