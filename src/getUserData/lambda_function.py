import json
import boto3
import botocore

dynamodb_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    # Read user ID from context object provided by authorizer
    user_id = event['requestContext']['authorizer']['user_id']
    is_admin = event['requestContext']['authorizer']['is_admin'] == 'true'
    
    error_occurred = False
    user_data_response = None
    try:
        user_data_response = dynamodb_client.get_item(
            TableName='normalized-user-table',
            Key={'id': {'S': user_id}}
        )
    except botocore.exceptions.ClientError as error:
        return generate_error_response(error)
        
    # Fetch team data
    team_data_response = None
    try:
        team_data_response = dynamodb_client.get_item(
            TableName='normalized-team-table',
            Key={ 'id': user_data_response.get('Item', {}).get('team', {}) }
        )
    except botocore.exceptions.ParamValidationError as error:
        team_data_response = None
        error_occurred = True
    except botocore.exceptions.ClientError as error:
        return generate_error_response(error)
        
    # Fetch assigned assistant data
    assistant_ids = [ {'id': id} for id in user_data_response.get('Item', {}).get('assignedAssistants', {}).get('L', []) ]
    assistants_data_response = None
    try:
        assistants_data_response = dynamodb_client.batch_get_item(
            RequestItems={
                'normalized-assistant-table': {
                    'Keys': assistant_ids
                }
            }
        )
    except botocore.exceptions.ParamValidationError as error:
        assistants_data_response = None
        error_occurred = True
    except botocore.exceptions.ClientError as error:
        return generate_error_response(error)
        
    # Construct user data object
    team_data = None
    try:
        team_data = {
            'id': team_data_response['Item']['id']['S'],
            'name': team_data_response['Item']['name']['S'],
            'icon': team_data_response['Item']['icon']['S'],
            'relatedAssistants': [ id['S'] for id in team_data_response['Item']['relatedAssistants']['L'] ]
        }
    except:
        team_data = None
        error_occurred = True
        
    assistants_data = []
    try:
        assistants_data = [ { 'id': data['id']['S'], 'name': data['name']['S'], 'imageLink': data['imageLink']['S'] } for data in assistants_data_response['Responses']['normalized-assistant-table']]
    except:
        assistants_data = []
        error_occurred = True
    
    user_data = user_data_response.get('Item', {})
    complete_user_data = {
        'email': user_data.get('email', {}).get('S'),
        'givenName': user_data.get('givenName', {}).get('S'),
        'familyName': user_data.get('familyName', {}).get('S'),
        'accessLevel': user_data.get('accessLevel', {}).get('S'),
        'employmentType': user_data.get('employmentType', {}).get('S'),
        'creationTime': user_data.get('creationTime', {}).get('S'),
        'accountDeletionDate': user_data.get('deleteBy', {}).get('S'),
        'team': team_data,
        'assistants': assistants_data,
    }
    
    response_message = 'Successful user data fetch'
    if error_occurred:
        response_message = 'A minor error has occurred during team/assistant data fetch'
    
    return generate_response({ 'message': response_message, 'data': complete_user_data })
    
    
# Helper function to generate a simple HTTP response
def generate_response(response_body, status_code=200):
    return {
        'statusCode': status_code,
        'body': json.dumps(response_body)
    }
    
    
# Helper function to generate an error HTTP response from a raised botocore exception
def generate_error_response(error):
    error_code = error.response['Error']['Code']
    error_message = error.response['Error']['Message']
    http_status_code = error.response['ResponseMetadata']['HTTPStatusCode']
    return generate_response({ 'message': 'A server error has occured while fetching user data', 'detailedMessage': error_message }, 500)