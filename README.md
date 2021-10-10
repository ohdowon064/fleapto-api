# Backend REST API Repo for Fleapto Project 
## 블록체인 기반 중고거래 플랫폼

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
