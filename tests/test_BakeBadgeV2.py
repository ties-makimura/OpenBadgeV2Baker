# import os, sys

import unittest

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


# ~/.profile に 設定を書いているのでヨシとする。
import BakeBadgeV2

class testBakeBadgeV2(unittest.TestCase):
    def test_1(self):
        self.assertEqual(BakeBadgeV2.func(), True)

    def test_email(self):

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
