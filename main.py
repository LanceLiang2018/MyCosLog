# -*- coding: utf8 -*-
# SCF configures the COS trigger, obtains the file uploading information from COS, and downloads it to the local temporary disk 'tmp' of SCF.
# SCF配置COS触发，从COS获取文件上传信息，并下载到SCF的本地临时磁盘tmp
import os
import time
from qcloud_cos_v5 import CosConfig
from qcloud_cos_v5 import CosS3Client
from qcloud_cos_v5 import CosServiceError
from qcloud_cos_v5 import CosClientError
import sys
import logging

import pymongo

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

appid = 1254016670  # Please replace with your APPID. 请替换为您的 APPID
secret_id = os.environ.get('app_sid', '')  # Please replace with your SecretId. 请替换为您的 SecretId
secret_key = os.environ.get('app_skey', '')  # Please replace with your SecretKey. 请替换为您的 SecretKey
region = os.environ.get('app_region', '')  # Please replace with the region where COS bucket located. 请替换为您bucket 所在的地域
# token = ''
# database_str = os.getenv('app_database_str', '')
database_str = "mongodb://LanceLiang:1352040930database@lanceliang-lktmq.azure.mongodb.net"

# config = CosConfig(Secret_id=secret_id, Secret_key=secret_key, Region=region, Token=token)
config = CosConfig(Secret_id=secret_id, Secret_key=secret_key, Region=region)
client = CosS3Client(config)
logger = logging.getLogger()
db = pymongo.MongoClient(database_str)
# db = pymongo.MongoClient('lanceliang-lktmq.azure.mongodb.net')


def main_handler(event, context):
    logger.info("start main handler")
    for record in event['Records']:
        try:
            bucket = record['cos']['cosBucket']['name'] + '-' + str(appid)
            key = record['cos']['cosObject']['key']
            key = key.replace('/' + str(appid) + '/' + record['cos']['cosBucket']['name'] + '/', '', 1)
            logger.info("Key is " + key)

            # # download object from cos
            # logger.info("Get from [%s] to download file [%s]" % (bucket, key))
            # download_path = '/tmp/{}'.format(key)
            # try:
            #     response = client.get_object(Bucket=bucket, Key=key, )
            #     response['Body'].get_stream_to_file(download_path)
            # except CosServiceError as e:
            #     print(e.get_error_code())
            #     print(e.get_error_msg())
            #     print(e.get_resource_location())
            #     return "Fail"
            # logger.info("Download file [%s] Success" % key)

            col = db.cos_logs[bucket]
            col.insert_one({
                'key': key,
                'bucket': bucket,
                'time': time.asctime(time.localtime(time.time()))
            })

        except Exception as e:
            print(e)
            print('Error getting object {} from bucket {}. '.format(key, bucket))
            raise e
            return "Fail"

    return "Success"
