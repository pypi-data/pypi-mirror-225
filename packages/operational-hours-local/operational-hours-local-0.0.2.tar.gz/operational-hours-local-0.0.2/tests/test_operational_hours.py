import sys
import os
import time
from dotenv import load_dotenv
from logger_local.LoggerComponentEnum import LoggerComponentEnum

script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '../operational_hours_local'))

load_dotenv()
from operational_hours import OperationalHours
from logger_local.LoggerLocal import logger_local as local_logger
from circles_local_database_python.connection import Connection

database = Connection("operational_hours")
connection = database.connect()

TEST_INSERT_SELECT_OPERATIONAL_HOURS_FUNCTION_NAME = "test_insert_select_operational_hours"
TEST_GET_OPERATIONAL_HOURS_ID_FUNCTION_NAME = "test_get_operational_hours_id"
TEST_GET_OPERATIONAL_HOURS_IDS_FUNCTION_NAME = "test_get_operational_hours_ids"
TEST_SELECT_INVALID_OPERATIONAL_HOURS_FUNCTION_NAME = "test_select_invalid_operational_hours"
TEST_UPDATE_OPERATIONAL_HOURS_FUNCTION_NAME = "test_update_operational_hours"
TEST_DELETE_OPERATIONAL_HOURS_FUNCTION_NAME = "test_delete_operational_hours"
TEST_CREATE_HOURS_ARRAY_OPERATIONAL_HOURS_FUNCTION_NAME = "test_create_hours_array_operational_hours"
OPERATIONAL_HOURS_TEST_COMPONENT_NAME = 'tests/test_operational_hours.py'
OPERATIONAL_HOURS_COMPONENT_ID = 158 

object_to_insert = {
    'payload': 'test the methods of OperationalHours class in operational-hours-local',
    'component_id': OPERATIONAL_HOURS_COMPONENT_ID,
    'component_name': OPERATIONAL_HOURS_TEST_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Unit_Test.value,
    'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
    'developer_email': 'tal.g@circ.zone'
}
local_logger.init(object=object_to_insert)

DAY_OF_WEEK_STRING = "day_of_week"
FROM_TIME_STRING = "from_time"
UNTIL_TIME_STRING = "until_time"

HOURS1 = [
    {
        FROM_TIME_STRING: 80000,
        UNTIL_TIME_STRING: 200000
    },
    {
        FROM_TIME_STRING: 80000,
        UNTIL_TIME_STRING: 200000
    },
    {
        FROM_TIME_STRING: 80000,
        UNTIL_TIME_STRING: 200000
    },
    {
        FROM_TIME_STRING: 80000,
        UNTIL_TIME_STRING: 200000
    },
    {
        FROM_TIME_STRING: 80000,
        UNTIL_TIME_STRING: 200000
    },
    {
        FROM_TIME_STRING: 80000,
        UNTIL_TIME_STRING: 200000
    },
    {
        FROM_TIME_STRING: 80000,
        UNTIL_TIME_STRING: 200000
    }
]

HOURS2 = [
    {
        FROM_TIME_STRING: 90000,
        UNTIL_TIME_STRING: 190000
    },
    {
        FROM_TIME_STRING: 90000,
        UNTIL_TIME_STRING: 190000
    },
    {
        FROM_TIME_STRING: 90000,
        UNTIL_TIME_STRING: 190000
    },
    {
        FROM_TIME_STRING: 90000,
        UNTIL_TIME_STRING: 190000
    },
    {
        FROM_TIME_STRING: 90000,
        UNTIL_TIME_STRING: 190000
    },
    {
        FROM_TIME_STRING: 90000,
        UNTIL_TIME_STRING: 190000
    },
    {
        FROM_TIME_STRING: 90000,
        UNTIL_TIME_STRING: 190000
    }
]

HOURS_INVALID = [
    {
        FROM_TIME_STRING: 800,
        UNTIL_TIME_STRING: 2500
    },
    {
        FROM_TIME_STRING: 900,
        UNTIL_TIME_STRING: 2600 
    }
]

