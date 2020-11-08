# 顔認識

# Pythonコンソール

## 環境構築

```
cp src/aws.json.sample src/aws.json
```

aws.jsonにAWSのアクセスキー・アクセスシークレットを記入

```
docker build -t rekognition .
```

## 起動

Dockerコンテナで起動しているPython Shellにログイン

```
docker run -it -w /app -v $(pwd):/app rekognition bash
```

Pythonプログラムを実行

```
python src/rekognition.py images/sample.jpg
```

# Webサーバ

```
docker build -t rekognition-web -f Dockerfile-web .
docker run -d -p 8080:8080 -v $(pwd)/web:/app rekognition-web
```

# Webページ

`front/index.html` をブラウザで開く

```
open front/index.html
```
