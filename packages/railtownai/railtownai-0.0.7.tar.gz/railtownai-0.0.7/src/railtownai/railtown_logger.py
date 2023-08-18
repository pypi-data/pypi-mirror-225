import urllib.request as request

# import urllib.parse as parse
import os
import json
import datetime
import traceback
import sys
import logging
from types import TracebackType
import re


class RailtownLogger:
    no_exception = True

    """Send easy log and stacktrace to railtown!-GS"""

    def __init__(
        self,
        no_exception: bool = True,
        RAILTOWN_LOGGING_URL: str = "",
        RAILTOWN_AUTHENTICATION_CODE: str = "",
        RAILTOWN_ENVIRONMENT_ID: str = "",
        RAILTOWN_ORGANIZATION_ID: str = "",
        RAILTOWN_PROJECT_ID: str = "",
        RAILTOWN_CONNECTION_NAME: str = "",
    ) -> None:
        """New log forwarding terminal
        @param `no_exception:bool` if True RailtownLogger will not manually raise any exception/error/warning but returned as string, this prevents infinite loop to appear. One must manually check output != str
        @param `RAILTOWN_LOGGING_URL:str` the url of the Railtown terminal to send, in empty, will attempt to pull from environmental variable
        @param `RAILTOWN_AUTHENTICATION_CODE:str` the token to use for request
        @param `language:str` specify the language of the error message, defaults to python
        """
        try:
            logging.basicConfig()
            self.logger = logging.getLogger(__name__)
            self.no_exception = no_exception
            self.RAILTOWN_LOGGING_URL = (
                RAILTOWN_LOGGING_URL if RAILTOWN_LOGGING_URL else os.environ.get("RAILTOWN_LOGGING_URL")
            )
            self.RAILTOWN_AUTHENTICATION_CODE = (
                RAILTOWN_AUTHENTICATION_CODE
                if RAILTOWN_AUTHENTICATION_CODE
                else os.environ.get("RAILTOWN_AUTHENTICATION_CODE")
            )
            self.RAILTOWN_ENVIRONMENT_ID = (
                RAILTOWN_ENVIRONMENT_ID if RAILTOWN_ENVIRONMENT_ID else os.environ.get("RAILTOWN_ENVIRONMENT_ID")
            )
            self.RAILTOWN_ORGANIZATION_ID = (
                RAILTOWN_ORGANIZATION_ID if RAILTOWN_ORGANIZATION_ID else os.environ.get("RAILTOWN_ORGANIZATION_ID")
            )
            self.RAILTOWN_PROJECT_ID = (
                RAILTOWN_PROJECT_ID if RAILTOWN_PROJECT_ID else os.environ.get("RAILTOWN_PROJECT_ID")
            )
            self.RAILTOWN_CONNECTION_NAME = (
                RAILTOWN_CONNECTION_NAME if RAILTOWN_CONNECTION_NAME else os.environ.get("RAILTOWN_CONNECTION_NAME")
            )
        except Exception as err:
            error_message = err.__str__()
            if e := self._internal_exception(error_message, AttributeError):
                return e

    def simple_init(self, no_exception: bool = True, RAILTOWN_REST_STRING=""):
        """New log forwarding terminal
        @param `no_exception:bool` if True RailtownLogger will not manually raise any exception/error/warning but returned as string, this prevents infinite loop to appear. One must manually check output != str
        @param `RAILTOWN_REST_STRING:str|list|list` auto config all fields __init__ will need, attempt fetch if not provided
          obtain string: go to overwatch->project->SETTINGS->Configure Project->Logs-></> configure instructions fro your selected environment->REST->copy and use as input, copy including //post
        @return new object
        """
        if not RAILTOWN_REST_STRING:
            RAILTOWN_REST_STRING = os.environ.get("RAILTOWN_REST_STRING")
        if not RAILTOWN_REST_STRING:
            error_message = "RAILTOWN_REST_STRING not configured"
            if e := self._internal_exception(error_message, AttributeError):
                return e
        parsed_data = str(RAILTOWN_REST_STRING).split("\\n", 2)
        a = parsed_data[-1].replace("\\n", "")
        data = json.loads(parsed_data[-1].replace("\n", ""))

        result = {}

        body = json.loads(data["Body"])
        result["RAILTOWN_ORGANIZATION_ID"] = body["OrganizationId"]
        result["RAILTOWN_ENVIRONMENT_ID"] = body["EnvironmentId"]
        result["RAILTOWN_PROJECT_ID"] = body["ProjectId"]

        result["RAILTOWN_AUTHENTICATION_CODE"] = data["UserProperties"]["AuthenticationCode"]
        result["RAILTOWN_CONNECTION_NAME"] = data["UserProperties"]["ConnectionName"]
        result["RAILTOWN_LOGGING_URL"] = data[0][8:]

        # self.__init__(no_exception)
        return result

    def _internal_exception(self, exception_message: str, exception_type=Exception):
        """Depend on no_exception, log and process exception"""
        self.logger.exception(exception_message)
        if self.no_exception:
            return exception_message
        else:
            raise exception_type(exception_message)

    def exception(self, error=None) -> dict:
        """send a log to railtown as exception
        ! Will need networking to function
        @param `error:str|tuple|list|Exception|None` the error stacktrace
            if not provided: will attempt to pull last exception through sys.exc_info()
            if str: use as log body (parsed, to display), no log name or raw log will be attached
            if tuple|list: then
                if size >= 1 and [0] == error object, [1] as log message, [2] as raw log
                if size == 3 and [0] == type(BaseException): [1] will be exception object and [2] will be trace back traceback (match output from sys.exc_info()), can be used for easy hooking
                if size == 3 and [0] == str: !take output from other railtown service, should not be used otherwise [0] will be used as formatted log body, [1] as log name, [2] as raw log
            if Exception: will attempt to read Exception content with traceback library
        @return `:dict` parsed response body from the request to Railtown
        """

        def parse_log(stacktrace: Exception) -> str:
            """Parse a stacktrace to Railtown python stacktrace format"""
            parsed_log = []
            formatted_log = ""
            formatted_log += f"{type(stacktrace).__name__}: {error.__str__()}\n"
            for file_name, line_number, function_name, _ in traceback.extract_tb(stacktrace.__traceback__):
                parsed_log.append({"file": file_name, "line": line_number, "function": function_name})
                formatted_log += f"\tat {function_name} ({file_name}:{line_number})\n"
            parsed_log.reverse()
            return str(formatted_log)

        """
        log body: the parsed log body to display
        log name: the error name of the stacktrace or meaningful information to display
        raw log: the complete log message, stored as reference and can be viewed
        """
        if error == None:
            parsed_log = parse_log(sys.exc_info()[1])
            log_name = sys.exc_info()[0].__name__ + ": " + str(sys.exc_info()[1])
            raw_log = "".join(traceback.format_exception(*sys.exc_info()))
        elif isinstance(error, str):
            parsed_log = parse_log(*sys.exc_info()[1])
            log_name = error
            #!
            raw_log = "".join(traceback.format_exception(*sys.exc_info()))
        elif isinstance(error, tuple) or isinstance(error, list):
            if isinstance(error[0], str):
                # [0] error body, [1] error message
                if len(error) != 2:
                    error_message = "Not a supported error format: when [0] == railtown_formatted_traceback:str, [1][2] must be error_message:str and raw_traceback:str"
                    if e := self._internal_exception(error_message, AttributeError):
                        return e
                parsed_log = error[0]
                if isinstance(error[1], str):
                    log_name = error[1]
                else:
                    error_message = "Not a supported error format: [1] bad str: error message"
                    if e := self._internal_exception(error_message, AttributeError):
                        return e
                if isinstance(error[2], str):
                    log_name = error[2]
                else:
                    error_message = "Not a supported error format: [0] bad str: raw stacktrace"
                    if e := self._internal_exception(error_message, AttributeError):
                        return e
            if isinstance(error[0], type):
                if len(error) != 3:
                    error_message = "Not a supported error format: when [0] == ExceptionType, [1][2] must be exception object and traceback"
                    if e := self._internal_exception(error_message, AttributeError):
                        return e
                # log name parse
                if isinstance(error[1], BaseException):
                    pass
                else:
                    error_message = "Not a supported error format: [1] bad BaseException"
                    if e := self._internal_exception(error_message, AttributeError):
                        return e
                # raw log parse
                if isinstance(error[2], TracebackType):
                    pass
                else:
                    error_message = "Not a supported error format: [2] bad traceback"
                    if e := self._internal_exception(error_message, AttributeError):
                        return e

                parsed_log = parse_log(error[1])
                log_name = type(error[1]).__name__ + ": " + str(error[1])
                raw_log = "".join(traceback.format_exception(type(error[1]), error[1], error[1].__traceback__))
            elif isinstance(error[0], Exception):
                parsed_log = parse_log(error[0])
                log_name = error[1] if len(error) >= 2 else type(error[0]).__name__ + ": " + str(error[0])
                raw_log = "".join(traceback.format_exception(type(error[0]), error[0], error[0].__traceback__))
            else:
                error_message = "Not a supported error format: Not a supported Tuple format"
                if e := self._internal_exception(error_message, AttributeError):
                    return e
        elif isinstance(error, Exception):
            parsed_log = parse_log(error)
            log_name = type(error).__name__ + ": " + str(error)
            raw_log = "".join(traceback.format_exception(type(error), error, error.__traceback__))

        else:
            error_message = "Not a supported error format"
            if e := self._internal_exception(error_message, AttributeError):
                return e

        # validate request parameters
        try:
            assert isinstance(parsed_log, str)
            assert isinstance(log_name, str)
            assert isinstance(raw_log, str)
            assert len(parsed_log) >= 1
        except Exception as err:
            error_message = "Not a supported data format: not valid log data" + err.__str__()
            if e := self._internal_exception(error_message + err.__str__(), AttributeError):
                return e

        data = [
            {
                "Body": str(
                    {
                        "EnvironmentId": self.RAILTOWN_ENVIRONMENT_ID,
                        "OrganizationId": self.RAILTOWN_ORGANIZATION_ID,
                        "ProjectId": self.RAILTOWN_PROJECT_ID,
                        "Runtime": "python",
                        "Properties": {"full_stack": raw_log},
                        "TimeStamp": str(datetime.datetime.utcnow().isoformat()),
                        "Message": log_name,
                        "Exception": parsed_log,
                        "Level": 4,
                    }
                ),
                "UserProperties": {
                    "Encoding": "utf-8",
                    "AuthenticationCode": self.RAILTOWN_AUTHENTICATION_CODE,
                    "ConnectionName": self.RAILTOWN_CONNECTION_NAME,
                    "ClientVersion": "python-rest",
                },
            }
        ]

        data = json.dumps(data).encode("utf-8")
        req = request.Request(self.RAILTOWN_LOGGING_URL, data=data, method="POST")
        with request.urlopen(req) as railtown_response:
            parsed_response = (
                {"body": railtown_response.read().decode("utf-8")} if railtown_response.read().decode("utf-8") else {}
            )
            parsed_response["status"] = railtown_response.status
            return parsed_response

    def active_full_hook(self, active: bool = True, exception_types: list = [Exception]):
        """A wrapper function for python exception that uses excepthook to forward any exception to Railtown
        Ideally, this function can be used to return uncaught exception, but it can be configured to return all exceptions
        @param `active:bool` if True, enable service, if False disable (restore excepthook state from moment when enabled)
        @param `exception_type:list` exception types and subtypes here will be captured and returned
        Note this after the exception is returned, exception will be forwarded to standard excepthook service (from moment when enabled)
        Please disable then re-enable when excepthook is modified, or else this function may not function as expected
        """

        def handle_exception(exception_type, exception_body, exception_traceback):
            if any(issubclass(exception_type, exception_class) for exception_class in exception_types):
                self.logger.info(f"logging uncaptured exception {str(exception_body)} to railtown")
                self.exception(exception_body)
            existing_hook(exception_type, exception_body, exception_traceback)

        existing_hook = ""
        if active:
            self.logger.info("Railtown full exception hook active")
            existing_hook = (
                sys.excepthook if sys.excepthook else sys.__excepthook__
            )  # is user defined their own exception hook
            sys.excepthook = handle_exception
        else:
            if existing_hook:
                self.logger.info("Railtown full exception hook disabled")
                sys.excepthook = existing_hook
            else:
                error_message = "You cannot disable the hook because it is not yet active"
                if e := self._internal_exception(error_message, AttributeError):
                    return e

    def __call__(self, error):
        """provoke exception endpoint, see RailtownLogger.exception()"""
        return self.exception(error)


