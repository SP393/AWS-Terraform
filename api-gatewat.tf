resource "aws_api_gateway_rest_api" "Enterprise-LLM-Bedrock-API" {
  name = "Tf-Enterprise-LLM-Bedrock-API"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "Enterprise-LLM-Parent-Resource" {
  for_each    = var.api-gateway-parent
  rest_api_id = aws_api_gateway_rest_api.Enterprise-LLM-Bedrock-API.id
  parent_id   = aws_api_gateway_rest_api.Enterprise-LLM-Bedrock-API.root_resource_id
  path_part   = each.value.path_part
}

# resource "aws_api_gateway_resource" "Enterprise-LLM-ChildFirst-Resource" {
#   for_each    = var.api-gateway-first-child
#   rest_api_id = aws_api_gateway_rest_api.Enterprise-LLM-Bedrock-API.id
#   parent_id   = aws_api_gateway_resource.Enterprise-LLM-Parent-Resource[each.value.parent].id
#   path_part   = each.value.path_part
# }
resource "aws_api_gateway_resource" "Enterprise-LLM-Main-Resource" {
  for_each    = var.api-gateway-methods
  rest_api_id = aws_api_gateway_rest_api.Enterprise-LLM-Bedrock-API.id
  # parent_id   = aws_api_gateway_resource.Enterprise-LLM-Parent-Resource[each.value.parent].id != null ? aws_api_gateway_resource.Enterprise-LLM-Parent-Resource[each.value.parent].id : aws_api_gateway_resource.Enterprise-LLM-ChildFirst-Resource[each.value.parent].id
  parent_id = aws_api_gateway_resource.Enterprise-LLM-Parent-Resource[each.value.parent].id

  path_part = each.value.path_part
}

resource "aws_api_gateway_method" "Enterprise-LLM-Method" {
  for_each      = var.api-gateway-methods
  rest_api_id   = aws_api_gateway_rest_api.Enterprise-LLM-Bedrock-API.id
  resource_id   = aws_api_gateway_resource.Enterprise-LLM-Main-Resource[each.key].id
  http_method   = each.value.method
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "Integration" {
  for_each                = var.api-gateway-methods
  rest_api_id             = aws_api_gateway_rest_api.Enterprise-LLM-Bedrock-API.id
  resource_id             = aws_api_gateway_resource.Enterprise-LLM-Main-Resource[each.key].id
  http_method             = aws_api_gateway_method.Enterprise-LLM-Method[each.key].http_method
  integration_http_method = each.value.method
  type                    = "AWS"
  uri                     = aws_lambda_function.lambda-functions[each.value.lambda].invoke_arn
}

resource "aws_lambda_permission" "apigw-lambda" {
  for_each      = var.api-gateway-methods
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda-functions[each.value.lambda].function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "arn:aws:execute-api:${var.AWS_REGION}:${var.AWS_ACCOUNT_ID}:${aws_api_gateway_rest_api.Enterprise-LLM-Bedrock-API.id}/*/${aws_api_gateway_method.Enterprise-LLM-Method[each.key].http_method}${aws_api_gateway_resource.Enterprise-LLM-Main-Resource[each.key].path}"
}



resource "aws_api_gateway_method_response" "response_200" {
  for_each    = var.api-gateway-methods
  rest_api_id = aws_api_gateway_rest_api.Enterprise-LLM-Bedrock-API.id
  resource_id = aws_api_gateway_resource.Enterprise-LLM-Main-Resource[each.key].id
  http_method = aws_api_gateway_method.Enterprise-LLM-Method[each.key].http_method
  status_code = "200"
}

resource "aws_api_gateway_integration_response" "Integration-Response" {
  for_each    = var.api-gateway-methods
  rest_api_id = aws_api_gateway_rest_api.Enterprise-LLM-Bedrock-API.id
  resource_id = aws_api_gateway_resource.Enterprise-LLM-Main-Resource[each.key].id
  http_method = aws_api_gateway_method.Enterprise-LLM-Method[each.key].http_method
  status_code = aws_api_gateway_method_response.response_200[each.key].status_code


  response_templates = {
    "application/json" = <<EOF
#set($inputRoot = $input.path('$'))
{1,2,3}
EOF
  }
}


resource "aws_api_gateway_deployment" "tf-ellm" {
  # for_each = var.api-gateway-methods
  # depends_on = [
  #   aws_api_gateway_integration.Enterprise-LLM
  # ]
  rest_api_id = aws_api_gateway_rest_api.Enterprise-LLM-Bedrock-API.id
  lifecycle {
    create_before_destroy = true
  }
  stage_name = "dev"
}
