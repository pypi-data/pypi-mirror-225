import json
import sys
import base64
from .anzo_jupyter_util import import_optional_dependency

# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/

class SecretsManager:
    @staticmethod
    def parse_login_info(secret_name, region_name):
        try:
            print(
                f'Attempting to read from secret manager: {secret_name}, {region_name} ')
            res = SecretsManager.get_secret(
                secret_name, region_name)
            secret_values = json.loads(res)

            login = secret_values["username"], secret_values["password"]
        except:
            raise ValueError(
                f'Error: Unable to access secrets manager or not provided\n  {secret_name}, {region_name}')
        return login

    @staticmethod
    def get_secret(secret_name, region_name):
        # Create a Secrets Manager client
        botocore = import_optional_dependency('boto3')
        from botocore.exceptions import ClientError
        boto3 = import_optional_dependency('boto3')
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
                # Deal with the exception here, and/or rethrow at your discretion.
                print(f'DecryptionFailureException:{e}')
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                # An error occurred on the server side.
                # Deal with the exception here, and/or rethrow at your discretion.
                print(f'InternalServiceErrorException:{e}')
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                # You provided an invalid value for a parameter.
                # Deal with the exception here, and/or rethrow at your discretion.
                print(f'InvalidParameterException:{e}')
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                # You provided a parameter value that is not valid for the current state of the resource.
                # Deal with the exception here, and/or rethrow at your discretion.
                print(f'InvalidRequestException:{e}')
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                # We can't find the resource that you asked for.
                # Deal with the exception here, and/or rethrow at your discretion.
                print(f'ResourceNotFoundException:{e}')
                raise e
            else:
                # Please see https://docs.aws.amazon.com/secretsmanager/latest/apireference/CommonErrors.html for all the other types of errors not handled above
                raise e
        else:
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if 'SecretString' in get_secret_value_response:
                print("Secret Manager Response Recieved!")
                return get_secret_value_response['SecretString']
            else:
                print("Secret Manager Response Received!")
                return base64.b64decode(get_secret_value_response['SecretBinary'])
