# 顔認識

## Docker

### 環境構築

```
docker build -t rekognition .
cp src/aws.json.sample src/aws.json
```

aws.jsonにAWSのアクセスキー・アクセスシークレットを記入

### 起動

```
docker run rekognition images/sample.jpg
```
