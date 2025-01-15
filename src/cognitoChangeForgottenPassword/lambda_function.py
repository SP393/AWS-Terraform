import os
import json
import boto3
import botocore
import logging

logger = logging.getLogger()
logger.setLevel('INFO')

cognito_region = os.environ['COGNITO_REGION']
cognito_client_id = os.environ['COGNITO_CLIENT_ID']
cognito_client = boto3.client('cognito-idp', region_name=cognito_region)

def lambda_handler(event, context):
    request_body = None
    try:
        request_body = json.loads(event['body'])
    except:
        return generate_response({ 'message': 'Request body incorrectly formatted'}, 400)
    
    # Extract request parameters from body
    email = None
    verification_code = None
    new_password = None
    try:
        email = request_body['email']
        verification_code = request_body['verificationCode']
        new_password = request_body['newPassword']
    except KeyError:
        return generate_response({ 'message': 'Request body missing parameters' }, 400)
    
    # Call ConfirmForgotPassword command
    response = None
    try:
        response = cognito_client.confirm_forgot_password(
            ClientId=cognito_client_id,
            Username=email,
            ConfirmationCode=verification_code,
            Password=new_password
        )
    except botocore.exceptions.ClientError as error:
        response = error.response['Error']['Message']
        return generate_response({ 'message': error.response['Error']['Message']}, error.response['ResponseMetadata']['HTTPStatusCode'])
    
    return generate_response({ 'message': 'Password change successful'})
    
    
# Helper function to generate a simple HTTP response
def generate_response(response_body, status_code=200):
    return {
        'statusCode': status_code,
        'body': json.dumps(response_body)
    }