import sys
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..', 'db'))
from circles_local_database_python.connection import Connection
from dotenv import load_dotenv
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.LoggerLocal import logger_local
import mysql.connector

from datetime import datetime




load_dotenv()
EXTERNAL_USER_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 115
EXTERNAL_USER_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME='external_user_local'
DEVELOPER_EMAIL="idan.a@circ.zone"
object_init = {
    'component_id': EXTERNAL_USER_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': EXTERNAL_USER_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    "developer_email": DEVELOPER_EMAIL,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
}
logger_local.init(object=object_init)



class ExternalUserDb:
    def __init__(self):
        pass

    @staticmethod
    def insert_or_update_external_user_access_token(user_name, profile_id, system_id, access_token):
        try:
            object_start = {
                'user_name': user_name,
                'profile_id': profile_id,
                'access_token': access_token
            }
            logger_local.start(object=object_start)
            connection = Connection('external_user').connect()
            query_insert_external = "INSERT INTO external_user.external_user_table (system_id,username,token) VALUES (%s,%s,%s)"
            values = (system_id, user_name, access_token)
            cursor = connection.cursor()
            cursor.execute(query_insert_external, values)
            id_new = cursor.lastrowid()
            values = (id_new, profile_id)
            query_insert_external_user_profile = "INSERT INTO external_user_profile.external_user_profile_table (external_user_id,profile_id) VALUES (%s,%s)"
            cursor = connection.cursor()
            cursor.execute(query_insert_external_user_profile, values)
            connection.commit()
            object_info = {
                'user_name': user_name,
                'system_id': system_id,
                'profile_id': profile_id,
                'access_token': access_token,
            }
            logger_local.info("external user updated",object=object_info)
        except mysql.connector.Error as error:
            logger_local.exception(object=error)
        logger_local.end(object={})

    @staticmethod
    def get_access_token(user_name, profile_id, system_id):
        access_token = None
        try:
            object_start = {
                'user_name': user_name,
                'profile_id': profile_id,
                'system_id': system_id
            }
            logger_local.start(object=object_start)
            connection = Connection('external_user').connect()
            query_get = "SELECT token FROM external_user.external_user_view as eu join external_user_profile.external_user_profile_table as eup on eu.external_user_id=eup.external_user_id WHERE eu.username=%s AND eu.system_id=%s And eup.profile_id=%s"
            cursor = connection.cursor()
            cursor.execute(query_get, (user_name, system_id, profile_id))
            access_token = cursor.fetchone()
            return access_token
        except mysql.connector.Error as error:
            logger_local.exception(object=error)
        logger_local.end(object={'access_token': access_token})

    @staticmethod
    def get_all_tokens_by_system_id(system_id):
        # good for update users details by system
        access_tokens = None
        try:
            object_start = {
                'system_id': system_id
            }
            logger_local.start(object=object_start)
            connection = Connection('external_user').connect()
            query_get_all = "SELECT token FROM external_user.external_user_view WHERE system_id=%s"
            cursor = connection.cursor()
            cursor.execute(query_get_all, (system_id))
            access_tokens = cursor.fetchall()
            cursor.close()
            connection.close()
            return access_tokens
        except mysql.connector.Error as error:
            logger_local.exception(object=error)
        logger_local.end(object={'access_tokens': access_tokens})

    @staticmethod
    def update_access_token(user_name, system_id, profile_id, access_token):
        try:
            object_start = {
                'user_name': user_name,
                'system_id': system_id,
                'profile_id': profile_id,
                'access_token': access_token,
            }
            logger_local.start(object=object_start)
            connection = Connection('external_user').connect()
            update_query = "UPDATE external_user.external_user_table AS eu JOIN external_user_profile.external_user_profile_table AS eup ON eu.external_user_id = eup.external_user_id SET eu.token = %s WHERE eu.username = %s AND eu.system_id = %s AND eup.profile_id = %s;"
            values = (access_token, user_name, system_id, profile_id)
            cursor = connection.cursor()
            cursor.execute(update_query, values)
            connection.commit()
            cursor.close()
            connection.close()
            object_info = {
                'user_name': user_name,
                'system_id': system_id,
                'profile_id': profile_id,
                'access_token': access_token,
            }
            logger_local.info("external user updated",object=object_info)
        except mysql.connector.Error as error:
            logger_local.exception(object=error)
        logger_local.end(object={})

    @staticmethod
    def delete_access_token(user_name, system_id, profile_id):
        try:
            object_start = {
                'user_name': user_name,
                'system_id': system_id,
                'profile_id': profile_id,
            }
            logger_local.start(object=object_start)
            connection = Connection('external_user').connect()
            cursor = connection.cursor()
            update_query = "UPDATE external_user.external_user_table AS eu JOIN external_user_profile.external_user_profile_table AS eup ON eu.external_user_id = eup.external_user_id SET eu.end_timestamp = %s WHERE eu.username = %s AND eu.system_id = %s AND eup.profile_id = %s;"
            current_datetime = datetime.now()
            current_date = current_datetime.date()
            values = (current_date, user_name, system_id, profile_id)
            cursor.execute(update_query, values)
            cursor.close()
            connection.commit()
            connection.close()
            object_info = {
                'user_name': user_name,
                'system_id': system_id,
                'profile_id': profile_id,
            }
            logger_local.info("external user updated",object=object_info)
        except mysql.connector.Error as error:
            logger_local.exception(object=error)
        logger_local.end(object={})
