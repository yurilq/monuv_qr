import boto3

client = boto3.client('cloudwatch')

# Criação de um alarme para monitorar erros na Lambda
response = client.put_metric_alarm(
    AlarmName='MonuvQRLambdaErrors',
    ComparisonOperator='GreaterThanThreshold',
    EvaluationPeriods=1,
    MetricName='Errors',
    Namespace='AWS/Lambda',
    Period=60,
    Statistic='Sum',
    Threshold=1.0,
    ActionsEnabled=True,
    AlarmActions=[
        'arn:aws:sns:us-east-1:123456789012:monuv-sns-topic'
    ],
    Dimensions=[
        {
            'Name': 'FunctionName',
            'Value': 'MonuvQRLambdaFunction'
        },
    ],
    Unit='Count'
)
