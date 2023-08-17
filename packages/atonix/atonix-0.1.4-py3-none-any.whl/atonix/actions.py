import json
import time
from datetime import datetime

import pytz

from atonix.auth_helper import handle_atx_request


class Actions:
    def __init__(self, base_url: str, user_key: str, key):
        self.base_url = base_url
        self.user_key = user_key
        self.private_key = key
        self.actions = []

    def get_model_actions(self, model_id: str, changedAfter: datetime = datetime(2000, 1, 1, 0, 0, 0)):
        """
        a list of actions on a specific model

        Returns
        -------
        a list of tags for a server
        e.x. [[ID, Name, AssetId]]
        """

        action_list = []

        resource = f'/v1/models/{model_id}/actions'
        http_method = "get"  # get, post, put, patch, or delete
        skip = 0
        request_body = None
        headers = None

        while True:
            query_params = {'skip': skip,
                            'take': 500,
                            'changedAfter': changedAfter}
            if skip != 0:
                time.sleep(0.21)
            response = handle_atx_request(
                self.base_url,
                self.api_key,
                self.private_key,
                resource,
                http_method,
                query_params,
                request_body,
                headers)

            response_json = json.loads(response.content)

            if response.status_code == 200 and response_json["StatusCode"] == 200:
                # Results element will be a list of dictionaries
                action_list.extend(response_json["Results"])
            else:
                raise Exception('Request Unsuccessful')

            if response_json["Count"] >= 50:
                skip += response_json["Count"]
            else:
                break

        return action_list

    def get_asset_actions(self,
                          asset_id: str,
                          changedAfter: datetime = datetime(2000, 1, 1, 0, 0, 0, tzinfo=pytz.UTC),
                          changedBefore: datetime = datetime.utcnow(),
                          includeDescendants: bool = False,
                          includeInactive: bool = False
                          ):
        """
        a list of actions on a specific model

        Returns
        -------
        a list of tags for a server
        e.x. [[ID, Name, AssetId]]
        """

        action_list = []

        changedBeforeDate = changedBefore.astimezone(pytz.UTC)
        changedAfterDate = changedAfter.astimezone(pytz.UTC)

        resource = f'/v1/models/actions'
        http_method = "get"  # get, post, put, patch, or delete
        skip = 0
        request_body = None
        headers = None

        while True:
            query_params = {'assetId': asset_id,
                            'changedAfter': changedAfter,
                            'changedBefore': changedBefore,
                            'includeDescendants': includeDescendants,
                            'includeInactive': includeInactive,
                            'skip': skip,
                            'take': 500,
                            }
            if skip != 0:
                time.sleep(0.21)
            response = handle_atx_request(
                self.base_url,
                self.api_key,
                self.private_key,
                resource,
                http_method,
                query_params,
                request_body,
                headers)

            response_json = json.loads(response.content)

            if response.status_code == 200 and response_json["StatusCode"] == 200:
                # Results element will be a list of dictionaries
                action_list.extend(response_json["Results"])
            else:
                raise Exception('Request Unsuccessful')

            if response_json["Count"] >= 50:
                skip += response_json["Count"]
            else:
                break

        return action_list
