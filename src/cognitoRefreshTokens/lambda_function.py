import os
import json
import boto3
import botocore
from cryptography.fernet import Fernet
import logging

logger = logging.getLogger()
logger.setLevel('INFO')

client_id = os.environ['COGNITO_CLIENT_ID']
cognito_region = os.environ['COGNITO_REGION']

cognito_client = boto3.client('cognito-idp', region_name=cognito_region)

fernet = Fernet(os.environ['TOKEN_ENCRYPTION_KEY'].encode())

def lambda_handler(event, context):
    # Read refresh token from cookies
    request_cookies = event.get('multiValueHeaders', {}).get('cookie', None)
    if request_cookies is None:
        request_cookies = event.get('multiValueHeaders', {}).get('Cookie', None)
        
    if request_cookies is None:
        return generate_error_response({ 'message': 'No tokens in request'})
        
    request_cookies = request_cookies[0]
    refresh_token = extract_token('__Host-refreshToken=', request_cookies)
    
    if refresh_token is None:
        return generate_error_response({ 'message': 'No refresh token in request'})
    
    # Decrypt refresh token
    decrypted_refresh_token = None
    try:
        decrypted_refresh_token = fernet.decrypt(refresh_token.encode()).decode()
    except:
        return generate_error_response({ 'message': 'Error decrypting refresh token'})
        
    # Call InitiateAuth command
    response = None
    try:
        response = cognito_client.initiate_auth(
            AuthFlow='REFRESH_TOKEN_AUTH',
            AuthParameters={
                'REFRESH_TOKEN': decrypted_refresh_token,
            },
            ClientId=client_id
        )
    except botocore.exceptions.ClientError as error:
        error_code = error.response['Error']['Code']
        error_message = error.response['Error']['Message']
        status_code = error.response['ResponseMetadata']['HTTPStatusCode']
        return generate_error_response({ 'message': error_message, 'code': error_code }, status_code)
    
    access_token = None
    id_token = None
    session_expires_in = None
    try:
        access_token = response['AuthenticationResult']['AccessToken']
        id_token = response['AuthenticationResult']['IdToken']
        session_expires_in = response['AuthenticationResult']['ExpiresIn']
    except KeyError:
        return generate_error_response({ 'message': 'Error extracting auth response values' }, 500)
    
    return {
        'statusCode': 200,
        'multiValueHeaders': {
            'Set-Cookie': [
                f'__Host-accessToken={fernet.encrypt(access_token.encode()).decode()}; Secure; HttpOnly; SameSite=Strict; Path=/; Max-Age=604800',
                f'__Host-idToken={fernet.encrypt(id_token.encode()).decode()}; Secure; HttpOnly; SameSite=Strict; Path=/; Max-Age=604800'
            ]
        },
        'body': json.dumps({ 'message': 'Refresh successful' })
    }
    

# Helper function to generate a simple HTTP response
def generate_error_response(error_body, status_code=400):
    return {
        'statusCode': status_code,
        'body': json.dumps(error_body)
    }
    
    
# Helper function to extract id and access tokens from a request header string
def extract_token(cookie_name, cookie_string):
    token = None
    
    parsed_cookies = cookie_string.split(cookie_name)
    if len(parsed_cookies) == 2:
        token = parsed_cookies[1]
        
        parsed_cookies2 = token.split('; __Host-')
        if len(parsed_cookies2) >= 2:
            token = parsed_cookies2[0]
    
    return token
