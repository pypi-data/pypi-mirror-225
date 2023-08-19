from datetime import datetime
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..')
sys.path.append(src_path)
from dotenv import load_dotenv
from logger_local.LoggerComponentEnum import LoggerComponentEnum
import pymysql
import traceback
import re
from logger_local.MessageSeverity import MessageSeverity
from logger_local.LoggerLocal import logger




load_dotenv()
logger_local=logger(component_id=102,component_name="logger local",component_category=LoggerComponentEnum.ComponentCategory.Unit_Test,developer_email="idan.a@circ.zone")
logger_local.setWriteToSql(True)
ID = 5000001
LOGGER_COMPONENT_ID = 102
COMPONENT_NAME = "Logger Python"
object_to_initlize = {
    'client_ip_v4': 'ipv4-py',
    'client_ip_v4': 'ipv4-py',
    'client_ip_v6': 'ipv6-py',
    'latitude': 33,
    'longitude': 35,
    'user_id': ID,
    'profile_id': ID,
    'activity': 'test from python',
    'activity_id': ID,
    'payload': 'log from python -object_1',
    'component_id': LOGGER_COMPONENT_ID,
    'variable_id': ID,
    'variable_value_old': 'variable_value_old-python',
    'variable_value_new': 'variable_value_new-python',
    'created_user_id': ID,
    'updated_user_id': ID,

}
logger_local.init(object=object_to_initlize)


# Connect to the datbaase to validat that the log was inserted
def get_connection() -> pymysql.connections.Connection:
    return pymysql.connect(
        host=os.getenv('RDS_HOSTNAME'),
        user=os.getenv('RDS_USERNAME'),
        password=os.getenv('RDS_PASSWORD'),
        database='logger'  # os.getenv('RDS_DB_NAME')
    )


def test_log_with_only_logger_object():
    object_to_insert_1 = {
        'payload': 'log from python -object_1 check',
    }
    logger_local.info(object=object_to_insert_1)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = '{object_to_insert_1['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Information.value


def test_error_with_only_logger_object():
    object_to_insert_2 = {
        'payload': 'payload from error python -object_2',
    }
    logger_local.error(object=object_to_insert_2)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = '{object_to_insert_2['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Error.value


def test_verbose_with_only_logger_object():
    object_to_insert_3 = {
        'client_ip_v4': 'ipv4-py',
        'client_ip_v6': 'ipv6-py',
        'latitude': 32,
        'longitude': 35,
        'variable_id': ID,
        'variable_value_old': 'variable_value_old-python-object_3',
        'variable_value_new': 'variable_value_new-python',
    }
    logger_local.verbose(object=object_to_insert_3)

    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE variable_value_old = '{object_to_insert_3['variable_value_old']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Verbose.value


def test_warn_with_only_logger_object():
    object_to_insert_4 = {
        'client_ip_v4': 'ipv4-py',
        'client_ip_v6': 'ipv6-py',
        'latitude': 32,
        'longitude': 35,
        'activity': 'test from python',
        'activity_id': ID,
        'payload': 'payload from python -object_4',
        'variable_value_new': 'variable_value_new-python',
        'created_user_id': ID,
        'updated_user_id': ID
    }
    logger_local.warn(object=object_to_insert_4)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = '{object_to_insert_4['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Warning.value


def test_add_message():
    # option to insert only message
    message = 'only message error from python'
    logger_local.error(message)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE message = '{message}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Error.value


def test_debug_with_only_logger_object():
    object_to_insert5 = {
        'payload': "Test python!!! check for debug insert"
    }
    logger_local.debug(object=object_to_insert5)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = '{object_to_insert5['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Debug.value


def test_start_with_only_logger_object():
    object_to_insert6 = {
        'payload': "Test python!!! check for start insert"
    }
    logger_local.start(object=object_to_insert6)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = '{object_to_insert6['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Start.value


def test_end_with_only_logger_object():
    object_to_insert7 = {
        'payload': "Test python!!! check for end insert",
    }
    logger_local.end(object=object_to_insert7)

    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE payload = '{object_to_insert7['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.End.value


