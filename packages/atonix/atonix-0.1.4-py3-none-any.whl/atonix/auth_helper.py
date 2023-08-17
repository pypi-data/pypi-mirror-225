"""This sample code is provided "As Is" and any warranties, express or implied,
are disclaimed. It is meant for your education and it is your responsibility to
test any code according to your (company) standard. In no event shall Atonix be
held liable or accountable for this sample code, nor can support be expected
for this sample code.

Last Modified: Kolton Stimpert
Date: 4/20/21
Version: 0.1

"""

from base64 import b64encode
import json
import time
from typing import Any

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import logging


def represent_request(api_key: str,
                      timestamp_milliseconds: int,
                      resource: str,
                      http_method: str,
                      query_params: dict = None,
                      request_body: Any = None) -> str:
    representation = '{}\n{}\n{}\n{}'.format(
        api_key,
        timestamp_milliseconds,
        resource.lower(),
        http_method.lower()
    )

    if query_params is not None:
        query_representations = []
        for key in sorted(query_params):
            if isinstance(query_params[key], list):
                query_value = ''.join(
                    sorted(['{}'.format(v) for v in query_params[key]])
                )
            else:
                query_value = '{}'.format(query_params[key])
            query_representations.append(f'{key}:{query_value}')

        if len(query_representations) > 0:
            representation += '\n{}'.format('\n'.join(query_representations))

    if request_body is not None:
        if isinstance(request_body, dict):
            request_body_dict = request_body
        else:
            request_body_dict = json.loads(request_body)

        representation += '\n{}'.format(
            json.dumps(request_body_dict, separators=(',', ':'))
        )
    return representation


def get_signature(representation: str, private_key: rsa.RSAPrivateKey) -> str:
    signature = b64encode(
        private_key.sign(
            representation.encode('ascii'),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
    ).decode('ascii')
    return signature


# Description: Needed to generate the x-atx-auth header for RSAMac Authentication
def atonix_auth_header(api_key: str,
                       private_key: rsa.RSAPrivateKey,
                       resource: str,
                       http_method: str,
                       query_params: dict = None,
                       request_body: Any = None) -> str:
    timestamp_milliseconds = int((round(time.time() * 1000)))
    representation = represent_request(
        api_key,
        timestamp_milliseconds,
        resource,
        http_method,
        query_params,
        request_body
    )
    signature = get_signature(representation, private_key)
    return '{}:{}:{}'.format(api_key, timestamp_milliseconds, signature)


def retry_session():
    s = requests.session()
    retries = Retry(total=3, backoff_factor=10, status_forcelist=[500, 502, 503, 504])
    s.mount('http://', HTTPAdapter(max_retries=retries))
    s.mount('https://', HTTPAdapter(max_retries=retries))
    return s


def handle_atx_request(base_url: str,
                       api_key: str,
                       private_key: rsa.RSAPrivateKey,
                       resource: str,
                       http_method: str,
                       query_params: dict = None,
                       request_body: Any = None,
                       headers: dict = None):
    request_url = f'{base_url}{resource}'

    header = atonix_auth_header(api_key,
                                private_key,
                                resource,
                                http_method=http_method,
                                query_params=query_params,
                                request_body=request_body)
    header_dict = {
        'x-atx-auth': header,
        'x-api-key': api_key
    }

    if headers is not None:
        for k, v in headers.items():
            header_dict[k] = v

    s = retry_session()
    if http_method.lower() == "get":
        response = s.get(request_url, headers=header_dict, params=query_params, timeout=30)
    elif http_method.lower() == "put":
        response = requests.put(request_url, headers=header_dict, params=query_params, json=request_body, timeout=30)
    elif http_method.lower() == "post":
        response = requests.post(request_url, headers=header_dict, params=query_params, json=request_body, timeout=30)
    elif http_method.lower() == "delete":
        response = requests.delete(request_url, headers=header_dict, params=query_params, timeout=30)
    elif http_method.lower() == "patch":
        response = requests.patch(request_url, headers=header_dict, params=query_params, json=request_body, timeout=30)
    else:
        raise Exception('Invalid HTTP method')

    if response.status_code == 429:
        print('Got rate limited')
        time.sleep(0.5)
        return handle_atx_request(base_url,
                                  api_key,
                                  private_key,
                                  resource,
                                  http_method,
                                  query_params,
                                  request_body,
                                  headers)
    else:
        return response
