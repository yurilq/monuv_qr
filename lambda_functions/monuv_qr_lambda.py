import json
import boto3
from datetime import datetime
import requests
from aws_lambda_powertools import Logger, Tracer

logger = Logger(service="monuv_qr_reader")
tracer = Tracer(service="monuv_qr_reader")

sqs_client = boto3.client('sqs')
queue_url = "https://sqs.us-east-1.amazonaws.com/123456789012/monuv-qr-processing-queue"

@tracer.capture_lambda_handler
@logger.inject_lambda_context
def lambda_handler(event, context):
    try:
        # Extração da imagem do corpo da requisição
        image_data = event['body']
        
        # Processamento fictício do QR Code a partir da imagem
        cam_code, client_code, qr_content, lat, long = read_qr_image(image_data)

        headers = {'Content-Type': 'application/json', 'Authorization': event['headers']['Authorization']}

        data = {
            "CamCode": cam_code,
            "Timestamp": datetime.now().isoformat(),
            "ClientCode": client_code,
            "QrContent": qr_content,
            "Lat": lat,
            "Long": long
        }

        # Envio dos dados ao servidor de controle de bilheteria
        response = requests.post(url=event['headers']['Post-Url'], json=data, headers=headers, timeout=5)
        print(f'POST Response: {response}')

        # Envio dos dados para a fila SQS
        sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=json.dumps(data)
        )
        
        logger.info(f'Successfully sent message to SQS: {response["MessageId"]}')
        return {
            'statusCode': 200,
            'body': json.dumps('QR Code processed successfully')
        }

    except Exception as e:
        logger.error(f"Error processing QR Code: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing QR Code')
        }
