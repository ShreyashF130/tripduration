# import boto3
# import shutil
# from botocore.exceptions import NoCredentialsError

# def upload_to_s3(local_file_path,bucketname,s3_file_path):
#     s3 = boto3.client('s3')

#     try:
#         # s3.upload(local_file_path,bucket_name,s3_file_path)
#         s3.upload_file(local_file_path, bucket_name, s3_file_path)
#         print(f"FIle uploaded successfully to {bucket_name}/{s3_file_path}")
#     except FileNotFoundError:
#         print(f"File {local_file_path} was not found")
#     except NoCredentialsError:
#         print("Credentials not available")

# local_model_path = 'C:\Users\Shreyash\tripduration\tripduration\models\model.joblib'
# bucket_name = 'nyc-taxi-first'
# s3_file_path = 'C:\Users\Shreyash\tripduration\tripduration\models\model.joblib'

# upload_to_s3(local_model_path,bucket_name,s3_file_path)
# shutil.copy(local_model_path,'model.joblib')





import boto3
import shutil
import pathlib
from botocore.exceptions import NoCredentialsError

def upload_to_s3(local_file_path, bucket_name, s3_file_path):
    s3 = boto3.client('s3')

    try:
        s3.upload_file(local_file_path, bucket_name, s3_file_path)
        print(f"File uploaded successfully to {bucket_name}/{s3_file_path}")
    except FileNotFoundError:
        print(f"File {local_file_path} was not found")
    except NoCredentialsError:
        print("Credentials not available")

# 1. Dynamically find the project root folder (just like in train_model.py)
curr_dir = pathlib.Path(__file__)
home_dir = curr_dir.parent.parent.parent # Backs out of src/models/ to the root

# 2. Build the exact absolute paths
local_model_path = (home_dir / 'models' / 'model.joblib').as_posix()
bucket_name = 'nyc-taxi-first'
s3_file_path = 'models/model.joblib'

# 3. Upload to S3
upload_to_s3(local_model_path, bucket_name, s3_file_path)

# 4. Copy the model to the root folder (for Docker later)
shutil.copy(local_model_path, (home_dir / 'model.joblib').as_posix())