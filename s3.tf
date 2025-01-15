resource "aws_s3_bucket" "tf-ent-llm" {
  bucket              = "tf-ent-llm"
  object_lock_enabled = true

}

resource "aws_s3_bucket_versioning" "versioning_ellm" {
  bucket = aws_s3_bucket.tf-ent-llm.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_object" "knowledge-base" {
  bucket = aws_s3_bucket.tf-ent-llm.id
  key    = "knowledge-base/Global-opportunity-working.pdf "
  source = "Object-files/Global-opportunity-working.pdf"
}
