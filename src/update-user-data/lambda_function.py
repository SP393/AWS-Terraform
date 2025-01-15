import json
import boto3
import botocore

cognito_client = boto3.client('cognito-idp')
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('enterprise-llm-users')

def lambda_handler(event, context):
    is_admin = event['requestContext']['authorizer']['is_admin']
    
    if is_admin == 'false':
        return {
            "statusCode": 401,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps({'message': 'you do not have admin access'})
        }
    
    response = None
    status_code = None
    
    # Values to be used for updating dynamoDB entry (notice: the space after "SET" is necessary)
    UpdateExpression="SET "
    ExpressionAttributeValues={}
    
    request_body_str = event['body']
    request_body = json.loads(request_body_str)
    
    if "firstName" in request_body:
        UpdateExpression += "firstName = :firstName,"
        ExpressionAttributeValues[":firstName"] = request_body.get('firstName')
        
        try:
            cognito_client.admin_update_user_attributes(
                UserPoolId= 'us-east-1_ozijXGPMA',
                Username= request_body.get('userId'),
                UserAttributes=[
                    {
                        'Name': 'given_name',
                        'Value': request_body.get('firstName')
                    }
                ]
            )
        except botocore.exceptions.ClientError as error:
            response = error.response['Error']['Message']
            status_code = 500
            
    if "lastName" in request_body:
        UpdateExpression += "lastName = :lastName,"
        ExpressionAttributeValues[":lastName"] = request_body.get('lastName')
        
        try:
            cognito_client.admin_update_user_attributes(
                UserPoolId= 'us-east-1_ozijXGPMA',
                Username=request_body.get('userId'),
                UserAttributes=[
                    {
                        'Name': 'family_name',
                        'Value': request_body.get('lastName')
                    }
                ]
            )
        except botocore.exceptions.ClientError as error:
            response = error.response['Error']['Message']
            status_code = 500
            
    if "role" in request_body:
        UpdateExpression += "role = :role,"
        ExpressionAttributeValues[":role"] = request_body.get('role')
    if "team" in request_body:
        UpdateExpression += "team = :team,"
        ExpressionAttributeValues[":team"] = request_body.get('team')
        
    if "endDate" in request_body:
        UpdateExpression += "endDate = :endDate,"
        ExpressionAttributeValues[":endDate"] = request_body.get('endDate')
    
    # remove trailing comma
    if UpdateExpression.endswith(','):
        UpdateExpression = UpdateExpression[:-1]
        
    try:
        response = table.update_item(
            Key={"UserID": request_body.get('userId')},
            UpdateExpression=UpdateExpression,
            ExpressionAttributeValues=ExpressionAttributeValues
        )
        
        status_code = 200
    
    except botocore.exceptions.ClientError as error:
        response = error.response['Error']['Message']
        status_code = 500
    
    return {
        'statusCode': status_code,
        'headers':{
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Methods": "OPTIONS,POST"
        },
        'body': json.dumps(response)
    }
