Create and Run
```sh
aws cloudformation create-stack --stack-name api-lambda --template-body file://resources.yaml --capabilities CAPABILITY_NAMED_IAM

zip -j app.zip app/index.py

aws lambda update-function-code --function-name app --zip-file fileb://app.zip
```

Clean Up
```sh
aws cloudformation delete-stack --stack-name api-lambda
```