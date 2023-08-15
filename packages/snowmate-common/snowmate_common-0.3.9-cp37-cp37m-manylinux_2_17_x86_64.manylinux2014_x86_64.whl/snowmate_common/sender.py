import sys
from typing import Dict, Tuple
from uuid import uuid4

from snowmate_common.messages_data.messages import MainMessage, S3Message
from snowmate_common.utils.compressing import compress_data

MAX_DATA_SIZE = 250 * 1024
MESSAGE_GROUP_ID = "1"
AUTHORIZATION_HEADER = "Authorization"


class SQSFields:
    MESSAGE_BODY = "MessageBody"
    MESSAGE_GROUP_ID = "MessageGroupId"
    MESSAGE_DEDUPLICATION_ID = "MessageDeduplicationId"


class S3Fields:
    KEY = "key"
    ACCESS_TOKEN = "accessToken"
    DATA = "data"
    S3_DATA = "s3_data"


class Destinations:
    BASELINE = "baseline"
    REGRESSIONS = "regressions"


class Routes:
    LARGE = "large"
    ENQUEUE = "enqueue"


class RequestMethods:
    POST = "POST"
    PUT = "PUT"


def create_s3_message(main_message: MainMessage) -> Tuple[str, S3Message]:
    key = f"{str(uuid4())}.json"
    s3_message = S3Message(file_key=key)
    s3_message = MainMessage(
        access_token=main_message.access_token,
        s3_message=s3_message
    )
    return key, s3_message


def create_message(
    base_url: str, destination: str, message: MainMessage
) -> Tuple[str, str, Dict, Dict]:
    compressed_message = compress_data(bytes(message))
    if sys.getsizeof(compressed_message) >= MAX_DATA_SIZE:
        url = f"{base_url}/{destination}/{Routes.LARGE}"
        method = RequestMethods.PUT
        s3_file_name, s3_message = create_s3_message(message)
        compressed_s3_message = compress_data(bytes(s3_message))
        payload = {
            S3Fields.KEY: s3_file_name,
            S3Fields.DATA: {
                S3Fields.ACCESS_TOKEN: message.access_token,
                S3Fields.DATA: compressed_message,
                S3Fields.S3_DATA: compressed_s3_message
            }
        }
    else:
        url = f"{base_url}/{destination}/{Routes.ENQUEUE}"
        method = RequestMethods.POST
        payload = {
            SQSFields.MESSAGE_BODY: compressed_message,
            SQSFields.MESSAGE_GROUP_ID: MESSAGE_GROUP_ID,
            SQSFields.MESSAGE_DEDUPLICATION_ID: str(uuid4()),
        }
    headers = {AUTHORIZATION_HEADER: f"Bearer {message.access_token}"}
    return method, url, headers, payload
