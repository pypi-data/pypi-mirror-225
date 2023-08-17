"""
a module to provide an interface with the AtonixOI APIs
written by: Kolton Stimpert
date: 10/15/2021
"""

from cryptography.hazmat.primitives import serialization
import atonix.assets as assets
import atonix.models as models
import atonix.processdata as processdata
import atonix.actions as actions
import atonix.issues as issues


class Api:
    def __init__(self, user_key_path: str, api_key_path: str, api_key_pw):
        self.base_url = "https://api.oi.atonix.com"

        with open(user_key_path, 'r') as api_key_file:
            api_key = api_key_file.read()
        self.api_key = api_key.replace("-", "").lower()

        # Retrieve the private key from the specified file path in the required format
        if api_key_pw is None:
            with open(api_key_path, "rb") as private_key_file:
                self.private_key = serialization.load_pem_private_key(private_key_file.read(), password=None)
        else:
            with open(api_key_path, "rb") as private_key_file:
                self.private_key = serialization.load_pem_private_key(private_key_file.read(),
                                                                      password=str.encode(api_key_pw, 'utf-8'))

        self.Assets = assets.Assets(base_url=self.base_url, user_key=self.api_key, key=self.private_key)
        self.Models = models.Models(base_url=self.base_url, user_key=self.api_key, key=self.private_key)
        self.Actions = actions.Actions(base_url=self.base_url, user_key=self.api_key, key=self.private_key)
        self.ProcessData = processdata.ProcessData(base_url=self.base_url, user_key=self.api_key, key=self.private_key)
        self.Issues = issues.Issues(base_url=self.base_url, user_key=self.api_key, key=self.private_key)
