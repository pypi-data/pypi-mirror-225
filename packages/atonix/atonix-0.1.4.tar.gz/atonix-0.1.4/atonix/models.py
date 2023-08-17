import json
import time
from datetime import datetime

import pytz

from atonix.auth_helper import handle_atx_request


class Models:
    def __init__(self, base_url: str, user_key: str, key):
        self.base_url = base_url
        self.user_key = user_key
        self.private_key = key

    def get_models(self, asset_id: str,
                   descendants: bool = True,
                   changedAfterDate: datetime = datetime(2000, 1, 1, 0, 0, 0, tzinfo=pytz.UTC),
                   changedBeforeDate: datetime = datetime.utcnow()
                   ):
        """
        get models associated to an asset.
        default to include descendants

        Parameters
        ----------
        asset_id
        descendants
        changedAfterDate

        Returns
        -------
        list of models that is a child of the given asset
        """
        model_list = []
        start_time = time.time()

        changedBeforeDate = changedBeforeDate.astimezone(pytz.UTC)
        changedAfterDate = changedAfterDate.astimezone(pytz.UTC)

        resource = '/v1/models'
        http_method = "get"  # get, post, put, patch, or delete
        skip = 0
        request_body = None
        headers = None

        while True:
            query_params = {'skip': skip,
                            'take': 500,
                            'includeDescendants': descendants,
                            'assetId': asset_id,
                            'changedAfter': changedAfterDate,
                            'changedBefore': changedBeforeDate}
            if skip != 0:
                time.sleep(0.20)
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
                model_list.extend(response_json["Results"])
            else:
                raise Exception(f'Request Unsuccessful. Status code: {response.status_code}')

            if response_json["Count"] >= 50:
                skip += response_json["Count"]
            else:
                break
        return model_list

    def get_model_config(self, model_id: str):
        """
        information about the config
        i.e. inputs, anomaly settings, alert settings, training information

        Parameters
        ----------
        model_id

        Returns
        -------
        list of model info
        """
        resource = f'/v1/models/{model_id}/config'
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
            headers
        )
        response_json = json.loads(response.content)

        if response.status_code == 200 and response_json["StatusCode"] == 200:
            # Results element will be a list of dictionaries
            return response_json["Results"]
        else:
            raise Exception(f'Request Unsuccessful. Status code: {response.status_code}')

    def get_model_state(self, model_id: str):
        """
        get the current state of a model. i.e. active state, alert state, any flags MM or other that may be set

        Parameters
        ----------
        model_id

        Returns
        -------

        """
        resource = f'/v1/models/{model_id}/state'
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
            headers
        )
        response_json = json.loads(response.content)

        return response_json

    def get_model_state_by_asset(self,
                                 asset_id: str,
                                 includeDescendants: bool = False,
                                 includeInactive: bool = False,
                                 ):
        """
        get the current state of a model. i.e. active state, alert state, any flags MM or other that may be set

        Parameters
        ----------
        asset_id

        Returns
        -------

        """

        alerts_list = []

        skip = 0

        resource = f'/v1/models/state'
        http_method = "get"  # get, post, put, patch, or delete
        request_body = None
        headers = None
        while True:
            query_params = {'assetId': asset_id,
                            'includeDescendants': includeDescendants,
                            'includeInactive': includeInactive,
                            'skip': skip,
                            'take': 500}
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
                headers
            )
            response_json = json.loads(response.content)

            if response.status_code == 200 and response_json["StatusCode"] == 200:
                # Results element will be a list of dictionaries
                alerts_list.extend(response_json["Results"])
            else:
                raise Exception('Request Unsuccessful')

            if response_json["Count"] >= 50:
                skip += response_json["Count"]
            else:
                break

        return alerts_list
