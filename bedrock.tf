# resource "aws_bedrockagent_knowledge_base" "Enterprise-LLM-Knowledge-base-1024" {
#   name     = "Enterprise-LLM-Knowledge-base-1024"
#   role_arn = "arn:aws:iam::533267275355:role/service-role/AmazonBedrockExecutionRoleForKnowledgeBase_pq4wx"
#   knowledge_base_configuration {
#     vector_knowledge_base_configuration {
#       embedding_model_arn = "arn:aws:bedrock:us-west-2::foundation-model/amazon.titan-embed-text-v2"
#     }
#     type = "VECTOR"
#   }
#   storage_configuration {
#     type = "PINECONE"
#     pinecone_configuration {
#       connection_string = "https://bedrock-knowledge-base-1024-kkr97mt.svc.aped-4627-b74a.pinecone.io"
#       field_mapping {
#         text_field     = "bedrock-knowledge-base-1024-index"
#         metadata_field = "LLM-metadata"
#       }
#       credentials_secret_arn = "arn:aws:secretsmanager:us-east-1:533267275355:secret:enterprise-llm-gg2nV1"
#     }

#   }
# }

# resource "aws_bedrockagent_data_source" "data-ellm" {
#   knowledge_base_id = aws_bedrockagent_knowledge_base.Enterprise-LLM-Knowledge-base-1024.id
#   name              = "Global-opportunity-working-pdf"
#   data_source_configuration {
#     type = "S3"
#     s3_configuration {
#       bucket_arn = aws_s3_bucket.tf-ent-llm.arn
#     }
#   }
# }
