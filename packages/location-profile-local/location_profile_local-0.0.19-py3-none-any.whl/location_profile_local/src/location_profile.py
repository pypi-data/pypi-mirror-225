from logger_local.LoggerLocal import logger_local as logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.connection import Connection
from circles_local_database_python.generic_crud import GenericCRUD

GET_LOCATION_ID_BY_PROFILE_ID_METHOD_NAME = "LocationProfile.get_location_id_by_profile_id()"

LOCATION_PROFILE_LOCAL_COMPONENT_ID = 167
COMPONENT_NAME = 'location_profile_local/location_profile.py'

object_to_insert = {
    'payload': 'method get_location_id_by_profile_id in location-profile-local',
    'component_id': LOCATION_PROFILE_LOCAL_COMPONENT_ID,
    'component_name': COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,
    'developer_email': 'tal.g@circ.zone'
}

logger.init(object=object_to_insert)

database = Connection("location_profile")

class LocationProfile(GenericCRUD):

    @staticmethod
    def get_location_id_by_profile_id(profile_id: int) -> int:
        logger.start(GET_LOCATION_ID_BY_PROFILE_ID_METHOD_NAME, object={'profile_id': profile_id})
        connection = database.connect()
        cursor = connection.cursor()
  
        logger.info(object={'profile_id':profile_id})
        query_get = "SELECT location_id FROM location_profile.location_profile_view WHERE profile_id=%s"
        cursor.execute(query_get, (profile_id,))
        rows = cursor.fetchall()
        location_id = None
        if len(rows) > 0:
            location_id, = rows[0]

        connection.commit()
        connection.close()

        logger.end(GET_LOCATION_ID_BY_PROFILE_ID_METHOD_NAME, object={'location_id':location_id})
        return location_id