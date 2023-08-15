from logger_local.LoggerComponentEnum import LoggerComponentEnum
import datetime
from dotenv import load_dotenv

load_dotenv()
from location_profile_local.location_profile import LocationProfile
from logger_local.LoggerLocal import logger_local as local_logger


INSERT_OPERATIONAL_HOURS_METHOD_NAME = "insert_operational_hours"
UPDATE_OPERATIONAL_HOURS_METHOD_NAME = "update_operational_hours"
READ_OPERATIONAL_HOURS_METHOD_NAME = "read_operational_hours"
DELETE_OPERATIONAL_HOURS_METHOD_NAME = "delete_operational_hours"
GET_OPERATIONAL_HOURS_ID_METHOD_NAME = "get_operational_hours_id"
GET_OPERATIONAL_HOURS_IDS_METHOD_NAME = "get_operational_hours_ids"
CREATE_HOURS_ARRAY_METHOD_NAME = "create_hours_array"
TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME = "timedelta_to_time_format"
OPERATIONAL_HOURS_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = 158 
OPERATIONAL_HOURS_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = 'operational_hours_local/operational_hours.py'

object_to_insert = {
    'payload': 'method get_location_id_by_profile_id in location-profile-local',
    'component_id': OPERATIONAL_HOURS_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': OPERATIONAL_HOURS_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
    'developer_email': 'tal.g@circ.zone'
}

local_logger.init(object=object_to_insert)


#OperationalHours class provides methods for all the CRUD operations to the operational_hours db
class OperationalHours:
  
  def __init__(self):
      pass
  
  @staticmethod
  def insert_operational_hours(connection, profile_id, hours):
      local_logger.start(INSERT_OPERATIONAL_HOURS_METHOD_NAME)

      location_id = LocationProfile.get_location_id_by_profile_id(connection, profile_id)
      for index, day in enumerate(hours):
        query_insert = "INSERT INTO operational_hours.operational_hours_table(profile_id, location_id, day_of_week, from_time, until_time) VALUES (%s, %s, %s, %s, %s)"
        local_logger.info(object={'query_insert':query_insert})
        local_logger.info(object={'query_parameters':(profile_id, int(location_id[0]), index, day["from_time"], day["until_time"])})
        connection.execute(query_insert, (profile_id, location_id[0], index, day["from_time"], day["until_time"]))
        local_logger.info("executed query insert")
      
      local_logger.end(INSERT_OPERATIONAL_HOURS_METHOD_NAME)

  @staticmethod
  def update_operational_hours(connection, profile_id, hours):
      local_logger.start(UPDATE_OPERATIONAL_HOURS_METHOD_NAME)

      ids = OperationalHours.get_operational_hours_ids(connection, profile_id)
      for index, day in enumerate(hours):
        tup = ids[index]
        id = int(tup[0])
        query_update = "UPDATE operational_hours.operational_hours_table SET day_of_week = %s, from_time = %s, until_time = %s WHERE operational_hours_id = %s"
        connection.execute(query_update, (index, day["from_time"], day["until_time"], id))

      local_logger.end(UPDATE_OPERATIONAL_HOURS_METHOD_NAME)

  @staticmethod
  def read_operational_hours(connection, profile_id):
      local_logger.start(READ_OPERATIONAL_HOURS_METHOD_NAME)

      now = datetime.datetime.now()
      query_get = "SELECT operational_hours_id, day_of_week, from_time, until_time FROM operational_hours.operational_hours_view WHERE profile_id = %s AND start_timestamp <= %s AND (end_timestamp >= %s OR end_timestamp IS NULL)"
      result = connection.fetchall(query_get, (profile_id, now, now))

      local_logger.end(READ_OPERATIONAL_HOURS_METHOD_NAME)
      return result

  @staticmethod
  def delete_operational_hours(connection, profile_id):
      local_logger.start(DELETE_OPERATIONAL_HOURS_METHOD_NAME)

      ids = OperationalHours.get_operational_hours_ids(connection, profile_id)
      for tuple in ids:
        id = tuple[0]
        now = datetime.datetime.now()

        query_update = "UPDATE operational_hours.operational_hours_table SET end_timestamp = %s WHERE operational_hours_id = %s"
        connection.execute(query_update, (now, id))

      local_logger.end(DELETE_OPERATIONAL_HOURS_METHOD_NAME)

  @staticmethod
  def get_operational_hours_id(connection, profile_id):
    local_logger.start(GET_OPERATIONAL_HOURS_ID_METHOD_NAME)

    query_get = "SELECT operational_hours_id FROM operational_hours.operational_hours_view WHERE profile_id = %s AND start_timestamp <= %s AND (end_timestamp >= %s OR end_timestamp IS NULL)"
    now = datetime.datetime.now()
    hours_id = connection.fetchone(query_get, (profile_id, now, now))

    local_logger.end(GET_OPERATIONAL_HOURS_ID_METHOD_NAME)
    return hours_id

  @staticmethod
  def get_operational_hours_ids(connection, profile_id):
    local_logger.start(GET_OPERATIONAL_HOURS_IDS_METHOD_NAME)

    query_get = "SELECT operational_hours_id FROM operational_hours.operational_hours_view WHERE profile_id = %s AND start_timestamp <= %s AND (end_timestamp >= %s OR end_timestamp IS NULL)"
    now = datetime.datetime.now()
    hours_ids = connection.fetchall(query_get, (profile_id, now, now))

    local_logger.end(GET_OPERATIONAL_HOURS_IDS_METHOD_NAME)
    return hours_ids

  '''
  There may be a problem, if for example there's hour1 = {"day_of_week" : 2, "from": 8:00, "until": 12:00} and hour2 = {"day_of_week": 2, "from": 15:00, "until": 20:00}
  (A business closed between 12:00 and 15:00) then hour2 will override hour1 in operational_hours = {}.
  '''
  @staticmethod
  def create_hours_array(days_collection):
    local_logger.start(CREATE_HOURS_ARRAY_METHOD_NAME)

    operational_hours = {}
    for day in days_collection:
        day_of_week = day.get("day_of_week", None)
        local_logger.info(object={'day_of_week':day_of_week})
        operational_hours[int(day_of_week)] = {
            "from_time": day.get("from_time", None),
            "until_time": day.get("until_time", None)
        }

    local_logger.end(CREATE_HOURS_ARRAY_METHOD_NAME)
    return operational_hours
  
  @staticmethod
  def timedelta_to_time_format(timedelta):
    local_logger.start(TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME)
    # Calculate the total seconds and convert to HH:MM:SS format
    total_seconds = int(timedelta.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Format as "HH:MM:SS"
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    local_logger.end(TIMEDELTA_TO_TIME_FORMAT_METHOD_NAME)
    return formatted_time







  
