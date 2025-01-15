data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

//Lambda source code

data "archive_file" "source-file" {
  for_each    = var.lambda
  type        = "zip"
  source_file = "${path.module}/src/${each.value.name}/lambda_function.py"
  output_path = each.value.name
}

# data "archive_file" "cognitoMFAAuth" {
#   type        = "zip"
#   source_file = "${path.module}/src/cognitoMFAAuth/lambda_function.py"
#   output_path = "cognitoMFAAuth.zip"
# }

# data "archive_file" "cognitoSendForgotPasswordEmail" {
#   type        = "zip"
#   source_file = "${path.module}/src/cognitoSendForgotPasswordEmail/lambda_function.py"
#   output_path = "cognitoSendForgotPasswordEmail.zip"
# }

# data "archive_file" "adminCreateAccount" {
#   type        = "zip"
#   source_file = "${path.module}/src/adminCreateAccount/lambda_function.py"
#   output_path = "adminCreateAccount.zip"
# }

# data "archive_file" "assistant-based-add-conversation" {
#   type        = "zip"
#   source_file = "${path.module}/src/assistant-based-add-conversation/lambda_function.py"
#   output_path = "assistant-based-add-conversation.zip"
# }

# data "archive_file" "authorizeUser" {
#   type        = "zip"
#   source_file = "${path.module}/src/authorizeUser/lambda_function.py"
#   output_path = "authorizeUser.zip"
# }

# data "archive_file" "cognitoChangeForgottenPassword" {
#   type        = "zip"
#   source_file = "${path.module}/src/cognitoChangeForgottenPassword/lambda_function.py"
#   output_path = "cognitoChangeForgottenPassword.zip"
# }

# data "archive_file" "cognitoFinalizeAccount" {
#   type        = "zip"
#   source_file = "${path.module}/src/cognitoFinalizeAccount/lambda_function.py"
#   output_path = "cognitoFinalizeAccount.zip"
# }

# data "archive_file" "cognitoInitiateAuth" {
#   type        = "zip"
#   source_file = "${path.module}/src/cognitoInitiateAuth/lambda_function.py"
#   output_path = "cognitoInitiateAuth.zip"
# }

# data "archive_file" "cognitoRefreshTokens" {
#   type        = "zip"
#   source_file = "${path.module}/src/cognitoRefreshTokens/lambda_function.py"
#   output_path = "cognitoRefreshTokens.zip"
# }

# data "archive_file" "cognitoResetKnownPassword" {
#   type        = "zip"
#   source_file = "${path.module}/src/cognitoResetKnownPassword/lambda_function.py"
#   output_path = "cognitoResetKnownPassword.zip"
# }

# data "archive_file" "cognitoSetupMFA" {
#   type        = "zip"
#   source_file = "${path.module}/src/cognitoSetupMFA/lambda_function.py"
#   output_path = "cognitoSetupMFA.zip"
# }

# data "archive_file" "cognitoSignout" {
#   type        = "zip"
#   source_file = "${path.module}/src/cognitoSignout/lambda_function.py"
#   output_path = "cognitoSignout.zip"
# }

# data "archive_file" "get-list-of-user" {
#   type        = "zip"
#   source_file = "${path.module}/src/get-list-of-user/lambda_function.py"
#   output_path = "get-list-of-user.zip"
# }

# data "archive_file" "getUserData" {
#   type        = "zip"
#   source_file = "${path.module}/src/getUserData/lambda_function.py"
#   output_path = "getUserData.zip"
# }

# data "archive_file" "update-user-data" {
#   type        = "zip"
#   source_file = "${path.module}/src/update-user-data/lambda_function.py"
#   output_path = "update-user-data.zip"
# }


