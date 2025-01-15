import json
import boto3
import re


client_bedrock_knowledgebase = boto3.client('bedrock-agent-runtime')

def sanitize_prompt(prompt):
   
    sanitized_prompt = prompt.strip().strip('"')
    sanitized_prompt = re.sub(r'""', '"', sanitized_prompt)
    return sanitized_prompt

def lambda_handler(event, context):
    # Log the incoming event
    print(f"Received event: {json.dumps(event)}")
    
    # Ensure the event has a 'prompt' key
    if 'prompt' not in event:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'The request object must contain a "prompt" field.'})
        }

    
    user_prompt = event['prompt']
    print(f"Original prompt: {user_prompt}")
    user_prompt = sanitize_prompt(user_prompt)
    print(f"Sanitized prompt: {user_prompt}")


    try:
        client_knowledgebase = client_bedrock_knowledgebase.retrieve_and_generate(
            input={
                'text': user_prompt
            },
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': 'E5JK9FLBOU',
                    'modelArn': 'arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0'
                }
            }
        )
        
        response_kbase_final = client_knowledgebase['output']['text']
        
        return {
        'statusCode': 200,
        'headers': {
  "Access-Control-Allow-Headers": "'Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,X-Requested-With,Accept,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Allow-Headers,HTTP'",
  "Access-Control-Allow-Origin": "'*'",
  "Access-Control-Allow-Methods": "'DELETE,GET,HEAD,OPTIONS,PATCH,POST,PUT'"
 },
        'body': response_kbase_final
    }

    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error.'})
        }
