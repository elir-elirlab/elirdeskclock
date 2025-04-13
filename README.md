# デスククロックプロジェクト

このリポジトリは、Raspberry Piを使用してデスククロックを作成するプロジェクトです。

詳しくはこちらのブログ記事（[えりる研究室: 【Raspberry Pi】 ラズパイで卓上時計を作る！AIを使って簡単制作【自由研究／DIY】](https://elirlab.com/diy-raspberry-pi-deskclock/)）をご覧ください

## 特徴

- 日付と現在時刻の表示

## 必要なもの

- Raspberry Pi（モデルは問いません）
- モニターまたはディスプレイ
- Python 3.13.2
- 必要なライブラリ（後述）

## セットアップ

1. このリポジトリをクローンします:
    ```bash
    git clone https://github.com/elir-elirlab/elirdeskclock.git
    cd elirdeskclock
    ```

2. 必要なPythonライブラリをインストールします:
    ```bash
    pip install -r requirements.txt
    ```

3. スクリプトを実行します:
    ```bash
    python main.py
    ```

## 使用方法

- プロジェクトを起動すると、日付と時刻が表示されます。
- main.pyと同じディレクトリにimage.pngを入れると起動時にそれが背景画像になります。
- image.pngが無ければ黒塗り背景になります。
- 起動後右クリックで背景画像を選択できます。


## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルをご覧ください。
