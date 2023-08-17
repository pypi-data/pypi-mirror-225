import json
import datetime
import time
from atonix.auth_helper import handle_atx_request


class Issues:
    def __init__(self, base_url: str, user_key: str, key):
        self.base_url = base_url
        self.user_key = user_key
        self.private_key = key

    def get(self,
            assetId: str,
            changedAfter: datetime = None,
            changedBefore: datetime = None,
            includeDescendants: bool = True,
            status: str = None
            ):
        """
        Get issues for a given asset
        defaults to include issues on children assets
        optionally can filter for date ranges or specific status values

        :param assetId:
        :param changedAfter:
        :param changedBefore:
        :param includeDescendants:
        :param status:
        :return:
        """
        issue_list = []

        resource = '/v1/issues'
        http_method = "get"  # get, post, put, patch, or delete
        skip = 0
        request_body = None
        headers = None

        while True:
            query_params = {'assetId': assetId,
                            'skip': skip,
                            'take': 500,
                            'includeDescendants': includeDescendants,
                            'changedAfter': changedAfter,
                            'changedBefore': changedBefore,
                            'status': status}
            query_params = {k: v for k, v in query_params.items() if v is not None}
            if skip != 0:
                time.sleep(0.21)
            response = handle_atx_request(
                self.base_url,
                self.user_key,
                self.private_key,
                resource,
                http_method,
                query_params,
                request_body,
                headers)

            response_json = json.loads(response.content)

            if response.status_code == 200 and response_json["StatusCode"] == 200:
                # Results element will be a list of dictionaries
                issue_list.extend(response_json["Results"])
            else:
                raise Exception(f'Request Unsuccessful. Requests status code: {response.status_code} \n'
                                f'Response status code: {response_json["StatusCode"]}')

            if response_json["Count"] >= 50:
                skip += response_json["Count"]
            else:
                break
        return issue_list

    def get_issue_details(self, issueId: str):
        """
        Get details for a specific issue

        :param issueId:
        :return:
        """

        resource = f'/v1/issues/{issueId}'
        http_method = "get"  # get, post, put, patch, or delete
        request_body = None
        headers = None
        query_params = None

        response = handle_atx_request(
            self.base_url,
            self.user_key,
            self.private_key,
            resource,
            http_method,
            query_params,
            request_body,
            headers)

        response_json = json.loads(response.content)

        if response.status_code == 200:
            # Results element will be a list of dictionaries
            return response_json["Results"]
        else:
            raise Exception(f'Request Unsuccessful. Status code: {response.status_code}')

    def get_discussion(self, issueId: str):
        discussion_list = []

        resource = f'/v1/issues/{issueId}/discussionentries'
        http_method = "get"  # get, post, put, patch, or delete
        skip = 0
        request_body = None
        headers = None

        while True:
            query_params = {'skip': skip,
                            'take': 500
                            }
            if skip != 0:
                time.sleep(0.21)
            response = handle_atx_request(
                self.base_url,
                self.user_key,
                self.private_key,
                resource,
                http_method,
                query_params,
                request_body,
                headers)

            response_json = json.loads(response.content)

            if response.status_code == 200 and response_json["StatusCode"] == 200:
                # Results element will be a list of dictionaries
                discussion_list.extend(response_json["Results"])
            else:
                raise Exception(f'Request Unsuccessful. Requests status code: {response.status_code} \n'
                                f'Response status code: {response_json["StatusCode"]}')

            if response_json["Count"] >= 50:
                skip += response_json["Count"]
            else:
                break
        return discussion_list

    def get_keywords(self, issueId: str):
        keyword_list = []

        resource = f'/v1/issues/{issueId}/keywords'
        http_method = "get"  # get, post, put, patch, or delete
        skip = 0
        request_body = None
        headers = None

        while True:
            query_params = {'skip': skip,
                            'take': 500
                            }
            if skip != 0:
                time.sleep(0.21)
            response = handle_atx_request(
                self.base_url,
                self.user_key,
                self.private_key,
                resource,
                http_method,
                query_params,
                request_body,
                headers)

            response_json = json.loads(response.content)

            if response.status_code == 200 and response_json["StatusCode"] == 200:
                # Results element will be a list of dictionaries
                keyword_list.extend(response_json["Results"])
            else:
                raise Exception(f'Request Unsuccessful. Requests status code: {response.status_code} \n'
                                f'Response status code: {response_json["StatusCode"]}')

            if response_json["Count"] >= 50:
                skip += response_json["Count"]
            else:
                break
        return keyword_list
