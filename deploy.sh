#!/bin/bash
rm -r packages
rm packages.zip
pip install -r requirements.txt --target ./packages
if [ -d packages ]; then
	cd packages
    mkdir apis
    mkdir data
	cp ../*.py .
	cp ../apis/* apis
	cp ../data/* data
	cp ../production.ini .
	find . -name "tests.py" -delete
	find . -name "app.py" -delete
	find . -name "*.pyc" -delete
	find . -name "*.egg-info" | xargs rm -rf
	find . -name "*.dist-info" | xargs rm -rf
	zip -9mrv packages.zip .
	mv packages.zip ..
	cd ..
	rm -rf packages
fi

<<COMMENT
aws lambda create-function \
    --region us-east-1 \
    --function-name otnskills \
    --zip-file fileb://packages.zip \
    --role "arn:aws:iam::065056466896:role/APIGatewayLambdaExecRole" \
    --environment Variables={STAGE=production} \
    --handler lambda_function.lambda_handler \
    --runtime python2.7 \
    --profile default
COMMENT

aws lambda update-function-code  --function-name otnskills  --zip-file fileb://packages.zip

rm -rf ./packages.zip

