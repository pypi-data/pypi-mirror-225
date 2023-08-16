import sys
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))
from datetime import datetime
from dotenv import load_dotenv
import pytest
from entity_type.EntityType import EntityType
from logger_local.LoggerLocal import logger_local
from logger_local.LoggerComponentEnum import LoggerComponentEnum

ENTITY_TYPE_COMPONENT_ID = 116
COMPONENT_NAME = 'entity-type-local-python-package'

logger_code_init  = {
    'component_id': ENTITY_TYPE_COMPONENT_ID,
    'component_name': COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
    'developer_email': 'idan.a@circ.zone'
}
logger_local.init(object=logger_code_init )

load_dotenv()

ENTITY_NAME = "TEST"+str(datetime.now())
ENTITY_NAME_INVALID = "INVALID"
USER_ID = 5000091

def test_insert_select():
    logger_local.start(object={})
    EntityType.insert_entity_type_id_by_name(ENTITY_NAME, USER_ID)
    entity = EntityType.get_entity_type_id_by_name(ENTITY_NAME)
    entity is not None
    logger_local.end("Test succeeded", object={})

def test_select_invalid():
    logger_local.start(object={})
    entity = EntityType.get_entity_type_id_by_name(ENTITY_NAME_INVALID)
    entity is None
    logger_local.end("Test succeeded", object={})