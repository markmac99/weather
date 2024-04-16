# Copyright (C) 2018-2023 Mark McIntyre
########################################################################
resource "aws_s3_bucket" "mjmm_weatherdata" {
  bucket = "mjmm-weatherdata"
  tags = {
    "billingtag" = "weather"
  }
}

resource "aws_s3_bucket_logging" "mjmm_weatherdata" {
  bucket        = aws_s3_bucket.mjmm_weatherdata.bucket
  target_bucket = "mjmmauditing"
  target_prefix = "weatherdata-logs/"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "mjmm_weatherdata" {
  bucket = aws_s3_bucket.mjmm_weatherdata.bucket

  rule {
    bucket_key_enabled = false
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "mjmm_weatherdata" {
  bucket = aws_s3_bucket.mjmm_weatherdata.id
  versioning_configuration {
    status = "Suspended"
  }
}

