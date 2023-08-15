import sys
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))
from src.external_user import ExternalUser
import dotenv
from datetime import datetime
from logger_local.LoggerLocal import logger_local
from logger_local.LoggerComponentEnum import LoggerComponentEnum



dotenv.load_dotenv()

USER_EXTERNAL="TEST"+str(datetime.now())
EXTERNAL_USER_COMPONENT_ID = 115
EXTERNAL_USER_COMPONENT_NAME='external_user_local'
object_init = {
    'component_id': EXTERNAL_USER_COMPONENT_ID,
    'component_name':EXTERNAL_USER_COMPONENT_NAME,
    'component_category':LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'testing_framework':LoggerComponentEnum.testingFramework.pytest.value,
    "developer_email":"idan.a@circ.zone"
}
logger_local.init(object=object_init)


def test_insert_get():
    logger_local.start("test started")
    ExternalUser.insert_or_update_external_user_access_token(
        USER_EXTERNAL, 2, 1, "access_token_test")
    token = ExternalUser.get_access_token(USER_EXTERNAL, 2, 1)
    assert token[0] == "access_token_test"
    logger_local.end("test successfull")



def test_update_access_token():
    logger_local.start("test started")
    ExternalUser.update_external_user_access_token(USER_EXTERNAL, 1, 2, "access_token_test2")
    token = ExternalUser.get_access_token(USER_EXTERNAL, 2, 1)
    assert token[0] == "access_token_test2"
    logger_local.end("test successfull")



def test_delete_access_token():
    logger_local.start("test started")
    ExternalUser.delete_access_token(USER_EXTERNAL, 1, 2)
    token = ExternalUser.get_access_token(USER_EXTERNAL, 2, 1)
    assert token is None
    logger_local.end("test successfull")

