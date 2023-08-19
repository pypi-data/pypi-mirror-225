from sys import platform
import requests
import pandas as pd
import os
import json
from urllib.parse import urlparse
from typing import List, Optional
import asyncio

# Async
from utilities.async_utils import async_wrap

class Vnitro:
    
    def __init__(self):
        self.serverUrl: str = None # from authenticate
        self.nitroUserName: str = None # from authenticate
        self.nitroPassword: str = None # from authenticate
        self.accessToken: str = None # from authenticate
        self.refreshToken: str = None # from authenticate
        self.appServerUrl: str = None # from authenticate
        self.tenantName: str = None # from authenticate
        self.instances: List[Optional(dict)] = None # from authenticate
        self.tenantRoles: List[Optional(dict)] = None # from authenticate
        self.instanceRoles: List[Optional(dict)] = None # from authenticate
        self.instancePermissions: dict = None # from authenticate
        self.cdwAPItoken: str = None # from get_cdw_api_token
        self.tenant: dict = None # from get_tenant
        self.configuration: dict = None # from get_configuration
        self.users: List[Optional(dict)] = None # from get_users
        self.applicationRoles: List[Optional(dict)] = None # from get_application_roles
        self.rules: dict = {} # from get_rules
        self.groups: dict = {} # from get_groups
        self.jobs: dict = {} # from get_jobs
        self.connectors: dict = {} # from get_connectors
        self.clusterDetails: dict = {} # from get_cluster_details
        self.jobResults: dict = {} # from get_results
        self.workingInstance: str = None # Set by any method that requires an instance name, last used instance name is stored here
                                         # Upon authentication, the first instance in the list of instances is set as the working instance
        
        
        
    def _handle_response(self, response):
        """
        A helper method to handle API responses.
        
        Args:
            response (Response): The response object from the requests library.
            
        Returns:
            dict: The response JSON content.
            
        Raises:
            Exception: If the response indicates an error.
        """
        if response.status_code == 200:
            return response.json()
        
        elif response.status_code == 401:
            if 'error' in response.json().keys():
                raise Exception(f"Unauthorized: {response.json()['error']}")
                
            else:
                raise Exception(f"Request failed. Response from server: {response.json()}")
        else:
            raise Exception(f"Request failed. Response from server: {response.json()}")
        
    def authenticate(
        self,
        serverUrl: str = None,
        nitroUserName: str = None,
        nitroPassword: str = None,
        accessToken: str = None
    ):
        """
        Authenticates the user with the Veeva Nitro API. If the accessToken is provided, the username and password are not required.
        The authentication also retrieves the tenant information and sets the attributes of the class to the response JSON.
        It loads the following attributes:
            self.accessToken, self.refreshToken, self.serverUrl, self.appServerUrl, self.tenantName,
            self.instances, self.tenantRoles, self.instanceRoles, self.instancePermissions
        
        Args:
            serverUrl (str): Required. The base URL for the Veeva Nitro API. Example: https://mycompany.veevanitro.com
            nitroUserName (str, optional): The username for authentication. Defaults to None. Must be provided if accessToken is not provided.
            nitroPassword (str, optional): The password for authentication. Defaults to None. Must be provided if accessToken is not provided.
            accessToken (str, optional): The session ID for authentication. Defaults to None. Must be provided if nitroUserName and nitroPassword are not provided.
            
        Raises:
            Exception: If the necessary parameters for authentication are not provided.
            Exception: If the authentication fails.
        """
        self.serverUrl = serverUrl if serverUrl is not None else self.serverUrl
        self.nitroUserName = nitroUserName if nitroUserName is not None else self.nitroUserName
        self.nitroPassword = nitroPassword if nitroPassword is not None else self.nitroPassword
        self.accessToken = accessToken if accessToken is not None else self.accessToken
        
        url = f"{self.serverUrl}/api/v1/auth/login"
        
        # Ensure at least serverUrl and accessToken are provided or serverUrl and nitroUserName and nitroPassword are provided
        if (self.serverUrl is None) or (self.accessToken is None and (self.nitroUserName is None or self.nitroPassword is None)):
            raise Exception("serverUrl and accessToken are required or serverUrl and nitroUserName and nitroPassword are required")
        
        # If authenticating with username and password:
        if self.accessToken is None:
            # Get the session ID
            payload = {
                "username": self.nitroUserName,
                "password": self.nitroPassword
            }

            response = requests.post(url, json=payload)
            
        # If authenticating with session ID
        else:
            # There is not a clear way to authenticate using accessToken, so we will just make a request to the tenant endpoint to test the validity of the session ID
            url = f"{self.serverUrl}/api/v1/admin/tenant"
            payload = {
                "Authorization": self.accessToken
            }

            response = requests.get(url, headers=payload)
            
        response_json = self._handle_response(response)
            

        attributes = [
            'accessToken', 'refreshToken', 'serverUrl', 'appServerUrl', 'tenantName',
            'instances', 'tenantRoles', 'instanceRoles', 'instancePermissions'
        ]

        # Decision was made here to raise an exception if
        # the response does not contain the expected attributes
        # This is to ensure that the attributes of the class are set correctly
        # and that future methods can rely on the attributes being set
        # MPay 2023-08-18
        try:
            # Set the attributes of the class to the response JSON
            for attr in attributes:
                setattr(self, attr, response_json[attr])
        except:
            raise Exception(f"""API response did not contain the expected attributes.
            Expected attributes: {attributes}
            Response JSON: {response_json}
            Please contact the developer or system administrator for assistance.
            Has the API changed due to latest release?""")
        
        # Set working instance
        try:
            self.workingInstance = self.instances[0]['instanceName']
        except:
            self.workingInstance = None
        
        return response_json
    
    
    def get_cdw_api_token(self):
        """
        Retrieves the CDW API token using the authenticated session.
        
        Returns:
            dict: The response JSON containing the CDW API token.
            
        Raises:
            Exception: If the request for the CDW API token fails.
            Exception: If not authenticated.
        """
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/api/v1/users/tokens/issue"
        
        headers = {
            "Authorization": self.accessToken
        }
        
        response = requests.post(url, headers=headers)
        
        respone_json = self._handle_response(response)
        
        if 'content' in respone_json and 'token' in respone_json['content']:
            self.cdwAPItoken = respone_json['content']['token']
        
        return respone_json
            
    def get_tenant(self) -> dict:
        """
        Retrieves tenant information from the Veeva Nitro API.
        
        Returns:
            dict: The response JSON containing tenant details.
            
        Raises:
            Exception: If the request for tenant information fails.
            Exception: If not authenticated.
        """
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/api/v1/admin/tenant"
        headers = {
            "Authorization": self.accessToken,
        }
        
        response = requests.get(url, headers=headers)
        
        response_json = self._handle_response(response)
        
        if 'content' in response_json:
            self.tenant = response_json['content']
        
        return response_json

    def get_configuration(self) -> dict:
        """
        Retrieves cluster configuration from the Veeva Nitro API.
        
        Returns:
            dict: The response JSON containing cluster configuration details.
            
        Raises:
            Exception: If the request for cluster configuration fails.
            Exception: If not authenticated.
        """
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/api/v1/admin/cluster/configuration"
        headers = {
            "Authorization": self.accessToken
        }
        
        response = requests.get(url, headers=headers)
        response_json = self._handle_response(response)
        
        if 'content' in response_json:
            self.configuration = response_json['content']
        
        return response_json
        
    def get_users(self) -> dict:
        """
        Retrieves user information from the Veeva Nitro API.
        
        Returns:
            dict: The response JSON containing user details.
            
        Raises:
            Exception: If the request for user information fails.
            Exception: If not authenticated.
        """
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/api/v1/admin/users"
        headers = {
            "Authorization": self.accessToken
        }
        
        response = requests.get(url, headers=headers)
        
        response_json = self._handle_response(response)
        
        if 'content' in response_json:
            self.users = response_json['content']
        
        return response_json

    # Question: Where can I find the app parameter values?
    def get_application_roles(self, app: str = "APP_SERVER") -> dict:
        """
        Retrieves application roles from the Veeva Nitro API.
        
        Args:
            app (str, optional): The application type. Defaults to "APP_SERVER".
            
        Returns:
            dict: The response JSON containing application roles.
            
        Raises:
            Exception: If the request for application roles fails.
            Exception: If not authenticated.
        """
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/api/v1/admin/users/application-roles?app={app}"
        headers = {
            "Authorization": self.accessToken
        }
        
        response = requests.get(url, headers=headers)
        
        response_json = self._handle_response(response)
        
        if 'content' in response_json:
            self.applicationRoles = response_json['content']
        
        return response_json


    def get_rules(self, Dwinstancename = None) -> dict:
        """
        Retrieves rule information from the Veeva Nitro API.
        
        Returns:
            dict: The response JSON containing rule details.
            
        Raises:
            Exception: If the request for rule information fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        self.workingInstance = Dwinstancename if Dwinstancename is not None else self.workingInstance
        
        if self.workingInstance is None:
            raise Exception("You must provide an instance name or set the working instance before executing this method")
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/mds/api/v1/rules"
        headers = {
            "Authorization": self.accessToken,
            "Dwinstancename": self.workingInstance,
            "Tenantname": self.tenantName
        }
        
        response = requests.get(url, headers=headers)
        response_json = self._handle_response(response)
        
        # Save the response content under the Dwinstancename key
        if 'content' in response_json:
            self.rules[self.workingInstance] = response_json['content']
        
        return response_json

    def get_groups(self, Dwinstancename = None) -> dict:
        """
        Retrieves rule group information from the Veeva Nitro API.
        
        Returns:
            dict: The response JSON containing rule group details.
            
        Raises:
            Exception: If the request for rule group information fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        self.workingInstance = Dwinstancename if Dwinstancename is not None else self.workingInstance
        
        if self.workingInstance is None:
            raise Exception("You must provide an instance name or set the working instance before executing this method")
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/mds/api/v1/rule/groups"
        headers = {
            "Authorization": self.accessToken,
            "Dwinstancename": self.workingInstance,
            "Tenantname": self.tenantName
        }
        
        response = requests.get(url, headers=headers)
        
        response_json = self._handle_response(response)
        
        if 'content' in response_json:
            self.groups[self.workingInstance] = response_json['content']
        
        return response_json

    def get_jobs(self, Dwinstancename = None, view: str = "condensed") -> dict:
        """
        Retrieves job information from the Veeva Nitro API.
        
        Args:
            view (str, optional): The view type for the jobs. Defaults to "condensed".
            
        Returns:
            dict: The response JSON containing job details.
            
        Raises:
            Exception: If the request for job information fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        self.workingInstance = Dwinstancename if Dwinstancename is not None else self.workingInstance
        
        if self.workingInstance is None:
            raise Exception("You must provide an instance name or set the working instance before executing this method")
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/mds/api/v1/jobs?view={view}"
        headers = {
            "Authorization": self.accessToken,
            "Dwinstancename": self.workingInstance,
            "Tenantname": self.tenantName
        }
        
        response = requests.get(url, headers=headers)
        
        response_json = self._handle_response(response)
        
        if 'content' in response_json:
            self.jobs[self.workingInstance] = response_json['content']
        
        return response_json

    def get_connectors(self, Dwinstancename = None, internalOnly: bool = False, ) -> dict:
        """
        Retrieves connector information from the Veeva Nitro API.
        
        Args:
            internalOnly (bool, optional): Filter for internal connectors. Defaults to False.
            
        Returns:
            dict: The response JSON containing connector details.
            
        Raises:
            Exception: If the request for connectors fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        self.workingInstance = Dwinstancename if Dwinstancename is not None else self.workingInstance
        
        if self.workingInstance is None:
            raise Exception("You must provide an instance name or set the working instance before executing this method")
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/mds/api/v1/connectors?internalOnly={internalOnly}"
        headers = {
            "Authorization": self.accessToken,
            "Dwinstancename": self.workingInstance,
            "Tenantname": self.tenantName
        }
        
        response = requests.get(url, headers=headers)
        
        response_json = self._handle_response(response)
        
        if 'content' in response_json:
            self.connectors[self.workingInstance] = response_json['content']
        
        return response_json

    def get_cluster_details(self, Dwinstancename = None) -> dict:
        """
        Retrieves cluster details from the Veeva Nitro API.
        
        Returns:
            dict: The response JSON containing cluster details.
            
        Raises:
            Exception: If the request for cluster details fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        self.workingInstance = Dwinstancename if Dwinstancename is not None else self.workingInstance
        
        if self.workingInstance is None:
            raise Exception("You must provide an instance name or set the working instance before executing this method")
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/api/v1/admin/cluster-details"
        headers = {
            "Authorization": self.accessToken,
            "Dwinstancename": self.workingInstance,
            "Tenantname": self.tenantName
        }
        
        response = requests.get(url, headers=headers)
        
        response_json = self._handle_response(response)
        
        if 'content' in response_json:
            self.clusterDetails[self.workingInstance] = response_json['content']
        
        return response_json

    def get_job_results(self, Dwinstancename: str = None, size: int = 1000, jobId: str = None) -> dict:
        """
        Retrieves job results from the Veeva Nitro API.
        
        Args:
            instanceName (str): The name of the instance.
            size (int, optional): The number of results to retrieve. Defaults to 1000.
            jobId (str, optional): The ID of the job. Defaults to None.
            
        Returns:
            dict: The response JSON containing job results.
            
        Raises:
            Exception: If the request for job results fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        self.workingInstance = Dwinstancename if Dwinstancename is not None else self.workingInstance
        
        if self.workingInstance is None:
            raise Exception("You must provide an instance name or set the working instance before executing this method")
        
        # Check if authentication has taken place
        if self.accessToken is None:
            raise Exception("You must authenticate first before executing this method")
        
        url = f"{self.serverUrl}/api/v1/admin/jobs/results?instanceName={self.workingInstance}&size={size}&jobId={jobId}"
        headers = {
            "Authorization": self.accessToken
        }
        
        response = requests.get(url, headers=headers)
        
        response_json = self._handle_response(response)
        
        if 'content' in response_json:
            self.jobResults[self.workingInstance] = response_json['content']
        
        return response_json
    
    
    ##############################################################################################################
    # Async methods
    ##############################################################################################################
    
    async def get_rules_from_instances(self, instances: List[str] = None):
        """
        Retrieves rule information from the Veeva Nitro API for a list of instances.
        
        Args:
            instances (List[str], optional): A list of instance names. Defaults to None.
            
        Returns:
            dict: The response JSON containing rule details.
            
        Raises:
            Exception: If the request for rule information fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        instances = instances if instances is not None else [instance['instanceName'] for instance in self.instances]
        
        # Create a list of async tasks
        tasks = []
        
        async_get_rules = async_wrap(self.get_rules)
        
        rules_dict = {}
        
        for instance in instances:
            tasks.append(async_get_rules(Dwinstancename=instance))
        
        # Execute the async tasks
        responses = await asyncio.gather(*tasks)
        
        # Create a dictionary of the responses
        for i, instance in enumerate(instances):
            rules_dict[instance] = responses[i]['content']
        
        self.rules = rules_dict
        
        return rules_dict
    

    async def get_groups_from_instances(self, instances: List[str] = None):
        """
        Retrieves rule group information from the Veeva Nitro API for a list of instances.
        
        Args:
            instances (List[str], optional): A list of instance names. Defaults to None.
            
        Returns:
            dict: The response JSON containing rule group details.
            
        Raises:
            Exception: If the request for rule group information fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        instances = instances if instances is not None else [instance['instanceName'] for instance in self.instances]
        
        # Create a list of async tasks
        tasks = []
        
        async_get_groups = async_wrap(self.get_groups)
        
        groups_dict = {}
        
        for instance in instances:
            tasks.append(async_get_groups(Dwinstancename=instance))
        
        # Execute the async tasks
        responses = await asyncio.gather(*tasks)
        
        # Create a dictionary of the responses
        for i, instance in enumerate(instances):
            groups_dict[instance] = responses[i]['content']
        
        self.groups = groups_dict
        
        return groups_dict

    async def get_jobs_from_instances(self, instances: List[str] = None, view: str = "condensed"):
        """
        Retrieves job information from the Veeva Nitro API for a list of instances.
        
        Args:
            instances (List[str], optional): A list of instance names. Defaults to None.
            view (str, optional): The view type for the jobs. Defaults to "condensed".
            
        Returns:
            dict: The response JSON containing job details.
            
        Raises:
            Exception: If the request for job information fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        instances = instances if instances is not None else [instance['instanceName'] for instance in self.instances]
        
        # Create a list of async tasks
        tasks = []
        
        async_get_jobs = async_wrap(self.get_jobs)
        
        jobs_dict = {}
        
        for instance in instances:
            tasks.append(async_get_jobs(Dwinstancename=instance, view=view))
        
        # Execute the async tasks
        responses = await asyncio.gather(*tasks)
        
        # Create a dictionary of the responses
        for i, instance in enumerate(instances):
            jobs_dict[instance] = responses[i]['content']
        
        self.jobs = jobs_dict
        
        return jobs_dict
    
    async def get_connectors_from_instances(self, instances: List[str] = None, internalOnly: bool = False):
        """
        Retrieves connector information from the Veeva Nitro API for a list of instances.
        
        Args:
            instances (List[str], optional): A list of instance names. Defaults to None.
            internalOnly (bool, optional): Filter for internal connectors. Defaults to False.
            
        Returns:
            dict: The response JSON containing connector details.
            
        Raises:
            Exception: If the request for connectors fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        instances = instances if instances is not None else [instance['instanceName'] for instance in self.instances]
        
        # Create a list of async tasks
        tasks = []
        
        async_get_connectors = async_wrap(self.get_connectors)
        
        connectors_dict = {}
        
        for instance in instances:
            tasks.append(async_get_connectors(Dwinstancename=instance, internalOnly=internalOnly))
        
        # Execute the async tasks
        responses = await asyncio.gather(*tasks)
        
        # Create a dictionary of the responses
        for i, instance in enumerate(instances):
            connectors_dict[instance] = responses[i]['content']
        
        self.connectors = connectors_dict
        
        return connectors_dict
    
    async def get_cluster_details_from_instances(self, instances: List[str] = None):
        """
        Retrieves cluster details from the Veeva Nitro API for a list of instances.
        
        Args:
            instances (List[str], optional): A list of instance names. Defaults to None.
            
        Returns:
            dict: The response JSON containing cluster details.
            
        Raises:
            Exception: If the request for cluster details fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        instances = instances if instances is not None else [instance['instanceName'] for instance in self.instances]
        
        # Create a list of async tasks
        tasks = []
        
        async_get_cluster_details = async_wrap(self.get_cluster_details)
        
        cluster_details_dict = {}
        
        for instance in instances:
            tasks.append(async_get_cluster_details(Dwinstancename=instance))
        
        # Execute the async tasks
        responses = await asyncio.gather(*tasks)
        
        # Create a dictionary of the responses
        for i, instance in enumerate(instances):
            cluster_details_dict[instance] = responses[i]['content']
        
        self.clusterDetails = cluster_details_dict
        
        return cluster_details_dict
    
    async def get_job_results_from_instances(self, instances: List[str] = None, size: int = 1000, jobId: str = None):
        """
        Retrieves job results from the Veeva Nitro API for a list of instances.
        
        Args:
            instances (List[str], optional): A list of instance names. Defaults to None.
            size (int, optional): The number of results to retrieve. Defaults to 1000.
            jobId (str, optional): The ID of the job. Defaults to None.
            
        Returns:
            dict: The response JSON containing job results.
            
        Raises:
            Exception: If the request for job results fails.
            Exception: If not authenticated.
            Exception: If no instance name is provided or set as the working instance.
        """
        
        instances = instances if instances is not None else [instance['instanceName'] for instance in self.instances]
        
        # Create a list of async tasks
        tasks = []
        
        async_get_job_results = async_wrap(self.get_job_results)
        
        job_results_dict = {}
        
        for instance in instances:
            tasks.append(async_get_job_results(Dwinstancename=instance, size=size, jobId=jobId))
        
        # Execute the async tasks
        responses = await asyncio.gather(*tasks)
        
        # Create a dictionary of the responses
        for i, instance in enumerate(instances):
            job_results_dict[instance] = responses[i]['content']
        
        self.jobResults = job_results_dict
        
        return job_results_dict
    
    
    async def get_all_tenant_details(self):
        
        tasks = [
            self.get_rules_from_instances(),
            self.get_groups_from_instances(),
            self.get_jobs_from_instances(),
            self.get_connectors_from_instances(),
            self.get_cluster_details_from_instances(),
            self.get_job_results_from_instances()
        ]
        
        result_dict = {}
        
        result = await asyncio.gather(*tasks)
        
        for i, instance in enumerate(self.instances):
            result_dict[instance['instanceName']] = {
                'rules': result[0][instance['instanceName']],
                'groups': result[1][instance['instanceName']],
                'jobs': result[2][instance['instanceName']],
                'connectors': result[3][instance['instanceName']],
                'clusterDetails': result[4][instance['instanceName']],
                'jobResults': result[5][instance['instanceName']]
            }
        
        return result_dict