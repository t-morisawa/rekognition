# 顔認識

# Webサーバ

## 環境構築

```
cp .env.example .env
```

.envにAWSとTwitterのアクセスキー・アクセスシークレットを記入

## 起動

```
$ docker-compose up --build
```

http://localhost:3000

# 参考文献

 - Element UI https://element.ele.me/#/en-US/component/installation

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

