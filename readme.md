# Cloud Exfiltrator

Exfiltrate data from AWS cloud environment given some credentials

## Description

This project provides some tools for testing how an attacker would do an exfiltration of data from an AWS account after acquiring access keys. This set of scripts could be used to generate example CloudTrail logs which is useful for defining alerting and monitoring rules.

## Usage

1. Install packages
```bash
pip install -r requirements.txt
```

2. Edit configuration

3. Begin S3 exfiltration
```bash
python s3.py
```