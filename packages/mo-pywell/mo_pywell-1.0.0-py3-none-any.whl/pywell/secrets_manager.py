from botocore.exceptions import ClientError
import base64
import boto3
import json
import logging

def get_secret(secret_name, region_name='us-west-1'):
    logging.getLogger().setLevel('INFO')
    # Create a Secrets Manager client
    session = boto3.session.Session(region_name=region_name)
    client = session.client(
        service_name='secretsmanager'
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )

    # Decrypts secret using the associated KMS CMK. Depending on whether
    # the secret is a string or binary, one of these fields will be
    # populated.
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = base64.b64decode(
            get_secret_value_response['SecretBinary']
        )

    return json.loads(secret)
