import json
import os
import time
import jwt
from cryptography.fernet import Fernet
import logging

logger = logging.getLogger()
logger.setLevel('INFO')

fernet = Fernet(os.environ['TOKEN_ENCRYPTION_KEY'].encode())

cognito_region = os.environ['COGNITO_REGION']
cognito_user_pool_id = os.environ['COGNITO_USER_POOL_ID']
cognito_client_id = os.environ['COGNITO_CLIENT_ID']

jwk_client = jwt.PyJWKClient(f'https://cognito-idp.{cognito_region}.amazonaws.com/{cognito_user_pool_id}/.well-known/jwks.json')

def lambda_handler(event, context):
    # Parse the input for request information
    arn_resource = event['methodArn']
        
    # Read ID Token from cookies
    request_cookies = event.get('multiValueHeaders', {}).get('cookie', None)
    if request_cookies is None:
        request_cookies = event.get('multiValueHeaders', {}).get('Cookie', None)
        
    if request_cookies is None:
        raise Exception('Unauthorized') # Return a 401 Unauthorized response
        return 'unauthorized'
        
    request_cookies = request_cookies[0]
        
    id_token = extract_token('__Host-idToken=', request_cookies)
    access_token = extract_token('__Host-accessToken=', request_cookies)
            
    if id_token is None or access_token is None:
        refresh_token = extract_token('__Host-refreshToken=', request_cookies)
        if refresh_token is None:
            raise Exception('Unauthorized') # Return a 401 Unauthorized response
            return 'unauthorized'
        else:
            # If refresh token is in request, its possible that the access/id tokens have just expired browser-side
            return generate_deny_request("unknown-user", arn_resource)
    
    # Decrypt ID Token
    decrypted_id_token = None
    decrypted_access_token = None
    try:
        decrypted_id_token = fernet.decrypt(id_token.encode()).decode()
        decrypted_access_token = fernet.decrypt(access_token.encode()).decode()
    except:
        raise Exception('Unauthorized') # Return a 401 Unauthorized response
        return 'unauthorized'
        
    # Decode and verify ID Token
    signing_key = jwk_client.get_signing_key_from_jwt(decrypted_id_token)
    
    token = None
    user_id = None
    exp_time = 0
    is_admin = False
    try:
        token = jwt.decode(
            decrypted_id_token,
            signing_key.key,
            algorithms=['RS256'],
            audience=cognito_client_id,
            issuer=f'https://cognito-idp.us-east-1.amazonaws.com/{cognito_user_pool_id}',
            options={'verify_signature': True, 'verify_exp': False, 'require': ['exp']}
        )
        user_id = token['sub']
        exp_time = token['exp']
    except:
        raise Exception('Unauthorized') # Return a 401 Unauthorized response
        return 'unauthorized'
        
    try:
        is_admin = 'Admin' in token['cognito:groups']
    except KeyError:
        is_admin = False
        
    # Check if the ID Token has expired
    if int(time.time()) > exp_time:
        return generate_deny_request(user_id, arn_resource)
    
    return generate_allow_request(user_id, arn_resource, decrypted_id_token, decrypted_access_token, is_admin)
    
    
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
    
    
# Helper function to generate an AWS IAM policy with a principal identifier (expected return from a REST Lambda authorizer)
# Additionally attaches decrypted id and access tokens for convienence
def generate_policy(principal_id, effect, resource, id_token, access_token, is_admin=False):
    auth_response = {}
    auth_response['principalId'] = principal_id

    policy_document = {}
    policy_document['Version'] = '2012-10-17'
    policy_document['Statement'] = []
    statement = {}
    statement['Action'] = 'execute-api:Invoke'
    statement['Effect'] = effect
    statement['Resource'] = resource
    policy_document['Statement'] = [statement]
    auth_response['policyDocument'] = policy_document
        
    # Context values to pass onto API method
    if effect == 'Allow':
        auth_response['context'] = {
            'id_token': id_token,
            'access_token': access_token,
            'user_id': principal_id,
            'is_admin': is_admin
        }
    elif effect == 'Deny':
        auth_response['context'] = {
            'message': "EXPIRED_TOKEN"
        }

    auth_response_json = json.dumps(auth_response)

    return auth_response

def generate_allow_request(principal_id, resource, id_token, access_token, is_admin):
    return generate_policy(principal_id, 'Allow', resource, id_token, access_token, is_admin)

def generate_deny_request(principal_id, resource):
    return generate_policy(principal_id, 'Deny', resource, None, None)