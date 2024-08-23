#!/bin/bash

# Fazer o upload do código Lambda para o S3
aws s3 cp lambda_functions/monuv_qr_lambda.py s3://monuv-code-bucket/monuv-qr-lambda.zip

# Criar ou atualizar a função Lambda via CloudFormation
aws cloudformation deploy \
    --template-file cloudformation/monuv_template.yaml \
    --stack-name monuv-qr-code-tracking-solution \
    --capabilities CAPABILITY_IAM
