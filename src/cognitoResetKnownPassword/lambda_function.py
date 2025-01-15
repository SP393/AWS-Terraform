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
    access_token = event['requestContext']['authorizer']['access_token']
    
    request_body = None
    try:
        request_body = json.loads(event['body'])
    except:
        return generate_response({ 'message': 'Request body incorrectly formatted'}, 400)
    
    # Extract request parameters from body
    old_password = None
    new_password = None
    try:
        old_password = request_body['oldPassword']
        new_password = request_body['newPassword']
    except KeyError:
        return generate_response({ 'message': 'Request body missing parameters' }, 400)
    
    # Call ChangePassword command
    response = None
    try:
        response = cognito_client.change_password(
            PreviousPassword=old_password,
            ProposedPassword=new_password,
            AccessToken=access_token
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