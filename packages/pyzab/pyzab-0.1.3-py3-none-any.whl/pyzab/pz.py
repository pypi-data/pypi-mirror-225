import requests
import os

# TODO
## - turn the module into a class, and the functions into methods
## - Use pydantic to model
## - Async support
## - Remove dotenv from pypi, and move it to tests dir
## - Docstrings and docs site
## - Logging
## - create host (with agent)
## - create host (with snmp)
## - enable/disable host (status = 0 --> enable)
## - get enabled/disabled hosts (status = 0 --> enabled)
## - get all groupids
## - get a host interfaces
## - get all hosts in a groupid
## - get all templates
## - add proxy option to create host
## - add update_host method

class Zabbix():
    def __init__(self, zabbix_api_url, zabbix_auth_token):
        self.url = zabbix_api_url
        self.token = zabbix_auth_token


    def get_host(self, filter={"":""}, output=["host", "hostid", "status", "templateid"]):
        """
        returns:
        {'hostid': '12345', 'host': 'exemplo', 'status': '0', 'templateid': '0'}
        """
        get_hosts_json = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": output,
                "filter": filter,
                "available": True
            },
            "auth": self.token,
            "id": 1
        }
        response = requests.post(url = self.url, json=get_hosts_json)
        #print(response.json())
        return response.json()['result'][0]


    def get_all_hosts(self, filter= {"": ""}, output=["host", "hostid", "status", "templateid"]):
        """
        returns:
        [{'hostid': '12345', 'host': 'exemplo', 'status': '0', 'templateid': '0'}]
        """
        get_hosts_json = {
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": output,
                "filter": filter,
                "available": True
            },
            "auth": self.token,
            "id": 1
        }
        response = requests.post(url = self.url, json=get_hosts_json)
        #print(response.json())
        return response.json()['result']


    def create_host(self, hostname, ip, group_id, template_id, type="agent", port="10050"):
        """
        Returns: {'hostids': ['12345']}
        *** Still need to handle cases where the hostname already exists
        """
        create_host_json = {
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": {
                "host": hostname,
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": ip,
                        "dns": "",
                        "port": port
                    }
                ],
                "groups": [
                    {
                        "groupid": group_id
                    }
                ],
                "tags": [
                    #{
                    #    "tag": "Teste de tag",
                    #    "value": "Resultado do teste"
                    #}
                ],
                "templates": [
                    {
                        "templateid": template_id
                    }
                ],
                "macros": [
                    #{
                    #    "macro": "{$USER_LOCATION}",
                    #    "value": "0:0:0",
                    #    "description": "latitude, longitude and altitude coordinates"
                    #}
                ],
                #"inventory_mode": 0,
                #"inventory": {
                #    "macaddress_a": "01234",
                #    "macaddress_b": "56768"
                #}
            },
            "auth": self.token,
            "id": 1
        }
        response = requests.post(url=self.url, json=create_host_json)
        #print(response.json())
        return response.json()['result']


    def delete_host(self, host_id):
        """
        Returns: {'hostids': ['10916']}
        *** Still need to handle cases where the hostname doesn't exist
        """
        delete_host_json = {
            "jsonrpc": "2.0",
            "method": "host.delete",
            "params": [
                host_id
            ],
            "auth": self.token,
            "id": 1
        }
        response = requests.post(url=self.url, json=delete_host_json)
        return response.json()['result']


    def enable_host(self, host_id):
        """
        Returns: {'hostids': ['10917']}
        """
        enable_host_json = {
            "jsonrpc": "2.0",
            "method": "host.update",
            "params": {
                "hostid": host_id,
                "status": 0
            },
            "auth": self.token,
            "id": 1
        }
        response = requests.post(url=self.url, json=enable_host_json)
        #print(response.json())
        return response.json()['result']


    def disable_host(self, host_id):
        """
        Returns: {'hostids': ['10917']}
        """
        disable_host_json = {
            "jsonrpc": "2.0",
            "method": "host.update",
            "params": {
                "hostid": host_id,
                "status": 1
            },
            "auth": self.token,
            "id": 1
        }
        response = requests.post(url=self.url, json=disable_host_json)
        #print(response.json())
        return response.json()['result']


    def get_host_interface(self, host_id):
        """
        returns:
        {'hostid': '12345', 'host': 'exemplo', 'status': '0', 'templateid': '0'}
        """
        get_hosts_json = {
            "jsonrpc": "2.0",
            "method": "hostinterface.get",
            "params": {
                "output": "extend",
                "hostids": host_id
            },
            "auth": self.token,
            "id": 1
        }
        response = requests.post(url = self.url, json=get_hosts_json)
        return response.json()['result'][0]


    def get_group_ids(self):
        ...


    def get_all_templates(self):
        ...


    def create_webscenario(self, webscenario_name: str, template_id: str, steps: dict):
        """
        Note: This needs a hostid or templateid (which will still go into hostid field).
        Returns: status code
        """
        update_template_json = {
            "jsonrpc": "2.0",
            "method": "httptest.create",
            "params": {
                "name": webscenario_name,
                "hostid": template_id,
                "steps": [
                    {
                        "name": steps["name"],
                        "url": steps["url"],
                        "status_codes": steps["status_code"],
                        "no": steps["step_number"]
                    }
                ]
            },
            "auth": self.token,
            "id": 1
        }
        response = requests.post(url=self.url, json=update_template_json)

        return response.status_code


    def __repr__(self):
        return "Zabbix API connection instance."

