resource "aws_cognito_user_pool" "ellm" {
  name = "tf-Enterprise-llm"
  password_policy {
    minimum_length                   = 8
    require_lowercase                = true
    require_uppercase                = true
    require_numbers                  = true
    require_symbols                  = true
    temporary_password_validity_days = 7
  }

  # deletion_protection = "ACTIVE"
  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }

  schema {
    attribute_data_type = "String"
    mutable             = true
    name                = "email"
    required            = true
  }
  schema {
    attribute_data_type = "String"
    mutable             = true
    name                = "given_name"
    required            = true
  }
  schema {
    attribute_data_type = "String"
    mutable             = true
    name                = "family_name"
    required            = true
  }
  schema {
    attribute_data_type = "String"
    mutable             = true
    name                = "Assistants"
    required            = false
  }
  schema {
    attribute_data_type = "String"
    mutable             = true
    name                = "Password"
    required            = false
  }
  schema {
    attribute_data_type = "String"
    mutable             = true
    name                = "Role"
    required            = false
  }
  schema {
    attribute_data_type = "String"
    mutable             = true
    name                = "Team"
    required            = false
  }

  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"
  }
}

resource "aws_cognito_user_pool_client" "client" {
  name                                 = "tf-Enterprise-llm"
  user_pool_id                         = aws_cognito_user_pool.ellm.id
  allowed_oauth_flows_user_pool_client = false
  explicit_auth_flows                  = ["ALLOW_ADMIN_USER_PASSWORD_AUTH", "ALLOW_CUSTOM_AUTH", "ALLOW_USER_PASSWORD_AUTH", "ALLOW_REFRESH_TOKEN_AUTH"]
  access_token_validity                = 1
  refresh_token_validity               = 7
  id_token_validity                    = 1
}
