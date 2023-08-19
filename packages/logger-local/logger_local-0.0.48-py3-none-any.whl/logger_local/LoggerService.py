import sys
import traceback
from logger_local.MessageSeverity import MessageSeverity
from logger_local.Writer import Writer
import os
import json
import inspect
from logger_local.fields import Fields
from logger_local.Component import Component
from logger_local.SendToLogzIo import SendTOLogzIo

debug = os.getenv("debug")
logzio_token = os.getenv("LOGZIO_TOKEN")
logzio_url = "https://listener.logz.io:8071"
COMPUTER_LANGUAGE = "Python"


class LoggerService:

    def __init__(self):
        if (logzio_token is None):
            raise Exception(
                "Please set in your .env file LOGZIO_TOKEN=cXNHuVkkffkilnkKzZlWExECRlSKqopE")
        self.fields = {}
        self._writer = Writer()
        self.logzio_handler = SendTOLogzIo()
        self.writeToSql = False
        self.additinal_fields = {}

    def init(self, log_message=None, **kwargs):
        if debug:
            print(f'LoggerService.init(args= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            self.insertVariables(**kwargs)
            kwargs['object']['severity_id'] = MessageSeverity.Init.value
            kwargs['object']['severity_name'] = MessageSeverity.Init.name
            kwargs['object']['log_message'] = log_message
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            if self.writeToSql == True:
                self._writer.addMessageAndPayload(log_message, **kwargs)
            self.logzio_handler.send_to_logzio(kwargs['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.Init.value,
                    'severity_name': MessageSeverity.Init.name,
                }
                log_object['log_message'] = log_message
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_To_object(**kwargs)
                if self.writeToSql:
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    self.insertVariables(**kwargs)
                    kwargs['object']['severity_id'] = MessageSeverity.Init.value
                    kwargs['object']['severity_name'] = MessageSeverity.Init.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    if (self.writeToSql == True):
                        self._writer.add(**kwargs)
                    self.logzio_handler.send_to_logzio(kwargs['object'])

    def start(self, log_message=None, **kwargs):
        if debug:
            print(f'LoggerService.init(args= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Start.value
            kwargs['object']['severity_name'] = MessageSeverity.Start.name
            kwargs['object']['log_message'] = log_message
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self.insert_To_object(**kwargs)
            if self.writeToSql == True:
                self._writer.addMessageAndPayload(log_message, **kwargs)
            self.logzio_handler.send_to_logzio(kwargs['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.Start.value,
                    'severity_name': MessageSeverity.Start.name,
                }
                log_object['log_message'] = log_message
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_To_object(**kwargs)
                if self.writeToSql:
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Start.value
                    kwargs['object']['severity_name'] = MessageSeverity.Start.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_To_object(**kwargs)
                    if self.writeToSql == True:
                        self._writer.add(**kwargs)
                    self.logzio_handler.send_to_logzio(kwargs['object'])

    def end(self, log_message=None, **kwargs):
        if debug:
            print(f'LoggerService.init(args= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.End.value
            kwargs['object']['severity_name'] = MessageSeverity.End.name
            kwargs['object']['log_message'] = log_message
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self.insert_To_object(**kwargs)
            if self.writeToSql == True:
                self._writer.addMessageAndPayload(log_message, **kwargs)
            self.logzio_handler.send_to_logzio(kwargs['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.End.value,
                    'severity_name': MessageSeverity.End.name,
                }
                log_object['log_message'] = log_message
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_To_object(**kwargs)
                if self.writeToSql:
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.End.value
                    kwargs['object']['severity_name'] = MessageSeverity.End.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_To_object(**kwargs)
                    if self.writeToSql == True:
                        self._writer.add(**kwargs)
                    self.logzio_handler.send_to_logzio(kwargs['object'])

    def exception(self, log_message=None, **kwargs):
        if debug:
            print(f'LoggerService.init(args= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            stack_trace = traceback.format_exception(
                type(kwargs['object']), kwargs['object'], kwargs['object'].__traceback__)
            object_exp = {
                'severity_id': MessageSeverity.Exception.value,
                'severty_name': MessageSeverity.Exception.name,
                'error_stack': f'{str(stack_trace)}',
                'log_message': log_message
            }
            object_exp = self.insert_to_payload_extra_vars(object=object_exp)
            self.insert_To_object(**object_exp)
            if self.writeToSql == True:
                self._writer.addMessageAndPayload(log_message, **object_exp)
            self.logzio_handler.send_to_logzio(object_exp['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.Exception.value,
                    'severity_name': MessageSeverity.Exception.name,
                }
                log_object['log_message'] = log_message
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_To_object(**kwargs)
                if self.writeToSql:
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    stack_trace = traceback.format_exception(
                        type(kwargs['object']), kwargs['object'], kwargs['object'].__traceback__)
                    object_exp = {
                        'severity_id': MessageSeverity.Exception.value,
                        'severty_name': MessageSeverity.Exception.name,
                        'error_stack': f'{str(stack_trace)}'
                    }
                    object_exp = self.insert_to_payload_extra_vars(
                        object=object_exp)
                    self.insert_To_object(**object_exp)
                    if self.writeToSql == True:
                        self._writer.add(**object_exp)
                    self.logzio_handler.send_to_logzio(object_exp['object'])

    def info(self, log_message=None, **kwargs):
        if debug:
            print(f'LoggerService.init(message= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Information.value
            kwargs['object']['severity_name'] = MessageSeverity.Information.name
            kwargs['object']['log_message'] = log_message
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self.insert_To_object(**kwargs)
            if self.writeToSql == True:
                self._writer.addMessageAndPayload(log_message, **kwargs)
            self.logzio_handler.send_to_logzio(kwargs['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.Information.value,
                    'severity_name': MessageSeverity.Information.name,
                }
                log_object['log_message'] = log_message
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_To_object(**kwargs)
                if self.writeToSql:
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Information.value
                    kwargs['object']['severity_name'] = MessageSeverity.Information.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_To_object(**kwargs)
                    if self.writeToSql == True:
                        self._writer.add(**kwargs)
                    self.logzio_handler.send_to_logzio(kwargs['object'])

    def error(self, message=None, **kwargs):
        if debug:
            print(f'LoggerService.init(args= {message} kwargs= {kwargs})')
        if message and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Error.value
            kwargs['object']['severity_name'] = MessageSeverity.Error.name
            kwargs['object']['log_message'] = message
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self.insert_To_object(**kwargs)
            if self.writeToSql == True:
                self._writer.addMessageAndPayload(message, **kwargs)
            self.logzio_handler.send_to_logzio(kwargs['object'])
        else:
            if message:
                log_object = {
                    'severity_id': MessageSeverity.Error.value,
                    'severity_name': MessageSeverity.Error.name,
                }
                log_object['log_message'] = message
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_To_object(**kwargs)
                if self.writeToSql:
                    self._writer.addMessageAndPayload(message, **kwargs)
                self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Error.value
                    kwargs['object']['severity_name'] = MessageSeverity.Error.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_To_object(**kwargs)
                    if self.writeToSql == True:
                        self._writer.add(**kwargs)
                    self.logzio_handler.send_to_logzio(kwargs['object'])

    def warn(self, log_message=None, **kwargs):
        if debug:
            print(f'LoggerService.init(args= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Warning.value
            kwargs['object']['severity_name'] = MessageSeverity.Warning.name
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self.insert_To_object(**kwargs)
            if self.writeToSql == True:
                self._writer.addMessageAndPayload(log_message, **kwargs)
            self.logzio_handler.send_to_logzio(kwargs['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.Warning.value,
                    'severity_name': MessageSeverity.Warning.name,
                }
                log_object['log_message'] = log_message
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_To_object(**kwargs)
                if self.writeToSql:
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity. Warning.value
                    kwargs['object']['severity_name'] = MessageSeverity.Warning.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_To_object(**kwargs)
                    if self.writeToSql == True:
                        self._writer.add(**kwargs)
                    self.logzio_handler.send_to_logzio(kwargs['object'])

    def debug(self, log_message=None, **kwargs):
        if debug:
            print(f'LoggerService.init(args= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Debug.value
            kwargs['object']['severity_name'] = MessageSeverity.Debug.name
            kwargs['object']['log_message'] = log_message
            self.insert_To_object(**kwargs)
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            if self.writeToSql == True:
                self._writer.addMessageAndPayload(log_message, **kwargs)
            self.logzio_handler.send_to_logzio(kwargs['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.Debug.value,
                    'severity_name': MessageSeverity.Debug.name,
                }
                log_object['log_message'] = log_message
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_To_object(**kwargs)
                if self.writeToSql:
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Debug.value
                    kwargs['object']['severity_name'] = MessageSeverity.Debug.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_To_object(**kwargs)
                    if self.writeToSql == True:
                        self._writer.add(**kwargs)
                    self.logzio_handler.send_to_logzio(kwargs['object'])

    def critical(self, log_message=None, **kwargs):
        if debug:
            print(f'LoggerService.init(args= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Critical.value
            kwargs['object']['severity_name'] = MessageSeverity.Critical.name
            kwargs['object']['log_message'] = log_message
            self.insert_To_object(**kwargs)
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            if self.writeToSql == True:
                self._writer.addMessageAndPayload(log_message, **kwargs)
            self.logzio_handler.send_to_logzio(kwargs['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.Critical.value,
                    'severity_name': MessageSeverity.Critical.name,
                }
                log_object['log_message'] = log_message
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_To_object(**kwargs)
                if self.writeToSql:
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Critical.value
                    kwargs['object']['severity_name'] = MessageSeverity.Critical.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_To_object(**kwargs)
                    if self.writeToSql == True:
                        self._writer.add(**kwargs)
                    self.logzio_handler.send_to_logzio(kwargs['object'])

    def verbose(self, log_message=None, **kwargs):
        if debug:
            print(f'LoggerService.init(args= {log_message} kwargs= {kwargs})')
        if log_message and 'object' in kwargs:
            kwargs['object']['severity_id'] = MessageSeverity.Verbose.value
            kwargs['object']['severity_name'] = MessageSeverity.Verbose.name
            kwargs['object']['log_message'] = log_message
            kwargs = self.insert_to_payload_extra_vars(**kwargs)
            self.insert_To_object(**kwargs)
            if self.writeToSql == True:
                self._writer.addMessageAndPayload(log_message, **kwargs)
            self.logzio_handler.send_to_logzio(kwargs['object'])
        else:
            if log_message:
                log_object = {
                    'severity_id': MessageSeverity.Verbose.value,
                    'severity_name': MessageSeverity.Verbose.name,
                }
                log_object['log_message'] = log_message
                kwargs['object'] = log_object
                kwargs = self.insert_to_payload_extra_vars(**kwargs)
                self.insert_To_object(**kwargs)
                if self.writeToSql:
                    self._writer.addMessageAndPayload(log_message, **kwargs)
                self.logzio_handler.send_to_logzio(kwargs['object'])
            else:
                if 'object' in kwargs:
                    kwargs['object']['severity_id'] = MessageSeverity.Verbose.value
                    kwargs['object']['severity_name'] = MessageSeverity.Verbose.name
                    kwargs = self.insert_to_payload_extra_vars(**kwargs)
                    self.insert_To_object(**kwargs)
                    if self.writeToSql == True:
                        self._writer.add(**kwargs)
                    self.logzio_handler.send_to_logzio(kwargs['object'])

    def insertVariables(self, **object):
        object_data = object.get("object", {})
        for field in self.fields.keys():
            if field in object_data.keys():
                self.fields[field] = object_data[field]
        for field in object_data.keys():
            if field not in self.fields:
                self.additinal_fields[field] = object_data.get(field)

    def insert_To_object(self, **kwargs):
        object_data = kwargs.get("object", {})
        for field in self.fields.keys():
            if field not in object_data:
                field_value = self.fields[field]
                if field_value is not None:
                    object_data[field] = field_value

    def get_logger_table_fields(self):
        if (self.writeToSql is True):
            fields = Fields.getFieldsSingelton()
            for field in fields:
                self.fields[field] = None
        return self.fields

    def clean_variables(self):
        for field in self.fields:
            self.fields[field] = None
        self.additinal_fields.clear()

    def insert_to_payload_extra_vars(self, **kwargs):
        message = kwargs['object'].pop('message', None)
        kwargs['object']['function'] = self.get_current_function_name()
        kwargs['object']['environment'] = os.getenv("ENVIRONMENT")
        kwargs['object']['class'] = self.get_calling_class()
        kwargs['object']['line_number'] = self.get_calling_line_number()
        kwargs['object']['computer_language'] = COMPUTER_LANGUAGE
        for field in self.fields.keys():
            if field not in kwargs['object']:
                field_value = self.fields[field]
                if field_value is not None:
                    kwargs['object'][field] = field_value
        for field in self.additinal_fields.keys():
            if field not in kwargs['object']:
                field_value = self.additinal_fields[field]
                kwargs['object'][field] = field_value
        if (self.writeToSql is True and 'component_id' in kwargs['object'] and 'component_name' not in kwargs['object']):
            component_info = self.get_component_info(
                kwargs['object']['component_id'])
            if (component_info):
                for field in component_info.keys():
                    if (field not in kwargs['object']):
                        field_value = component_info[field]
                        if field_value is not None:
                            kwargs['object'][field] = field_value
        if message is not None:
            kwargs['object']['message'] = message
        object_data = kwargs.get("object", {})
        object_data_payload = {key: value for key,
                               value in object_data.items()}
        object_data_record_json = json.dumps(object_data_payload)
        object_data["record"] = object_data_record_json
        if self.writeToSql:
            object_data = {key: value for key,
                       value in object_data.items() if key in self.fields.keys()}
            kwargs["object"] = object_data

        return kwargs

    def get_current_function_name(self):
        stack = inspect.stack()
        caller_frame = stack[3]
        function_name = caller_frame.function
        return function_name

    def get_calling_class(self):
        stack = inspect.stack()
        calling_module = inspect.getmodule(stack[3].frame)
        return calling_module.__name__

    def get_calling_line_number(self):
        stack = inspect.stack()
        calling_frame = stack[3]
        line_number = calling_frame.lineno
        return line_number


    def get_component_info(self, component_id):
        result = Component.getDetailsByComponentId(component_id)
        if result:
            name, component_type, component_category, testing_framework, api_type = result
            component_info = {
                'component_name': name,
                'component_type': component_type,
                'component_category': component_category,
                'testing_framework': testing_framework,
                'api_type': api_type
            }
            for field in component_info.keys():
                self.fields[field] = component_info[field]
            return component_info
        else:
            return None

    def isComponentComplete(self):
        return getattr(self, 'component_name') is None or getattr(self, 'component_type') is None or getattr(self, 'component_category') is None or getattr(self, 'testing_framework') is None or getattr(self, 'api_type') is None

    def setWriteToSql(self, value):
        self.writeToSql = value
        if (self.writeToSql is True):
            self.get_logger_table_fields()

    def sql(self):
        try:
            con = self._writer.get_connection()
            cursor = con.cursor()
            sql_query = f"DESCRIBE logger.logger_table"
            cursor.execute(sql_query)
            columns_info = cursor.fetchall()
            columns = [column[0] for column in columns_info]
            return columns
        except Exception as e:
            print("logger-local-python-package LoggerService.py sql(self) Exception catched SQL=" +
                  sql_query+" Exception=" + str(e), file=sys.stderr)
            return None
    


