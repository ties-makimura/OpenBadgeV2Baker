# README

## この Repository の構成

```
+ data
+ tests テスト用データ
	- unittest は、python3標準のunittestを利用している。
	- unittest利用時は、.profileにexport PYTHONPATH=/home/yabuki/src/OpenBadgeV2 などと書いて置くこと
+ Makefile makeコマンドで実行、unittest, clean などが実行できる。使い方は src/OpenBadgeV2 で make とだけ打って helpを出せ
+ BakeBadgeV2.py モジュール。Docstringつけているから見よ。
```

## 追加モジュール

GitHub Actions (以下GHA) で動かすために、ubuntu 20.04 準拠とした。

これらの設定は、手元のpython3.8環境で動かすときに必要です。
GHAで動かす時には、設定済みなので不要です。

```
apt install python3-rfc3986 python3-iso8601
apt install python3-pip
pip3 openbadges_bakery
```

## 使い方

### 手元の環境

下記の4つのファイルを data/ へ置いて、make run を実行する。
csvにはheaderありが望ましい。dialect を推定しているので、windowsのExcelでもいけると思う。

- Assertions.csv
- BadgeClass.csv
- Issuer.csv
- pngまたは、svgのファイル

そうすると、 output/ に下記のファイルが生成される。

1/Assertion.json
  BakedBadge.png または、BakedBadge.svg
BadgeClass.json
Issuer.json

1の部分は、人数分の数字になります。

### GHA(GitHub Actions)

現在のworkflowを参照のこと。

## 開発していた環境

type-hinting は、ubuntu 20.04 環境のデフォルトである python3.8に合わせてある。python 3.9 だと type-hinting の書き方が変わる。mypy + VSCode の Jedi-LSP を使っていた。

## CSV 作成時の TIPs

自動的にファイルを生成するので、uplaod 作業を楽にする命名方法がある。

### Assertions.csv

- id の部分の 下位は、数字/Assertion.json 具体例 2/Assertion.json にする
ディレクトリを作成してファイル名を変更する手間を考えると合わせるのが得です。

- badge の部分も上記と同様です。
数字のディレクトリ配下にAssertion.json と BakedBadge.png または、BakedBadge.svg という名前でBadgeができあがります。

### BadgeClass.csv

- 発見したら追記します。

### Issuer.csv

- 発見したら追記します。

## ライセンス

Apache 2.0 ライセンスです。内容は、LICENSE ファイルを参照してください。

## Authors

著作権が発生するほどのコントリビュートを本プロジェクトに頂いた場合に、お名前と連絡先(Email address)をAuthors.md に記載していきます。

## Thanks

このリポジトリーにあるソフトウェアおよび、GitHub Actions を使った一連のシステムは、LICENCEファイルで定義されたライセンスで公開されます。
この公開に際して、特別な貢献をいただいている方々にたいしての謝辞を Thanks.md に記載いたします。
