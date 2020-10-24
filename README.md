# 顔認識

## Docker

### 環境構築

```
cp src/aws.json.sample src/aws.json
```

aws.jsonにAWSのアクセスキー・アクセスシークレットを記入

### 起動

```
docker build -t rekognition .
docker run rekognition images/sample.jpg
```

ソースコードの更新・画像の更新ごとにbuildから実行する必要あり
