import os
import json
import boto3
import botocore
import logging

logger = logging.getLogger()
logger.setLevel('INFO')

cognito_region = os.environ['COGNITO_REGION']
cognito_client = boto3.client('cognito-idp', region_name=cognito_region)

def lambda_handler(event, context):
    request_body = None
    try:
        request_body = json.loads(event['body'])
    except:
        return generate_response({ 'message': 'Request body incorrectly formatted'}, 400)
    
    # Extract request parameters from body
    session_id = None
    user_code = None
    try:
        session_id = request_body['sessionId']
        user_code = request_body['userCode']
    except KeyError:
        return generate_response({ 'message': 'Request body missing parameters' }, 400)
    
    # Call VerifySoftwareToken command
    response = None
    try:
        response = cognito_client.verify_software_token(
            Session = session_id,
            UserCode = user_code,
        )
    except botocore.exceptions.ClientError as error:
        response = error.response['Error']['Message']
        return generate_response({ 'message': error.response['Error']['Message']}, error.response['ResponseMetadata']['HTTPStatusCode'])
    
    return generate_response({ 'message': 'MFA setup successful'})
    
    
# Helper function to generate a simple HTTP response
def generate_response(response_body, status_code=200):
    return {
        'statusCode': status_code,
        'body': json.dumps(response_body)
    }