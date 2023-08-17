import json
from operator import index
import time
import pandas as pd
from datetime import datetime, timedelta
import os
import math
import pytz
from atonix.auth_helper import handle_atx_request


class ProcessData:
    def __init__(self, base_url: str, user_key: str, key, server_id: str = None):
        self.base_url = base_url
        self.user_key = user_key
        self.private_key = key
        self.server_id = server_id

    def get_servers(self):
        """
        a list of servers that the account has access to
        list includes serverGUID, serverName, assetGUID

        Returns
        -------
        a list of server information
        e.x. [[ServerGUID, ServerName, AssetGUID]]
        """

        server_list = []

        resource = '/v1/processdata/servers'
        http_method = "get"  # get, post, put, patch, or delete
        skip = 0
        request_body = None
        headers = None

        while True:
            query_params = {'skip': skip,
                            'take': 50}
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
                server_list.extend(response_json["Results"])
            else:
                raise Exception('Request Unsuccessful')

            if response_json["Count"] >= 50:
                skip += response_json["Count"]
            else:
                break
        print(f'there were {len(server_list)} servers returned')

        return server_list


    def get_tags_list(self, server_id: str, changedAfter: datetime = datetime(2000, 1, 1, 0, 0, 0)):
        """
        a list of tags on a specific data server

        Returns
        -------
        a list of tags for a server
        e.x. [[ID, Name, AssetId]]
        """

        tag_list = []

        resource = f'/v1/processdata/servers/{server_id}/tags'
        http_method = "get"  # get, post, put, patch, or delete
        skip = 0
        request_body = None
        headers = None

        while True:
            query_params = {'skip': skip,
                            'take': 50,
                            'changedAfter': changedAfter}
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
                tag_list.extend(response_json["Results"])
            else:
                raise Exception('Request Unsuccessful')

            if response_json["Count"] >= 50:
                skip += response_json["Count"]
            else:
                break
        print(f'there were {len(tag_list)} tags returned')

        return tag_list


    def get_tag_details(self, tag_id: str):
        """
        Get the definition for a tag.

        :return:
        a dict containing keys...
        {'Description':, 'EngUnit':, 'Name':, 'Qualifier':, 'Source':, 'CreateDate':, 'ChangeDate':}
        """

        resource = f'/v1/processdata/tags/{tag_id}'
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

        if response.status_code == 200 and response_json["StatusCode"] == 200:
            tag_info = response_json['Results'][0]
            return tag_info
        else:
            raise Exception('Request Unsuccessful')

    def PDImport(self
                 , server_id: str
                 , data_source: str
                 , data_timezone: str = None
                 , tag_list: pd.DataFrame = None
                 , archive:str='both'
                 ):
        """
        A routine to push process data to the AtonixOI data servers
        takes 1min data as source and will publish to both the 1min and 60min archives

        :param server_id: server guid
        :param data_source: either a Excel file (.xlsx .xlsm .xlsb .xls) or csv file
            first row should be headers. with each tag name as a header
            first column should be timestamps. if timestamps are not US/Central then use the data_timezone argument
        :return: none
        """



        if tag_list is None:
            # Get all the tag info for the server so we can look up GUIDs for tag names
            skip = 0
            tags = self.get_tags_list(server_id)
            df_tags = pd.DataFrame(tags)
            df_tags.set_index('Name', inplace=True)
        else:
            df_tags = tag_list
            if 'Name' in list(df_tags.columns):
                df_tags.set_index('Name', inplace=True)

        # Read the values to be written from local spreadsheet

        excel_extensions = ['.xlsx', '.xls', '.xlsm', '.xlsb']

        if os.path.splitext(data_source)[-1] in excel_extensions:
            df_data_1min = pd.read_excel(data_source, parse_dates=True, index_col=0, engine='openpyxl')
        elif '.csv' in data_source:
            df_data_1min = pd.read_csv(data_source, parse_dates=True, index_col=0)
        elif '.pkl' in data_source:
            df_data_1min = pd.read_pickle(data_source)

        if df_data_1min.index.tzinfo == None:
            df_data_1min.index = df_data_1min.index.tz_localize(data_timezone, ambiguous='NaT', nonexistent='NaT')
            df_data_1min.index = df_data_1min.index.tz_convert('UTC')
            df_data_1min.dropna(inplace=True)
            df_data_1min.sort_index(inplace=True)
        else:
            df_data_1min.index = df_data_1min.index.tz_convert('UTC')

        # Create a DataFrame of 60min average data
        df_status_mask = df_data_1min != -9999
        df_status_1min = df_status_mask.replace(False, 255).replace(True, 0)
        df_data_60min = df_data_1min.resample('1h').mean()
        df_status_60min = (df_status_1min.resample('1h').mean() == 0).replace(False, 255).replace(True, 0)

        if archive == 'both':
            self.dataframe_to_atonix(server_id, df_data_1min, df_status_1min, df_tags, '1min')
            self.dataframe_to_atonix(server_id, df_data_60min, df_status_60min, df_tags, '60min')
        elif archive == '1min':
            self.dataframe_to_atonix(server_id, df_data_1min, df_status_1min, df_tags, '1min')
        elif archive == '60min':
            self.dataframe_to_atonix(server_id, df_data_60min, df_status_60min, df_tags, '60min')


    def dataframe_to_atonix(self
                            , server_id: str
                            , df_data: pd.DataFrame
                            , df_status: pd.DataFrame
                            , df_tags: pd.DataFrame
                            , archive: str):
        """
        The dataframe_to_atonix function structures data in the TagData format and
            sends it to AtonixOI. It can be used for 1min or 60min data.
        """

        # Set payload variables to be used later
        payload_limit = 30000
        records_per_payload = int(payload_limit / len(df_data.columns))
        num_payloads = math.ceil(len(df_data.index) / records_per_payload)

        # Build a TagData dict within the payload limit by gathering data for all tags and a subset of columns
        for i in range(num_payloads):
            tag_data_list = []
            start_index = i * records_per_payload
            stop_index = min((i + 1) * records_per_payload - 1, len(df_data.index) - 1)
            print(
                f'Packaging data for all tags for the {archive} archive from {df_data.index[start_index]} '
                f'to {df_data.index[stop_index]}')
            # Loop through one tag at a time
            for column in df_data.columns:
                try:
                    tag_guid = df_tags.loc[column, 'Id']
                except:
                    print(f'No AtonixOI tag exists with name: {column}')
                    df_data = df_data.drop(columns=[column])
                    df_status = df_status.drop(columns=[column])
                    print(f'{column} has been dropped from data and status')
                    continue

                tag_data = {'TagId': tag_guid, 'Data': {'Statuses': [], 'Timestamps': [], 'Values': []}}
                # Loop through a slice of the DataFrame to stay under the payload limit
                for timestamp, value in df_data.iloc[start_index:stop_index+1][column].items():
                    tag_data['Data']['Timestamps'].append(timestamp.isoformat())
                    tag_data['Data']['Values'].append(value)
                    tag_data['Data']['Statuses'].append(int(df_status.loc[timestamp, column]))
                tag_data_list.append(tag_data)

            # Build the API call and send it
            resource = f'/v1/processdata/write'
            http_method = 'post'  # get, post, put, patch, or delete
            query_params = None
            request_body = {'Archive': archive, 'ServerId': server_id, 'TagData': tag_data_list}
            headers = None
            response = handle_atx_request(self.base_url,
                                          self.user_key,
                                          self.private_key,
                                          resource,
                                          http_method,
                                          query_params,
                                          request_body,
                                          headers)
            response_json = json.loads(response.content)


    def get_archives(self, server_id: str):
        """
        a list of archives on a specific data server

        Returns
        -------
        a list of archives for a server
        e.x. [{'Name': '1min','Interval': 60},{'Name':'60min','Interval':3600}]
        """

        archive_list = []

        resource = f'/v1/processdata/servers/{server_id}/archives'
        http_method = "get"  # get, post, put, patch, or delete
        skip = 0
        request_body = None
        headers = None

        while True:
            query_params = {'skip': skip,
                            'take': 50}
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
                archive_list.extend(response_json["Results"])
            else:
                raise Exception('Request Unsuccessful')

            if response_json["Count"] >= 50:
                skip += response_json["Count"]
            else:
                break
        print(f'{archive_list} are the available archives')

        return archive_list


    def get_data_for_range(self,
                           server_id: str,
                           start_time: datetime,
                           end_time: datetime,
                           tag_ids: list,
                           archive: str,
                           time_zone: str):
        """
        Get timeseries data for a set of tags in a given time window.
        Call is limited to a response of 250k data points.

        :param server_id as str:
        :param start_time as datetime tz naive:
        :param end_time as datetime tz naive:
        :param tag_ids as list:
        :param archive as str '1min', '60min', or 'both':
        :param time_zone as str:
        :returns dataframe with tz='US/Central':
        """
        # assume data is given as timezone naive
        # apply given time and convert to UTC
        start_time = start_time.astimezone(pytz.timezone(time_zone))
        start_time = start_time.astimezone(pytz.UTC)
        end_time = end_time.astimezone(pytz.timezone(time_zone))
        end_time = end_time.astimezone(pytz.UTC)

        if start_time >= end_time:
            raise Exception('End time must be greater than the start time')
        response_limit = 250000

        # validate that specified archive exists
        avail_archives = pd.DataFrame(self.get_archives(server_id=server_id))
        if archive in avail_archives['Name'].values:
            # get the distance between the timestamps in seconds
            interval = avail_archives['Interval'].loc[avail_archives['Name'] == archive].item()
        else:
            raise Exception('Specified archive not available')

        # determine number of expected data points
        num_tags = len(tag_ids)
        num_timestamps = (end_time - start_time).total_seconds() / interval

        if num_tags >= response_limit:
            raise Exception('Too many tags')

        records_per_payload = int(response_limit / num_tags) # floor division
        num_calls = math.ceil(num_timestamps / records_per_payload)

        data = pd.DataFrame()
        for i in range(num_calls):
            req_start_time = start_time + timedelta(seconds=i * records_per_payload * interval)
            req_end_time = start_time + timedelta(seconds=(i + 1) * records_per_payload * interval)
            if req_end_time > end_time:
                req_end_time = end_time

            resource = f'/v1/processdata/query'
            http_method = "post"  # get, post, put, patch, or delete
            query_params = None
            request_body = {'Archive': archive,
                            'End': req_end_time.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                            'ServerId': server_id,
                            'Start': req_start_time.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                            'TagIds': tag_ids}
            headers = None
            response = handle_atx_request(self.base_url,
                                          self.user_key,
                                          self.private_key,
                                          resource,
                                          http_method,
                                          query_params,
                                          request_body,
                                          headers)

            response_json = json.loads(response.content)

            if response.status_code == 200 and response_json["StatusCode"] == 200:
                for tag in range(response_json['Count']):
                    tag_data = pd.DataFrame(response_json['Results'][tag]['Data'])
                    tag_data['tag_id'] = response_json['Results'][tag]['TagId']
                    data = pd.concat([data, tag_data])
            else:
                raise Exception('Request Unsuccessful')

            time.sleep(0.20)

        return data
