# 顔認識

## Docker

```
docker build -t rekognition .
docker run -e AWS_DEFAULT_REGION=ap-northeast-1 -e AWS_ACCESS_KEY_ID=xxx -e AWS_SECRET_ACCESS_KEY=xxx -v src:/src -v images:/images rekognition images/sample.jpg
```
