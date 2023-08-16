from dotenv import load_dotenv
from logger_local.LoggerLocal import logger_local
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.connection import DatabaseFunctions
load_dotenv()

ENTITY_TYPE_COMPONENT_ID = 116
ENTITY_TYPE_COMPONENT_NAME = 'entity-type-local-python-package'

logger_code_init  = {
    'component_id': ENTITY_TYPE_COMPONENT_ID,
    'component_name': ENTITY_TYPE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'idan.a@circ.zone'
}
logger_local.init(object=logger_code_init)
database_conn = DatabaseFunctions("entityType")
connection = database_conn.connect()

class EntityType:

    def __init__(self):
        pass

    @staticmethod
    def get_entity_type_id_by_name(entity_type_name):
        entity_type_id = None
        try:
            object1 = {
                'entity_type_name': entity_type_name
            }
            logger_local.start(object=object1)
            sql_query = "SELECT entity_type_id FROM entity_type.entity_type_en_view WHERE entity_type_name = '{}'".format(
                entity_type_name)
            cursor = connection.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            if result:
                entity_type_id = result[0]
        except Exception as e:
            logger_local.exception(object=e)
        object1 = {
            'entity_type_id': entity_type_id
        }
        logger_local.end(object=object1)
        return entity_type_id

    @staticmethod
    def insert_entity_type_id_by_name(entity_type_name, user_id):
        try:
            object1 = {
                'entity_type_name': entity_type_name
            }
            logger_local.start(object=object1)
            cursor = connection.cursor()
            query_entity = "INSERT INTO entity_type.entity_type_table(`created_user_id`,`updated_user_id`)" \
                " VALUES ({}, {})".format(user_id, user_id)
            cursor.execute(query_entity)
            last_inserted_id = cursor.lastrowid
            query_entity_ml = "INSERT INTO entity_type.entity_type_ml_table(`entity_type_name`,`entity_type_id`,`lang_code`,`created_user_id`,`updated_user_id`)" \
                              " VALUES (%s, %s, %s, {}, {})".format(
                                  user_id, user_id)
            cursor.execute(query_entity_ml,
                           (entity_type_name, last_inserted_id, 'en'))
            logger_local.end(object={})
            connection.commit()
        except Exception as e:
            logger_local.exception(object=e)
        logger_local.end(object={})
