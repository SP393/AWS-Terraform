import json
import boto3
from boto3.dynamodb.conditions import Attr
import botocore

cognito_client = boto3.client('cognito-idp')
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('enterprise-llm-users')

def lambda_handler(event, context):
    user_id = event['requestContext']['authorizer']['user_id']
    is_admin = event['requestContext']['authorizer']['is_admin']
    
    if is_admin == 'false':
        return {
            "statusCode": 401,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps({'message': 'you do not have admin access'})
        }
    
    response = {
        "users": [],
        "exclusiveStartKey": None
    }
    status_code = None
    
    query_param = event.get('queryStringParameters', {})
    filter_name = query_param.get("name", "")
    filter_value = query_param.get("value", "")
    exclusive_start_key = query_param.get("exclusiveStartKey")
    
    try:
        # parameters for dynamodb scan()
        scan_params = {
            "Limit": 10
        }
        
        # If there was a exclusive start key (pagination), add to the scan params
        if exclusive_start_key:
            scan_params["ExclusiveStartKey"] = json.loads(exclusive_start_key)
        
        if filter_name != "" and filter_value != "":
            scan_params["FilterExpression"] = Attr(f"{filter_name}").eq(f"{filter_value.lower()}")
        
        get_users = table.scan(**scan_params)
        
        users_list = get_users.get("Items", [])

        # Sort the list by the 'FirstName' attribute
        sorted_list = sorted(users_list, key=lambda person: person['firstName'])
        
        # Filter the results to make sure current logged in user is not returned as well
        for user in sorted_list:
           if user.get("UserID") != user_id:
               response["users"].append(user)
        
        # If an exclusive start is returned, add to the response as well
        if 'LastEvaluatedKey' in get_users:
            response["exclusiveStartKey"] = json.dumps(get_users["LastEvaluatedKey"])
        
        status_code = 200
    
    except botocore.exceptions.ClientError as error:
        status_code = 500
        response = error.response['Error']['Message']
        
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Methods": "OPTIONS,GET"
        },
        "body": json.dumps(response)
    }