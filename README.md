# Backend REST API Repo for Fleapto Project 
### 블록체인 기반 중고거래 REST API

![Fleapto 서버구성도](https://user-images.githubusercontent.com/60056004/136686405-ca49d02e-cdfa-4642-91b3-42d959e91954.png)

## Stack
- API : Python FastAPI
- DB : MongoDB
- API SERVER : AWS Lambda 서비스를 이용한 Serverless로 서버 운용

## Start in Localhost
```
> pip install -r requirements.txt
> uvicorn main:app --reload
```

## Start in AWS Lambda with serverless node package
```
> npm install -g serverless
> npm install
> pip install -r requirements.txt
> serverless deploy
```
