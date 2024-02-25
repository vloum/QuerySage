import os
import requests
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

from config import TENCENT_SECRET_ID, TENCENT_SECRET_KEY
from urllib.parse import urlparse

from configs.kb_config import KB_ROOT_PATH

REGION = 'ap-guangzhou'     # 替换为用户的 Region
BUCKET = 'public-file-1312069664'
BASEURL = 'https://public-file-1312069664.cos.ap-guangzhou.myqcloud.com/'

token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=REGION, SecretId=TENCENT_SECRET_ID,
           SecretKey=TENCENT_SECRET_KEY, Token=token, Scheme=scheme)
# 2. 获取客户端对象
client = CosS3Client(config)

# 创建桶
def create_bucket(bucket: str = BUCKET):
  return client.create_bucket(
    # 桶的名称
    Bucket=bucket
  )

# 判断文件是否存在
def check_file_exists(key: str, bucket: str = BUCKET):
  response = client.head_object(
    # 桶的名称
    Bucket=bucket,
    # 文件的路径
    Key=key
  )
  return response['ResponseMetadata']['HTTPStatusCode'] == 200

# 上传文件
def cos_upload_file(file_path: str, key: str, bucket: str = BUCKET):
    file_path, file_name = parsing_path_file(file_path, key)

    client.upload_file(
        # 本地文件路径
        LocalFilePath=file_path,
        # 上传到桶
        Bucket=bucket,
        # 上传到桶的文件名
        Key=file_name
    )
    # 返回访问连接
    url = f'{BASEURL}{file_name}'

    delete_file(file_path)

    return url


def parsing_path_file(url: str, key: str):
    temp_dir = os.path.join(os.getcwd(), f'{KB_ROOT_PATH}')
    # Create the save directory if it doesn't exist
    os.makedirs(temp_dir, exist_ok=True)

    # Extract the file name from the URL
    parsed_url = urlparse(url)
    file_name = os.path.basename(parsed_url.path)
    # 拿到文件后缀
    file_ext = file_name.split('.')[-1]
    file_name = f'{key}.{file_ext}'

    # 这里需要判断是不是在线 url,如果是的话再下载，如果不是的话拼接 file_path 直接返回
    if 'http' not in url:
        return url, file_name
    # Download the file
    response = requests.get(url)
    file_path = os.path.join(temp_dir, file_name)

    # Save the file to the specified directory
    with open(file_path, 'wb') as file:
        file.write(response.content)

    return file_path, file_name


async def delete_file(file_path: str):
    # Delete the file if it exists
    if os.path.exists(file_path):
        os.remove(file_path)
