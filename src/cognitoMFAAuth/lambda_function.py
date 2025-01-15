import os
import json
import jwt
import boto3
import botocore
from cryptography.fernet import Fernet
import logging

logger = logging.getLogger()
logger.setLevel('INFO')

client_id = os.environ['COGNITO_CLIENT_ID']
cognito_region = os.environ['COGNITO_REGION']
cognito_user_pool_id = os.environ['COGNITO_USER_POOL_ID']
cognito_client = boto3.client('cognito-idp', region_name=cognito_region)

jwk_client = jwt.PyJWKClient(f'https://cognito-idp.{cognito_region}.amazonaws.com/{cognito_user_pool_id}/.well-known/jwks.json')

fernet = Fernet(os.environ['TOKEN_ENCRYPTION_KEY'].encode())

def lambda_handler(event, context):
    request_body = None
    try:
        request_body = json.loads(event['body'])
    except:
        return generate_response({ 'message': 'Request body incorrectly formatted'}, 400)
    
    # Extract request parameters from body
    session_id = None
    email = None
    mfa_code = None
    try:
        session_id = request_body['sessionId']
        email = request_body['email']
        mfa_code = request_body['mfaCode']
    except KeyError:
        return generate_response({ 'message': 'Request body missing parameters' }, 400)
        
    # Call RespondToAuthChallenge command
    response = None
    try:
        response = cognito_client.respond_to_auth_challenge(
            ClientId=client_id,
            ChallengeName='SOFTWARE_TOKEN_MFA',
            Session=session_id,
            ChallengeResponses={
                'USERNAME': email,
                'SOFTWARE_TOKEN_MFA_CODE': mfa_code,
            },
        )
    except botocore.exceptions.ClientError as error:
        error_code = error.response['Error']['Code']
        error_message = error.response['Error']['Message']
        http_status_code = error.response['ResponseMetadata']['HTTPStatusCode']
        return generate_response({ 'message': error_message, 'code': error_code }, http_status_code)
    
    # Handle auth challenges
    challenge_response = handle_auth_challenge(response, email);
    if challenge_response is not None:
        return challenge_response
    
    # Check if the user is an admin or not
    id_token = response['AuthenticationResult']['IdToken']
    is_admin_check_successful, is_admin = check_is_admin(id_token)
    if not is_admin_check_successful:
        return generate_response({ 'message': 'An error has occurred while decoding JWT' }, 500)

    access_token = response['AuthenticationResult']['AccessToken']
    refresh_token = response['AuthenticationResult']['RefreshToken']
    session_expires_in = response['AuthenticationResult']['ExpiresIn']
    return {
        'statusCode': 200,
        'multiValueHeaders': {
            'Set-Cookie': [
                f'__Host-accessToken={fernet.encrypt(access_token.encode()).decode()}; Secure; HttpOnly; SameSite=Strict; Path=/; Max-Age=604800',
                f'__Host-idToken={fernet.encrypt(id_token.encode()).decode()}; Secure; HttpOnly; SameSite=Strict; Path=/; Max-Age=604800',
                f'__Host-refreshToken={fernet.encrypt(refresh_token.encode()).decode()}; Secure; HttpOnly; SameSite=Strict; Path=/; Max-Age=604800'                                                                                                     
            ]
        },
        'body': json.dumps({ 'message': 'MFA sign in successful', 'isAdmin': is_admin })
    }

    
# Helper function to generate a simple HTTP response
def generate_response(response_body, status_code=200):
    return {
        'statusCode': status_code,
        'body': json.dumps(response_body)
    }

    
# Helper function that handles any auth challenges and returns an appropriate response
# Returns None if there is no auth challenge
def handle_auth_challenge(auth_response, email):
    challenge_name = auth_response.get('ChallengeName', None)
    if challenge_name is None:
        return None
        
    status_code = 200
    response_message = 'Authentication challenge'
    challenge_data = { 'session': auth_response['Session'], 'email': email }
    if challenge_name == 'MFA_SETUP':
        try:
            response = cognito_client.associate_software_token(
                Session = auth_response['Session']
            )
            challenge_data['session'] = response['Session']
            challenge_data['secretCode'] = response['SecretCode']
        except botocore.exceptions.ClientError as error:
            status_code = 500
            response_message = error.response['Error']['Message']
        except:
            status_code = 500
            response_message = 'An unknown error has occured while setting up MFA for this account'
        
    return generate_response({ 'message': response_message, 'challengeName': challenge_name,  'challengeData': challenge_data}, status_code)
    
    
# Helper function to check if authenticated user is an admin or not
def check_is_admin(id_token):
    is_admin = False
    is_admin_check_successful = True
    
    signing_key = jwk_client.get_signing_key_from_jwt(id_token)
    try:
        claims = jwt.decode(
            id_token,
            signing_key.key,
            algorithms=['RS256'],
            audience=client_id,
            issuer=f'https://cognito-idp.us-east-1.amazonaws.com/{cognito_user_pool_id}',
            options={'verify_signature': True, 'require': ['exp']}
        )
        is_admin = 'Admin' in claims.get('cognito:groups', [])
    except:
        is_admin_check_successful = False
        
    return is_admin_check_successful, is_admin