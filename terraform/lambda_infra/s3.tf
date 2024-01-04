resource "aws_s3_object" "lambda_file" {
  bucket     = var.experiment_bucket
  key        = "experiment_code_lambda-${var.owner}.zip"
  source     = data.archive_file.lambda_source_package.output_path
  depends_on = [data.archive_file.lambda_source_package]
  kms_key_id = aws_kms_key.s3_key.arn
}