if __name__ == "__main__":
    railtown_rest_string = repr(
        """// POST https://tst3978dadf9a1e49b3822276df158786e6.railtownlogs.com

[
   {
       "Body": "{\"Message\":\"[Your message]\",   \"Level\": 4,   \"Runtime\":\"dotnet-csharp\",   \"Properties\":{\"YourProperty1\":\"YourValue1\",\"YourProperty2\":\"YourValue2...\"},  \"TimeStamp\":\"2023-05-01T22:30:34.1044027+00:00\",  \"EnvironmentId\":\"69b820d5-d4d0-4883-99a1-c040d1a1f7cb\",  \"OrganizationId\":\"d66a542a-eb2d-4efe-9191-488bedb3d8e9\",  \"ProjectId\":\"4a550f34-92fd-4c68-b6fa-25d92437f6bb\"}",
       "UserProperties": {
           "Encoding":"utf-8",
           "AuthenticationCode": "Nry5VXDGh7xOKFW+Dh5S5DsyViYeAAmQP1JfX73/Pno=",
           "ConnectionName": "tst3978dadf9a1e49b3822276df158786e6.railtownlogs.com",
           "ClientVersion": "REST.v1"
       }
   }
]"""
    )

    print(RailtownLogger.simple_init(RailtownLogger, True, railtown_rest_string))
    exit()

    def raise_exception():
        assert "Railtown, the best AI error tracking tool you have!" == False

    try:
        raise_exception()
    except Exception as err:
        railtown_logger = RailtownLogger()
        import logging
        from io import StringIO

        log_stream = StringIO()
        logging.basicConfig(stream=log_stream, level=logging.INFO)
        logger1 = logging.getLogger(__name__)
        logger1.setLevel(10)
        logger1.error(str(err), exc_info=True)
        logger1.exception("err")
        # from opencensus.ext.azure.log_exporter import AzureLogHandler

        railtown_logger.exception(err)

        railtown_logger.active_full_hook()
        dived_by_zero = 3.1415 / 0
        print("sent")
        exit()
        # setting up exception logger. should only be used to throw exceptions
        azure_log_handler = AzureLogHandler(connection_string=os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"])
        loggerOC = logging.getLogger(__name__)
        loggerOC.setLevel(10)
        loggerOC.addHandler(azure_log_handler)
        loggerOC.exception("QError!")
        print(traceback.format_exc())
