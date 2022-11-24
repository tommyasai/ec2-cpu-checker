## Prerequisite
```
pip3 install boto3 
pip3 install jmespath
```

## Overview
This is a tool to query CPUUtilizaion for all EC2 instances in account.
It supports to make output to csv. The CSV will saved to your local.

## Usage
1. Set the AWS credentials
```
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
```
TODO: Enable 2FA 

2. Check the target period to check CPU
     If you want to change it, you will need to fix `start_time` and `end_time` in source code



Run `python3 mainy.py`

## Note
Developer Env
```
❯ python3 --version
Python 3.10.6

❯ pip3 --version
pip 22.2.2 from /usr/local/lib/python3.10/site-packages/pip (python 3.10)
```