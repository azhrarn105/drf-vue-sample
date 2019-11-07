### 対象

- [現場で使える Django REST Framework の教科書](https://www.amazon.co.jp/%E7%8F%BE%E5%A0%B4%E3%81%A7%E4%BD%BF%E3%81%88%E3%82%8B-Django-REST-Framework-%E3%81%AE%E6%95%99%E7%A7%91%E6%9B%B8-ebook/dp/B07XWL8FPM)
  - 第 10 章 チュートリアル その 2： DRF + VueCLI3 で　JWT 認証付き SPA を本格構築
  - 第 8 章 ユニットテスト

### 目的

- 上記の書籍を元に、Django REST Framework（DRF） と Vue（VueCLI3）による開発環境を構築してみる

### 試行時の環境

- Windows 10 Home
- Python 3.7.4
- npm 6.12.0

### 実行手順

1. このリポジトリを Clone（or Fork）後、直下の階層で Python の任意の仮想環境を構築  
  （理論上 venv でも virtualenv でも pipenv でも問題ないが、 pipenv で試行したのでその手順を示す）
   1. 環境変数に以下を追加
      1. `PIPENV_VENV_IN_PROJECT`: True
   2. 以下コマンドを順に実行
      1. `> pip install pipenv` (pipenv 未インストールの場合のみ)
      2. `> pipenv --python 3.7` (これでPipfileから必要なライブラリはインストールされる)
      3. `> pipenv shell` (仮想環境に入る)
2. 以下コマンドで DB 周りを設定
   1. `> py manage.py makemigrations`
   2. `> py manage.py migrate`
   3. `> py manage.py createsuperuser` 対話式質問に答え、ユーザーを作成する
   4. ルートディレクトリで、Django の開発サーバーを起動する、 http://127.0.0.1:8000/  
      `> py manage.py runserver` 
3. 別ターミナルで`frontend` ディレクトリへ移動し、以下コマンドを実行
   1. `> npm install`
4. `frontend` ディレクトリのまま、以下コマンドを実行し、 http://localhost:8080/ に ログイン画面が表示されることを確認
   1. `> npm run serve`
5. 2-3 で作成したユーザーアカウントでログインすると、Bookデータの登録、更新ができる

### サンプルコード、手順を実行した際のポイント、変更点
- ユニットテストの test_serializers.py について
  - `from .serializers import BookSerializer` の箇所は `from apiv1.serializers import BookSerializer` としないと動かなかった
