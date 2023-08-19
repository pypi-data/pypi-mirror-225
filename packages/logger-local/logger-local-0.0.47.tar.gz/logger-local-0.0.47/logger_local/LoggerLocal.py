import os
from functools import wraps
from logger_local.LoggerService import LoggerService
from logger_local.LoggerComponentEnum import LoggerComponentEnum

loggers={}
def logger(component_id:int,component_name:str,component_category:LoggerComponentEnum.ComponentCategory,developer_email:str):
    if(os.getenv("ENVIRONMENT") is None):
        raise Exception("please insert")
    if component_id in loggers:
        return loggers.get(component_id)
    else:
        logger=LoggerService()
        loggers[component_id]=logger
        logger_object={
            "component_id":component_id,
            "component_name":component_name,
            "component_category": component_category.value,
            "developer_email":developer_email       
        }
        logger.init(object=logger_object)
        return logger
    
def log_function_execution(func):
    @wraps(func)
    def wrapper(component_id,*args, **kwargs):
        logger_local=logger(component_id)
        object1 = {
            'args': str(args),
            'kawargs': str(kwargs),
        }
        logger_local.start(object=object1)
        result = func(*args, **kwargs)  # Execute the function
        object2 = {
            'result': result,
        }
        logger_local.end(object=object2)
        return result
    return wrapper