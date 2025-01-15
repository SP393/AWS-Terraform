variable "AWS_REGION" {
  default   = "us-east-2"
  type      = string
  sensitive = true
}

variable "AWS_ACCOUNT_ID" {
  default   = "533267275355"
  type      = string
  sensitive = true
}


variable "lambda" {
  description = "Map of Lambda function names"
  type        = map(any)
  default = {
    Enterprise-LLM-Lambda-Bedrock = {
      name = "Enterprise-LLM-Lambda-Bedrock"
    },
    cognitoMFAAuth = {
      name = "cognitoMFAAuth"
    },
    cognitoSendForgotPasswordEmail = {
      name = "cognitoSendForgotPasswordEmail"
    },
    adminCreateAccount = {
      name = "adminCreateAccount"
    },
    assistant-based-add-conversation = {
      name = "assistant-based-add-conversation"
    },
    authorizeUser = {
      name = "authorizeUser"
    },
    cognitoChangeForgottenPassword = {
      name = "cognitoChangeForgottenPassword"
    },
    cognitoFinalizeAccount = {
      name = "cognitoFinalizeAccount"
    },
    cognitoInitiateAuth = {
      name = "cognitoInitiateAuth"
    },
    cognitoRefreshTokens = {
      name = "cognitoRefreshTokens"
    },
    cognitoResetKnownPassword = {
      name = "cognitoResetKnownPassword"
    },
    cognitoSetupMFA = {
      name = "cognitoSetupMFA"
    },
    cognitoSignout = {
      name = "cognitoSignout"
    },
    get-list-of-user = {
      name = "get-list-of-user"
    },
    getUserData = {
      name = "getUserData"
    },
    update-user-data = {
      name = "update-user-data"
    },
  }
}

variable "api-gateway-parent" {
  description = "Map API gateway resource paths."
  type        = map(any)
  default = {
    Enterprise-LLM = {
      path_part = "Enterprise-LLM"
    },
    assistantidMain = {
      path_part = "assistantid"
    },
    api = {
      path_part = "api"
    },

    auth = {
      path_part = "auth"
    },
    admin = {
      path_part = "admin"
      parent    = "api"
    }


  }
}


variable "api-gateway-methods" {
  description = "Map API gateway methods."
  type        = map(any)
  default = {

    assistantid = {
      path_part = "{assistantid}"
      parent    = "assistantidMain"
      method    = "POST"
      type      = "AWS"
      lambda    = "assistant-based-add-conversation"
    },
    create-user = {
      path_part = "create-user"
      parent    = "admin"
      method    = "POST"
      type      = "AWS"
      lambda    = "adminCreateAccount"
    },
    get-users = {
      path_part = "get-users"
      parent    = "admin"
      method    = "GET"
      type      = "AWS"
      lambda    = "get-list-of-user"
    },
    update-user = {
      path_part = "update-user"
      parent    = "admin"
      method    = "POST"
      type      = "AWS"
      lambda    = "update-user-data"
    }
    mfa-login = {
      path_part = "mfa-login"
      parent    = "auth"
      method    = "POST"
      type      = "AWS"
      lambda    = "cognitoMFAAuth"
    },
    send-forgot-password-email = {
      path_part = "send-forgot-password-email"
      parent    = "auth"
      method    = "POST"
      type      = "AWS"
      lambda    = "cognitoSendForgotPasswordEmail"
    },
    user = {
      path_part = "user"
      parent    = "auth"
      method    = "POST"
      type      = "AWS"
      lambda    = "authorizeUser"
    },
    change-forgotten-password = {
      path_part = "change-forgotten-password"
      parent    = "auth"
      method    = "POST"
      type      = "AWS"
      lambda    = "cognitoChangeForgottenPassword"
    },
    finalize-account = {
      path_part = "finalize-account"
      parent    = "auth"
      method    = "POST"
      type      = "AWS"
      lambda    = "cognitoFinalizeAccount"
    },
    login = {
      path_part = "login"
      parent    = "auth"
      method    = "POST"
      type      = "AWS"
      lambda    = "cognitoInitiateAuth"
    },
    token-refresh = {
      path_part = "token-refresh"
      parent    = "auth"
      method    = "GET"
      type      = "AWS"
      lambda    = "cognitoRefreshTokens"
    },
    reset-known-password = {
      path_part = "reset-known-password"
      parent    = "auth"
      method    = "POST"
      type      = "AWS"
      lambda    = "cognitoResetKnownPassword"
    },
    mfa-setup = {
      path_part = "mfa-setup"
      parent    = "auth"
      method    = "POST"
      type      = "AWS"
      lambda    = "cognitoSetupMFA"
    },
    logout = {
      path_part = "logout"
      parent    = "auth"
      method    = "POST"
      type      = "AWS"
      lambda    = "cognitoSignout"
    }
  }
}