def test_init_with_only_logger_object():
    logger_local.init("Test python!!! check for init insert")
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id FROM logger.logger_table WHERE message = 'Test python!!! check for init insert' ORDER BY timestamp DESC LIMIT 1;"""
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Init.value


def test_exception_with_only_logger_object():
    try:
        x = 5 / 0
    except Exception as e:
        logger_local.exception(object=e)
        stack_trace = str(traceback.format_exception(
            type(e), e, e.__traceback__))

    conn = get_connection()
    cursor = conn.cursor()

    escaped_stack_trace = re.escape(stack_trace)
    pattern = f"%{escaped_stack_trace}%"
    sql = "SELECT severity_id FROM logger.logger_table WHERE error_stack LIKE %s ORDER BY timestamp DESC LIMIT 1;"
    cursor.execute(sql, (pattern,))

    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Exception.value


def test_error():
    object_to_insert9 = {
        'payload': 'payload from error python -object_9'

    }
    msg = "check for error with both object and message"
    logger_local.error(msg, object=object_to_insert9)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id,message FROM logger.logger_table WHERE payload = '{object_to_insert9['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)

    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Error.value
    assert result[1] == msg


def test_start():
    object_to_insert10 = {
        'payload': 'payload from start python -object_10'

    }
    msg = "check for start with both object and message"
    logger_local.start(msg, object=object_to_insert10)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id,message FROM logger.logger_table WHERE payload = '{object_to_insert10['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)

    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Start.value
    assert result[1] == msg


def test_End():
    object_to_insert11 = {
        'payload': 'payload from end python -object_11'

    }
    msg = "check for end with both object and message"
    logger_local.end(msg, object=object_to_insert11)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id,message FROM logger.logger_table WHERE payload = '{object_to_insert11['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)

    result = cursor.fetchone()
    assert result[0] == MessageSeverity.End.value
    assert result[1] == msg


def test_debug():
    object_to_insert12 = {
        'payload': 'payload from debug python -object_12'

    }
    msg = "check for debug with both object and message"
    logger_local.debug(msg, object=object_to_insert12)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id,message FROM logger.logger_table WHERE payload = '{object_to_insert12['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)

    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Debug.value
    assert result[1] == msg


def test_log():
    object_to_insert13 = {
        'payload': 'payload from info python -object_13'

    }
    msg = "check for info with both object and message"
    logger_local.info(msg, object=object_to_insert13)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id,message FROM logger.logger_table WHERE payload = '{object_to_insert13['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)

    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Information.value
    assert result[1] == msg


def test_Init():
    object_to_insert14 = {
        'payload': 'payload from init python -object_14'

    }
    msg = "check for init with both object and message"
    logger_local.init(msg, object=object_to_insert14)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT severity_id,message FROM logger.logger_table WHERE payload = '{object_to_insert14['payload']}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)

    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Init.value
    assert result[1] == msg


def test_Exception():
    try:
        x = 5 / None
    except Exception as e:
        logger_local.exception("exception check", object=e)
        stack_trace = str(traceback.format_exception(
            type(e), e, e.__traceback__))
    conn = get_connection()
    cursor = conn.cursor()

    escaped_stack_trace = re.escape(stack_trace)
    pattern = f"%{escaped_stack_trace}%"
    sql = "SELECT severity_id,message FROM logger.logger_table WHERE error_stack LIKE %s ORDER BY timestamp DESC LIMIT 1;"
    cursor.execute(sql, (pattern,))
    result = cursor.fetchone()
    assert result[0] == MessageSeverity.Exception.value
    assert result[1] == "exception check"


def test_check_Function():
    logger_local.clean_variables()
    object_to_insert15 = {
        'payload': "check python",
        'component_id': LOGGER_COMPONENT_ID,
        'a': 5,
        'b': 6,
    }
    logger_local.start(object=object_to_insert15)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT component_id FROM logger.logger_table WHERE record = '{'{"payload": "check python", "component_id": 102, "a": 5, "b": 6, "severity_id": 400, "severity_name": "Start", "function": "test_check_Function", "environment": "play1", "class": "test_writer", "line_number": 353, "computer_language": "Python", "component_name": "Logger Python"}'}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == LOGGER_COMPONENT_ID
    object_to_insert16 = {
        'component_id': LOGGER_COMPONENT_ID,
        'payload': "check python",
        'return': 9,
    }
    logger_local.end(object=object_to_insert16)
    sql = f"""SELECT component_id FROM logger.logger_table WHERE record = '{'{"component_id": 102, "payload": "check python", "return": 9, "severity_id": 400, "severity_name": "End", "function": "test_check_Function", "environment": "play1", "class": "test_writer", "line_number": 365, "computer_language": "Python", "component_name": "Logger Python"}'}' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == LOGGER_COMPONENT_ID


def test_check_Init_compoent_enum():
    logger_local.clean_variables()
    object_to_insert17 = {
        'payload': "check python init with component",
        'component_id': LOGGER_COMPONENT_ID,
        'component_name': COMPONENT_NAME,
        "component_category": LoggerComponentEnum.ComponentCategory.Unit_Test.value,
        'testing_framework': LoggerComponentEnum.testingFramework.pytest.value,

    }
    logger_local.init(object=object_to_insert17)
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"""SELECT component_name,component_category,testing_framework FROM logger.logger_table WHERE payload="check python init with component" ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == COMPONENT_NAME
    assert result[1] == LoggerComponentEnum.ComponentCategory.Unit_Test.value
    assert result[2] == LoggerComponentEnum.testingFramework.pytest.value
    logger_local.info("check if component saved")
    sql = f"""SELECT component_name,component_category,testing_framework FROM logger.logger_table WHERE message = 'check if component saved' ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql)
    result = cursor.fetchone()
    assert result[0] == COMPONENT_NAME
    assert result[1] == LoggerComponentEnum.ComponentCategory.Unit_Test.value
    assert result[2] == LoggerComponentEnum.testingFramework.pytest.value
def test_check_Init_two_different_loggers():
    logger1=logger(component_id=101,component_name="check",component_category=LoggerComponentEnum.ComponentCategory.Unit_Test,developer_email="idan.a@circ.zone")
    logger2=logger(component_id=111,component_name="check2",component_category=LoggerComponentEnum.ComponentCategory.Unit_Test,developer_email="idan.a@circ.zone")
    logger1.setWriteToSql(True)
    logger2.setWriteToSql(True)
    msg1="check logger 1"+str(datetime.now())
    logger1.info(msg1)
    msg2="check logger 2"+str(datetime.now())
    logger2.info(msg2)
    conn = get_connection()
    cursor = conn.cursor()
    sql = """SELECT component_id FROM logger.logger_table WHERE message=%s ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql,(msg1))
    comp1 = cursor.fetchone()[0]
    cursor = conn.cursor()
    sql = """SELECT component_id FROM logger.logger_table WHERE message=%s ORDER BY timestamp DESC LIMIT 1;"""
    cursor.execute(sql,(msg2))
    comp2 = cursor.fetchone()[0]
    assert comp1==101
    assert comp2==111
    
