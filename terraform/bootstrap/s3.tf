resource "aws_s3_bucket" "backend_bucket" {
  bucket = "experiment-pipeline-backend-bucket-alpha"
}
#resource "aws_s3_bucket_acl" "backend_bucket_acl" {
#  bucket = aws_s3_bucket.backend_bucket.id
#  acl    = "private"
#}
resource "aws_s3_bucket_public_access_block" "backend_bucket" {
  bucket = aws_s3_bucket.backend_bucket.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
resource "aws_s3_bucket_versioning" "backend_bucket_versioning" {
  bucket = aws_s3_bucket.backend_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "backend_bucket_sse" {
  bucket = aws_s3_bucket.backend_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}