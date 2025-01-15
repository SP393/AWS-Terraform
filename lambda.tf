# Enterprise-LLM-Lambda-Bedrock function 

resource "aws_lambda_function" "lambda-functions" {
  for_each      = var.lambda
  filename      = "${each.value.name}.zip"
  function_name = each.key
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "lambda_handler"

  source_code_hash = data.archive_file.source-file[each.key].output_base64sha256

  runtime = "python3.10"

}

# # cognitoMFAAuth function 

# resource "aws_lambda_function" "cognitoMFAAuth" {
#   filename         = "cognitoMFAAuth.zip"
#   function_name    = "cognitoMFAAuth"
#   role             = aws_iam_role.iam_for_lambda.arn
#   handler          = "lambda_handler"
#   source_code_hash = data.archive_file.cognito-mfaauth.output_base64sha256

#   runtime = "python3.10"

# }

# # cognitoSendForgotPasswordEmail function 

# resource "aws_lambda_function" "cognitoSendForgotPasswordEmail" {
#   filename      = "cognitoSendForgotPasswordEmail.zip"
#   function_name = "cognitoSendForgotPasswordEmail"
#   role          = aws_iam_role.iam_for_lambda.arn
#   handler       = "lambda_handler"

#   source_code_hash = data.archive_file.cognitoSendForgotPasswordEmail.output_base64sha256

#   runtime = "python3.10"

# }

# # adminCreateAccount function 

# resource "aws_lambda_function" "adminCreateAccount" {
#   filename      = "adminCreateAccount.zip"
#   function_name = "adminCreateAccount"
#   role          = aws_iam_role.iam_for_lambda.arn
#   handler       = "lambda_handler"

#   source_code_hash = data.archive_file.adminCreateAccount.output_base64sha256

#   runtime = "python3.10"

# }

# # adminCreateAccount function 

# resource "aws_lambda_function" "assistant-based-add-conversation" {
#   filename      = "assistant-based-add-conversation.zip"
#   function_name = "assistant-based-add-conversation"
#   role          = aws_iam_role.iam_for_lambda.arn
#   handler       = "lambda_handler"

#   source_code_hash = data.archive_file.assistant-based-add-conversation.output_base64sha256

#   runtime = "python3.10"

# }

# # authorizeUser function 

# resource "aws_lambda_function" "authorizeUser" {
#   filename      = "authorizeUser.zip"
#   function_name = "authorizeUser"
#   role          = aws_iam_role.iam_for_lambda.arn
#   handler       = "lambda_handler"

#   source_code_hash = data.archive_file.authorizeUser.output_base64sha256

#   runtime = "python3.10"

# }

# # cognitoChangeForgottenPassword function 

# resource "aws_lambda_function" "cognitoChangeForgottenPassword" {
#   filename      = "cognitoChangeForgottenPassword.zip"
#   function_name = "cognitoChangeForgottenPassword"
#   role          = aws_iam_role.iam_for_lambda.arn
#   handler       = "lambda_handler"

#   source_code_hash = data.archive_file.cognitoChangeForgottenPassword.output_base64sha256

#   runtime = "python3.10"

# }

# # cognitoFinalizeAccount function 

# resource "aws_lambda_function" "cognitoFinalizeAccount" {
#   filename      = "cognitoFinalizeAccount.zip"
#   function_name = "cognitoFinalizeAccount"
#   role          = aws_iam_role.iam_for_lambda.arn
#   handler       = "lambda_handler"

#   source_code_hash = data.archive_file.cognitoFinalizeAccount.output_base64sha256

#   runtime = "python3.10"

# }

# # cognitoInitiateAuth function 

# resource "aws_lambda_function" "cognitoInitiateAuth" {
#   filename      = "cognitoInitiateAuth.zip"
#   function_name = "cognitoInitiateAuth"
#   role          = aws_iam_role.iam_for_lambda.arn
#   handler       = "lambda_handler"

#   source_code_hash = data.archive_file.cognitoInitiateAuth.output_base64sha256

#   runtime = "python3.10"

# }

# # cognitoRefreshTokens function 

# resource "aws_lambda_function" "cognitoRefreshTokens" {
#   filename      = "cognitoRefreshTokens.zip"
#   function_name = "cognitoRefreshTokens"
#   role          = aws_iam_role.iam_for_lambda.arn
#   handler       = "lambda_handler"

#   source_code_hash = data.archive_file.cognitoRefreshTokens.output_base64sha256

#   runtime = "python3.10"

# }

# # cognitoResetKnownPassword function 

# resource "aws_lambda_function" "cognitoResetKnownPassword" {
#   filename      = "cognitoResetKnownPassword.zip"
#   function_name = "cognitoResetKnownPassword"
#   role          = aws_iam_role.iam_for_lambda.arn
#   handler       = "lambda_handler"

#   source_code_hash = data.archive_file.cognitoResetKnownPassword.output_base64sha256

#   runtime = "python3.10"

# }

# # cognitoSetupMFA function 

# resource "aws_lambda_function" "cognitoSetupMFA" {
#   filename      = "cognitoSetupMFA.zip"
#   function_name = "cognitoSetupMFA"
#   role          = aws_iam_role.iam_for_lambda.arn
#   handler       = "lambda_handler"

#   source_code_hash = data.archive_file.cognitoSetupMFA.output_base64sha256

#   runtime = "python3.10"

# }

# # cognitoSignout function 

# resource "aws_lambda_function" "cognitoSignout" {
#   filename      = "cognitoSignout.zip"
#   function_name = "cognitoSignout"
#   role          = aws_iam_role.iam_for_lambda.arn
#   handler       = "lambda_handler"

#   source_code_hash = data.archive_file.cognitoSignout.output_base64sha256

#   runtime = "python3.10"

# }

# # get-list-of-user function 

# resource "aws_lambda_function" "get-list-of-user" {
#   filename      = "get-list-of-user.zip"
#   function_name = "get-list-of-user"
#   role          = aws_iam_role.iam_for_lambda.arn
#   handler       = "lambda_handler"

#   source_code_hash = data.archive_file.get-list-of-user.output_base64sha256

#   runtime = "python3.10"

# }

# # getUserData function 

# resource "aws_lambda_function" "getUserData" {
#   filename      = "getUserData.zip"
#   function_name = "getUserData"
#   role          = aws_iam_role.iam_for_lambda.arn
#   handler       = "lambda_handler"

#   source_code_hash = data.archive_file.getUserData.output_base64sha256

#   runtime = "python3.10"

# }

# # update-user-data function 

# resource "aws_lambda_function" "update-user-data" {
#   filename      = "update-user-data.zip"
#   function_name = "update-user-data"
#   role          = aws_iam_role.iam_for_lambda.arn
#   handler       = "lambda_handler"

#   source_code_hash = data.archive_file.update-user-data.output_base64sha256

#   runtime = "python3.10"

# }
