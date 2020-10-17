# 顔認識

## サンプル

### 環境構築

1. 仮想環境

```
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

2. aws profileの設定

 - `~/.aws/config` `./.aws/credentials` にアクセスキーやリージョンを設定する
 - https://docs.aws.amazon.com/ja_jp/cli/latest/userguide/cli-configure-profiles.html

### 実行

```
AWS_PROFILE=<profile> python rekognition.py sample.jpg
```

`profile`: aws profileの名前
