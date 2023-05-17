the app is: Lambda Function and Deployment on AWS using the Serverless Framework

the files we have decided to generate are: lambda_handler.py, requirements.txt, serverless.yml, install_plugins.sh, .env

Shared dependencies:

1. Environment Variables:
   - OEC_ECI_trade_ENDPOINT

2. Bucket and Directory Names:
   - Bucket: sumeo-OEC
   - Directory: data_profile=raw/provider_name=OEC/dataset_name=ECI_trade/request_time=request_day/

3. Function Names:
   - Lambda function: lambda_data_to_s3

4. Data Schemas:
   - Metadata:
     - Request time in UTC
     - Provider: OEC
     - Dataset name: ECI_trade

5. File Names:
   - lambda_handler.py
   - requirements.txt
   - serverless.yml
   - install_plugins.sh
   - .env

6. AWS Region:
   - eu-west-1

7. Scheduled Event Time:
   - 21:00 UTC