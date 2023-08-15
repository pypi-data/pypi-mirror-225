import pytest
import os
from src.pyzab import Zabbix
from dotenv import load_dotenv


@pytest.fixture
def zabbix_client():
    load_dotenv()
    config = {
        'zabbix_api_url': os.getenv('zabbix_url'),
        'zabbix_auth_token': os.getenv('zabbix_auth_token')
    }
    return Zabbix(**config)

it@github.com:LucasRochaAbr
def test_get_host(zabbix_client):
    """ Tests an API call to get info about a host."""
    host = zabbix_client.get_host(filter={"hostid": "10917"})
    assert isinstance(host, dict)
    assert isinstance(host['host'], str)


def test_get_all_hosts(zabbix_client):
    """ Tests an API call to get all hosts based on given optional filters."""
    hosts = zabbix_client.get_all_hosts(filter={"status": "1"})
    assert isinstance(hosts, list)


def test_create_host(zabbix_client):
    new_host = zabbix_client.create_host(hostname="Host para testes de API3", ip="10.99.99.99", group_id="5", template_id="10186")
    assert isinstance(new_host, dict)
    assert isinstance(new_host['hostids'], list)
    assert isinstance(new_host['hostids'][0], str)


def test_delete_host(zabbix_client):
    deleted_host = zabbix_client.delete_host(host_id="10917")
    assert isinstance(deleted_host, dict)
    assert isinstance(deleted_host['hostids'], list)
    assert deleted_host['hostids'] == '10917'


def test_enable_host(zabbix_client):
    host = zabbix_client.enable_host(host_id="10917")
    assert isinstance(host, dict)
    assert isinstance(host['hostids'], list)
    assert host['hostids'][0] == '10917'


def test_disable_host(zabbix_client):
    host = zabbix_client.disable_host(host_id="10917")
    assert isinstance(host, dict)
    assert isinstance(host['hostids'], list)
    assert host['hostids'][0] == '10917'


def test_get_host_interface(zabbix_client):
    """ Tests an API call to get all interface info of a specific host."""
    host = zabbix_client.get_host_interface(host_id="10917")
    assert isinstance(host, dict)
    assert host['hostid'] == "10917"


def test_get_group_ids(zabbix_client):
    ...


def test_get_all_templates(zabbix_client):
    ...

