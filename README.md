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
docker run -e AWS_DEFAULT_REGION=ap-northeast-1 -e AWS_ACCESS_KEY_ID=xxx -e AWS_SECRET_ACCESS_KEY=xxx -v src:/src -v images:/images rekognition images/sample.jpg
```
