
import pytest
import os # for getting the environment variables
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..')) # the absolute path of the directory that contains the current file

from logger_local.LoggerLocal import logger_local
from src.ZoomAPI import ZoomAPI
from dotenv import load_dotenv
load_dotenv()

# set the component id for the logger
DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_ID = 13
CLIENT_ID = "o8MQRrHSLOmNvJimS87_Q"
CLIENT_SECRET = "4z3bfgMCaVIfO8GdIiwCmTZT3Fb7qBlR"
ACCESS_TOKEN = 'eyJzdiI6IjAwMDAwMSIsImFsZyI6IkhTNTEyIiwidiI6IjIuMCIsImtpZCI6ImI1MTRkMDBjLTQ4MDEtNDY1Ny1hN2UwLTRkNDVhOGYzMzRmOSJ9.eyJ2ZXIiOjksImF1aWQiOiI0NTk2ZTk5NWFiYmYzYjA5OGU4YWEwN2NmMDQ1OTU1ZCIsImNvZGUiOiJBb041Wm1jY0c2U25UcjlNNVV2UkNLR09IYVdlZDRlQVEiLCJpc3MiOiJ6bTpjaWQ6bzhNUVJySFNMT21OdkppbVM4N19RIiwiZ25vIjowLCJ0eXBlIjowLCJ0aWQiOjAsImF1ZCI6Imh0dHBzOi8vb2F1dGguem9vbS51cyIsInVpZCI6Ik5KWFVDUEdNUjRxQlBRN3RHZUVjM2ciLCJuYmYiOjE2OTIwOTE0MDAsImV4cCI6MTY5MjA5NTAwMCwiaWF0IjoxNjkyMDkxNDAwLCJhaWQiOiJQNzBhZkVKb1FUcVgyNXVaUlBSRUdBIn0.Q-uZYX6OfUMFFcJ6LtD4EdP2FkZukyGLGbKwXSX1-Me1r9VxeW6ACWg0PqJHlGpNG_C230dYPdhCjzS-vlsLpw'
REDIRECT_URL = 'https://zoom.us/oauth/authorize?response_type=code&client_id=o8MQRrHSLOmNvJimS87_Q&redirect_uri=https%3A"%2F%2Foauth.pstmn.io%2Fv1%2Fbrowser-callback'



@pytest.fixture(scope="module", autouse=True)
def setup_logger():
    logger_local.init(object={
        'component_id': DATABASE_WITHOUT_ORM_PYTHON_PACKAGE_COMPONENT_ID
    })
    yield

def test_get_access_token():
    logger_local.start()
    try:
        zoom = ZoomAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        access_token = zoom.get_access_token()
        print(access_token)
        assert access_token is not None
    except Exception as e:
        logger_local.exception("Exception in test_get_access_token", object = e)
    logger_local.end()



def test_get_user_by_email():
    logger_local.start()
    try:
        zoom = ZoomAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token=ACCESS_TOKEN)
        email = "sahar.g@circ.zone"
        user_data = zoom.get_user_by_email(email)
        assert user_data is not None
    except Exception as e:
        logger_local.exception("Exception in test_get_user_by_email", object = e)
    logger_local.end()

def test_get_users():
    logger_local.start()
    try:
        zoom = ZoomAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token=ACCESS_TOKEN)
        users = zoom.get_users()
        assert users is not None
    except Exception as e:
        logger_local.exception("Exception in test_get_users", object = e)
    logger_local.end()


def test_get_user_id():
    logger_local.start()
    try:
        zoom = ZoomAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token=ACCESS_TOKEN)
        email = "sahar.g@circ.zone"
        user_id = zoom.get_user_id(email)
        assert user_id is not None
    except Exception as e:
        logger_local.exception("Exception in test_get_user_id", object = e)
    logger_local.end()

def test_get_user_by_id():
    logger_local.start()
    try:
        zoom = ZoomAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, access_token=ACCESS_TOKEN)
        user_id = "NjXUCPGMR4qBQP7tGeEc3g"
        user_data = zoom.get_user_by_id(user_id)
        assert user_data is not None
    except Exception as e:
        logger_local.exception("Exception in test_get_user_by_id", object = e)
    logger_local.end()