HOURS_ENTRY = [
    {
        DAY_OF_WEEK_STRING: "0",
        FROM_TIME_STRING: 80000,
        UNTIL_TIME_STRING: 250000
    },
    {
        DAY_OF_WEEK_STRING: "1",
        FROM_TIME_STRING: 90000,
        UNTIL_TIME_STRING: 260000 
    }
]

ROW_INDEX = 0
COLUMN_INDEX = 2
HOUR_FORMAT_FOR_UPDATE_ASSERT = "09:00:00"
FROM_HOUR_INT_FORMAT_FOR_CREATE_HOURS_ARRAY_ASSERT = 80000
UNTIL_HOUR_INT_FORMAT_FOR_CREATE_HOURS_ARRAY_ASSERT = 250000


PROFILE_ID = 1
PROFILE_ID_INVALID = 1000

def test_insert_select_operational_hours():
    local_logger.start(TEST_INSERT_SELECT_OPERATIONAL_HOURS_FUNCTION_NAME)
    OperationalHours.insert_operational_hours(connection, PROFILE_ID, HOURS1)
    hours = OperationalHours.read_operational_hours(connection, PROFILE_ID)
    assert(hours is not [])

    local_logger.end(TEST_INSERT_SELECT_OPERATIONAL_HOURS_FUNCTION_NAME)

def test_get_operational_hours_id():
    local_logger.start(TEST_GET_OPERATIONAL_HOURS_ID_FUNCTION_NAME)
    id_tuple = OperationalHours.get_operational_hours_id(connection, PROFILE_ID)
    assert(id is not None)

    local_logger.end(TEST_GET_OPERATIONAL_HOURS_ID_FUNCTION_NAME)

def test_get_operational_hours_ids():
    local_logger.start(TEST_GET_OPERATIONAL_HOURS_ID_FUNCTION_NAME)
    ids_tuples_list = OperationalHours.get_operational_hours_ids(connection, PROFILE_ID)
    assert(ids_tuples_list is not [])

    local_logger.end(TEST_GET_OPERATIONAL_HOURS_ID_FUNCTION_NAME)

def test_select_invalid_operational_hours():
    local_logger.start(TEST_SELECT_INVALID_OPERATIONAL_HOURS_FUNCTION_NAME)

    hours = OperationalHours.read_operational_hours(connection, PROFILE_ID_INVALID)
    assert(hours == [])

    local_logger.end(TEST_SELECT_INVALID_OPERATIONAL_HOURS_FUNCTION_NAME)

def test_update_operational_hours():
    local_logger.start(TEST_UPDATE_OPERATIONAL_HOURS_FUNCTION_NAME)

    OperationalHours.update_operational_hours(connection, PROFILE_ID, HOURS2)
    hours = OperationalHours.read_operational_hours(connection, PROFILE_ID)
    if hours is not []:
        assert(OperationalHours.timedelta_to_time_format(hours[ROW_INDEX][COLUMN_INDEX]) == HOUR_FORMAT_FOR_UPDATE_ASSERT)
    else:
        assert(False)

    local_logger.end(TEST_UPDATE_OPERATIONAL_HOURS_FUNCTION_NAME)

def test_delete_operational_hours():
    local_logger.start(TEST_DELETE_OPERATIONAL_HOURS_FUNCTION_NAME)
    
    OperationalHours.delete_operational_hours(connection, PROFILE_ID)
    time.sleep(1)
    hours = OperationalHours.read_operational_hours(connection, PROFILE_ID)
    assert(hours == [])

    local_logger.end(TEST_DELETE_OPERATIONAL_HOURS_FUNCTION_NAME)

def test_create_hours_array_operational_hours():
    local_logger.start(TEST_CREATE_HOURS_ARRAY_OPERATIONAL_HOURS_FUNCTION_NAME)

    created_hours = OperationalHours.create_hours_array(HOURS_ENTRY)
    assert(created_hours[ROW_INDEX] == {FROM_TIME_STRING: FROM_HOUR_INT_FORMAT_FOR_CREATE_HOURS_ARRAY_ASSERT, UNTIL_TIME_STRING: UNTIL_HOUR_INT_FORMAT_FOR_CREATE_HOURS_ARRAY_ASSERT})

    local_logger.end(TEST_CREATE_HOURS_ARRAY_OPERATIONAL_HOURS_FUNCTION_NAME)
