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
    # If globalSignout query parameter is not provided, default to False
    isGlobalSignout = 'false'
    try:
        isGlobalSignout = event.get('queryStringParameters', {}).get('globalSignout', 'false')
    except:
        isGlobalSignout = 'false'
        
    response_message = 'Signout successful'
    if isGlobalSignout == 'true':
        try:
            access_token = event['requestContext']['authorizer']['access_token']
            cognito_client.global_sign_out(AccessToken=access_token)
        except botocore.exceptions.ClientError as error:
            return generate_response({ 'message': error.response['Error']['Message'], 'code': error.response['Error']['Code'] }, error.response['ResponseMetadata']['HTTPStatusCode'])
        except:
            return generate_response({ 'message': 'An unknown server error has occured' }, 500)
            
        response_message = 'Global signout successful'
    
    return {
        'statusCode': 200,
        'multiValueHeaders': {
            'Set-Cookie': [
                f'__Host-accessToken=invalid-token; Secure; HttpOnly; SameSite=Strict; Path=/; Max-Age=1',
                f'__Host-idToken=invalid-token; Secure; HttpOnly; SameSite=Strict; Path=/; Max-Age=1',
                f'__Host-refreshToken=invalid-token; Secure; HttpOnly; SameSite=Strict; Path=/; Max-Age=1'                                                                                                     
            ]
        },
        'body': json.dumps({ 'message': response_message })
    }
    
    
# Helper function to generate a simple HTTP response
def generate_response(response_body, status_code=200):
    return {
        'statusCode': status_code,
        'body': json.dumps(response_body)
    }