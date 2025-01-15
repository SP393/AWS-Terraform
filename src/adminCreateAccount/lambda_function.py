import os
from datetime import datetime
import json
import boto3
import botocore
import logging

logger = logging.getLogger()
logger.setLevel('INFO')

cognito_region = os.environ['COGNITO_REGION']
cognito_user_pool_id = os.environ['COGNITO_USER_POOL_ID']
cognito_client = boto3.client('cognito-idp', region_name=cognito_region)

dynamodb = boto3.resource('dynamodb')
ddb_user_table = dynamodb.Table('normalized-user-table')

def lambda_handler(event, context):
    if event['requestContext']['authorizer']['is_admin'] != 'true':
        return generate_response( { 'message': 'Denied access to this resource' }, 403)
    
    request_body = None
    try:
        request_body = json.loads(event['body'])
    except:
        return generate_response({ 'message': 'Request body incorrectly formatted'}, 400)
    
    # Extract request parameters from body
    email = None
    team_id = None
    access_level = None
    assigned_assistants = None
    try:
        email = request_body['email']
        team_id = request_body['teamID']
        access_level = request_body['accessLevel'].lower()
        assigned_assistants = request_body['assignedAssistants']
    except KeyError:
        return generate_response({ 'message': 'Request body missing parameters' }, 400)
        
    # TODO: Add check for valid team_id + assigned_assistants
    if access_level != "admin" or access_level != "user":
        return generate_response({ 'message': 'Invalid access level' }, 400)
        
    # Call AdminCreateUser command
    response = None
    try:
        response = cognito_client.admin_create_user(
            UserPoolId=cognito_user_pool_id,
            Username=email,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email,
                },
                {
                    'Name': 'email_verified',
                    'Value': 'true',
                },
                {
                    'Name': 'custom:Role',
                    'Value': access_level,
                },
                {
                    'Name': 'custom:Team',
                    'Value': team_id,
                },
                {
                    'Name': 'custom:Assistants',
                    'Value': ', '.join(assigned_assistants),
                },
            ],
            DesiredDeliveryMediums=['EMAIL']
        )
    except botocore.exceptions.ClientError as error:
        error_code = error.response['Error']['Code']
        error_message = error.response['Error']['Message']
        http_status_code = error.response['ResponseMetadata']['HTTPStatusCode']
        return generate_response({ 'message': error_message, 'code': error_code }, http_status_code)
        
    # Call AdminAddUserToGroup
    if access_level == 'admin':
        try:
            cognito_client.admin_add_user_to_group(
                UserPoolId=cognito_user_pool_id,
                Username=email,
                GroupName='Admin',
            )
        except botocore.exceptions.ClientError as error:
            assign_admin_error_response = { 'message': error.response['Error']['Message'], 'code': error.response['Error']['Code'] }
            assign_admin_response_status_code = error.response['ResponseMetadata']['HTTPStatusCode']
            
            # If add to admin group fails, abort action and delete created cognito account
            return handle_failed_command(response['User']['Username'], 'admin-assign', assign_admin_error_response, assign_admin_response_status_code)
    
    # Add user data to database
    try:
        ddb_user_table.put_item(
            Item={
                'id': response['User']['Username'],
                'creationTime': datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
                'email': email,
                'employmentType': 'intern',
                'deleteBy': '2024-12-31',
                'givenName': '',
                'familyName': '',
                'searchName': '',
                'accessLevel': access_level,
                'team': team_id,
                'assignedAssistants': assigned_assistants,
            }
        )
    except botocore.exceptions.ClientError as error:
        add_to_db_error_response = { 'message': error.response['Error']['Message'], 'code': error.response['Error']['Code'] }
        add_to_db_response_status_code = error.response['ResponseMetadata']['HTTPStatusCode']
        
        # If add to database fails, abort action and delete created cognito account
        return handle_failed_command(response['User']['Username'], 'add-to-db', add_to_db_error_response, add_to_db_response_status_code)
        
    return {
        'statusCode': 200,
        'body': json.dumps({ 'message': f'{access_level.capitalize()} account created for {email}' })
    }

    
# Helper function to generate a simple HTTP response
def generate_response(response_body, status_code=200):
    return {
        'statusCode': status_code,
        'body': json.dumps(response_body)
    }
    
    
# Helper function to delete an account in Cognito if other steps in the account creation process fail
def handle_failed_command(account_username, failure_step, failure_step_response, failure_step_status_code):
    try:
        cognito_client.admin_delete_user(
            UserPoolId=cognito_user_pool_id,
            Username=account_username
        )
    except botocore.exceptions.ClientError as error:
        deletion_error_response = { 'message': 'A critical error has occured. Contact developers for help.', 'deleteErrorMessage': error.response['Error']['Message'], 'deleteErrorCode': error.response['Error']['Code'] }
        deletion_error_response['failureStepErrorMessage'] = failure_step_response['message']
        deletion_error_response['failureStepErrorCode'] = failure_step_response['code']
        deletion_error_response['failureStep'] = failure_step
        return generate_response(deletion_error_response, 500)
        
    return generate_response(failure_step_response, failure_step_status_code)