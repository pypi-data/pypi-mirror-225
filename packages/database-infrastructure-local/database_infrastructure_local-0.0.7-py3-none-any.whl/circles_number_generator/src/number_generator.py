from logger_local.LoggerComponentEnum import LoggerComponentEnum
import random 
import sys
from dotenv import load_dotenv
load_dotenv()
from circles_local_database_python.connection import Connection 
from logger_local.LoggerLocal import logger_local as logger


INIT_METHOD_NAME = "__init__"
GET_CONNECTION_METHOD_NAME = "get_connection"
GET_RANDOM_NUMBER_METHOD_NAME = "get_random_number"

CIRCLES_NUMBER_GENERATOR_COMPONENT_ID = 177
CIRCLES_NUMBER_GENERATOR_COMPONENT_NAME = "circles_number_generator/src/number_generator.py"

object_to_insert = {
    'component_id': CIRCLES_NUMBER_GENERATOR_COMPONENT_ID,
    'component_name': CIRCLES_NUMBER_GENERATOR_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'tal.g@circ.zone'
}

logger.init(object=object_to_insert)

class NumberGenerator:
    
    def __init__(self, schema, table):
        logger.start(INIT_METHOD_NAME)

        self.schema = schema
        self.table = table

        logger.end(INIT_METHOD_NAME)

    def get_connection(self):
        # Connect to the MySQL database
        logger.start(GET_CONNECTION_METHOD_NAME)

        database = Connection(self.schema)
        connection = database.connect()
        connection.database = self.schema 

        logger.end(GET_CONNECTION_METHOD_NAME)
        return connection

    def get_random_number(self):
        logger.start(GET_RANDOM_NUMBER_METHOD_NAME)
        
        logger.info("Starting random number generator...")
        connection = self.get_connection()
        cursor = connection.cursor()

        successful = False

        while not successful:
            number = random.randint(1, sys.maxsize)
            logger.info(object = {"Random number generated": str(number)})

            cursor.execute("SELECT id FROM %s.%s WHERE `number` = %s" % (self.schema, self.table, number))
            if cursor.fetchone() == None:
                successful = True
                logger.info("Number does not already exist in database")

        connection.close()
        logger.end(GET_RANDOM_NUMBER_METHOD_NAME, object = {"number" : number})
        return number 
