
import pytest
import os # for getting the environment variables
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..')) # the absolute path of the directory that contains the current file
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.LoggerLocal import logger_local
from src.ZoomInfo import ZoomInfo
from dotenv import load_dotenv
load_dotenv()

# set the component id for the logger
ZOOM_IMPORTER_LOCAL = 178

obj = {
    'component_id': ZOOM_IMPORTER_LOCAL,
    'component_name': 'Zoom Importer Local',
    'component_type': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'developer_email': 'sahar.g@circ.zone',
    'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
}

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_url = os.getenv("REDIRECT_URL")
access_token = os.getenv("ACCESS_TOKEN")

@pytest.fixture(scope="module", autouse=True)
def setup_logger():
    logger_local.init(object=obj)
    yield


def test_get_user_by_email():
    logger_local.start()
    try:
        zoom = ZoomInfo(client_id=client_id, client_secret=client_secret, redirect_url=redirect_url ,access_token=access_token)
        email = "sahar.g@circ.zone"
        user_data = zoom.get_user_by_email(email)
        assert user_data is not None
    except Exception as e:
        logger_local.exception("Exception in test_get_user_by_email", object = e)
    logger_local.end()

def test_get_users():
    logger_local.start()
    try:
        zoom = ZoomInfo(client_id=client_id, client_secret=client_secret, redirect_url=redirect_url ,access_token=access_token)
        users = zoom.get_all_users()
        assert users is not None
    except Exception as e:
        logger_local.exception("Exception in test_get_users", object = e)
    logger_local.end()

def test_get_user_id():
    logger_local.start()
    try:
        zoom = ZoomInfo(client_id=client_id, client_secret=client_secret, redirect_url=redirect_url ,access_token=access_token)
        email = "sahar.g@circ.zone"
        user_id = zoom.get_user_id(email)
        assert user_id is not None
    except Exception as e:
        logger_local.exception("Exception in test_get_user_id", object = e)
    logger_local.end()

def test_get_user_by_id():
    logger_local.start()
    try:
        zoom = ZoomInfo(client_id=client_id, client_secret=client_secret, redirect_url=redirect_url ,access_token=access_token)
        user_id = "NjXUCPGMR4qBQP7tGeEc3g"
        user_data = zoom.get_user_by_id(user_id)
        assert user_data is not None
    except Exception as e:
        logger_local.exception("Exception in test_get_user_by_id", object = e)
    logger_local.end()

def test_get_request():
    logger_local.start()
    try:
        zoom = ZoomInfo(client_id=client_id, client_secret=client_secret, redirect_url=redirect_url ,access_token=access_token)
        endpoint = "users"
        params = {"email": "sahar.g@circ.zone"}
        response = zoom._get_request(endpoint, params=params)
        assert response is not None
    except Exception as e:
        logger_local.exception("Exception in test_get_request", object = e)
    logger_local.end()
    
def test_get_user_by_phone():
    logger_local.start()
    try:
        zoom = ZoomInfo(client_id=client_id, client_secret=client_secret, redirect_url=redirect_url ,access_token=access_token)
        phone = ""
        user_data = zoom.get_user_by_phone(phone)
        assert user_data is not None
    except Exception as e:
        logger_local.exception("Exception in test_get_user_by_phone", object = e)
    logger_local.end()

def test_get_user_by_name():
    logger_local.start()
    try:
        zoom = ZoomInfo(client_id=client_id, client_secret=client_secret, redirect_url=redirect_url, access_token=access_token)
        first_name = "sahar"
        last_name = ""
        user_data = zoom.ger_user_by_name(first_name, last_name)
        assert user_data is not None
    except Exception as e:
        logger_local.exception("Exception in test_get_user_by_name", object = e)
    logger_local.end()


def test_get_next_page_token():
    logger_local.start()
    try:
        zoom = ZoomInfo(client_id=client_id, client_secret=client_secret, redirect_url=redirect_url, access_token=access_token)
        token = zoom.get_next_page_token()
        assert token is not None
    except Exception as e:
        logger_local.exception("Exception in test_get_next_page_token", object = e)
    logger_local.end()


def test_get_all_users_by_location():
    logger_local.start()
    try:
        zoom = ZoomInfo(client_id=client_id, client_secret=client_secret, redirect_url=redirect_url ,access_token=access_token)
        location = ""
        users_data = zoom.get_all_users_by_location(location)
        assert users_data is not None
    except Exception as e:
        logger_local.exception("Exception in test_get_all_users_by_location", object = e)
    logger_local.end()


def test_get_all_users_by_job_title():
    logger_local.start()
    try:
        zoom = ZoomInfo(client_id=client_id, client_secret=client_secret, redirect_url=redirect_url ,access_token=access_token)
        job_title = ""
        users_data = zoom.get_all_users_by_job_title(job_title)
        assert users_data is not None
    except Exception as e:
        logger_local.exception("Exception in test_get_all_users_by_job_title", object = e)
    logger_local.end()