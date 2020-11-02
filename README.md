# 顔認識

## Docker

### 環境構築

```
cp src/aws.json.sample src/aws.json
```

aws.jsonにAWSのアクセスキー・アクセスシークレットを記入

```
docker build -t rekognition .
```

### 起動

Dockerコンテナで起動しているPython Shellにログイン

```
docker run -it -w /app -v $(pwd):/app rekognition bash
```

Pythonプログラムを実行

```
python src/rekognition.py images/sample.jpg
```