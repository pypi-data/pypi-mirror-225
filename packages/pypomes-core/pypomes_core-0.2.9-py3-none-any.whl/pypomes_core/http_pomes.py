import logging
import requests
import sys
from flask import Request
from typing import Final
from werkzeug.exceptions import BadRequest

from .env_pomes import APP_PREFIX, env_get_int
from .exception_pomes import exc_format

# https://developer.mozilla.org/pt-BR/docs/Web/HTTP/Status

HTTP_DELETE_TIMEOUT: Final[int] = env_get_int(f"{APP_PREFIX}_HTTP_DELETE_TIMEOUT", 10)
HTTP_GET_TIMEOUT: Final[int] = env_get_int(f"{APP_PREFIX}_HTTP_GET_TIMEOUT", 10)
HTTP_POST_TIMEOUT: Final[int] = env_get_int(f"{APP_PREFIX}_HTTP_POST_TIMEOUT", 10)
HTTP_PUT_TIMEOUT: Final[int] = env_get_int(f"{APP_PREFIX}_HTTP_PUT_TIMEOUT", 10)

MIMETYPE_BINARY: Final[str] = "application/octet-stream"
MIMETYPE_CSS: Final[str] = "text/css"
MIMETYPE_CSV: Final[str] = "text/csv"
MIMETYPE_HTML: Final[str] = "text/html"
MIMETYPE_JAVASCRIPT: Final[str] = "text/javascript"
MIMETYPE_JSON: Final[str] = "application/json"
MIMETYPE_MULTIPART: Final[str] = "multipart/form-data"
MIMETYPE_PDF: Final[str] = "application/pdf"
MIMETYPE_PKCS7: Final[str] = "application/pkcs7-signature"
MIMETYPE_SOAP: Final[str] = "application/soap+xml"
MIMETYPE_TEXT: Final[str] = "text/plain"
MIMETYPE_URLENCODED: Final[str] = "application/x-www-form-urlencoded"
MIMETYPE_XML: Final[str] = "application/xml"
MIMETYPE_ZIP: Final[str] = "application/zip"


# TODO (add description)
__HTTP_STATUS: Final[dict] = {
  200: {
    "name": "OK",
    "description": ""
  },
  201: {
    "name": "CREATED",
    "description": ""
  },
  202: {
    "name": "ACCEPTED",
    "description": ""
  },
  203: {
    "name": "NON AUTHORITATIVE INFORMATION",
    "description": ""
  },
  204: {
    "name": "NO CONTENT",
    "description": ""
  },
  205: {
    "name": "RESET CONTENT",
    "description": ""
  },
  206: {
    "name": "PARTIAL CONTENT",
    "description": ""
  },
  300: {
    "name": "MULTIPLE CHOICE",
    "description": ""
  },
  301: {
    "name": "MOVED PERMANENTLY",
    "description": ""
  },
  302: {
    "name": "FOUND",
    "description": ""
  },
  303: {
    "name": "SEE OTHER",
    "description": ""
  },
  304: {
    "name": "NOT MODIFIED",
    "description": ""
  },
  305: {
    "name": "USE PROXY",
    "description": ""
  },
  307: {
    "name": "TEMPORARY REDIRECT",
    "description": ""
  },
  308: {
    "name": "PERMANENT REDIRECT",
    "description": ""
  },
  400: {
    "name": "BAD REQUEST",
    "description": ""
  },
  401: {
    "name": "UNAUTHORIZED",
    "description": ""
  },
  403: {
    "name": "FORBIDDEN",
    "description": ""
  },
  404: {
    "name": "NOT FOUND",
    "description": ""
  },
  405: {
    "name": "METHOD NOT ALLOWED",
    "description": ""
  },
  406: {
    "name": "NOT ACCEPTABLE",
    "description": ""
  },
  407: {
    "name": "AUTHENTICATION REQUIRED",
    "description": ""
  },
  408: {
    "name": "REQUEST TIMEOUT",
    "description": ""
  },
  409: {
    "name": "CONFLICT",
    "description": ""
  },
  410: {
    "name": "GONE",
    "description": ""
  },
  411: {
    "name": "LENGTH REQUIRED",
    "description": ""
  },
  412: {
    "name": "",
    "description": ""
  },
  413: {
    "name": "PAYLOAD TOO LARGE",
    "description": ""
  },
  414: {
    "name": "URI TOO LONG",
    "description": ""
  },
  500: {
    "name": "INTERNAL SERVER ERROR",
    "description": ""
  },
  501: {
    "name": "NOT IMPLEMENTED",
    "description": ""
  },
  502: {
    "name": "",
    "description": ""
  },
  503: {
    "name": "BAD GATEWAY",
    "description": ""
  },
  504: {
    "name": "GATEWAY TIMEOPUT",
    "description": ""
  },
  505: {
    "name": "",
    "description": ""
  },
  506: {
    "name": "VARIANT ALSO NEGOTIATES",
    "description": ""
  },
  507: {
    "name": "INSUFFICIENT STORAGE",
    "description": ""
  },
  508: {
    "name": "LOOP DETECTED",
    "description": ""
  },
  510: {
    "name": "NOT EXTENDED",
    "description": ""
  },
  511: {
    "name": "NETWORK AUTHENTICATION REQUIRED",
    "description": ""
  }
}


def http_status_name(status_code: int) -> str:
    """
    Return the name of the status message identified to by *status_code*.

    :param status_code: the code of the status
    :return: the corresponding name given to the status
    """
    item: dict = __HTTP_STATUS.get(status_code, {"name": "Unknown status code"})
    return f"HTTP status code {status_code}: {item.get('name')}"


def http_status_description(status_code: int) -> str:
    """
    Return the description of the status message identified to by *status_code*.

    :param status_code: the code of the status
    :return: the corresponding status description
    """
    item: dict = __HTTP_STATUS.get(status_code, {"description": "Unknown status code"})
    return f"HTTP status code {status_code}: {item.get('description')}"


def http_json_from_form(request: Request) -> dict:
    """
    Build and return a *dict* containing the *key-value* pairs of the form parameters found in *request*.

    :param request: the HTTP request
    :return: dict containing the form parameters found
    """
    # initialize the return variable
    result: dict = {}

    # traverse the form parameters
    for key, value in request.form.items():
        result[key] = value

    return result


def http_json_from_request(request: Request) -> dict:
    """
    Obtain the *JSON* holding the *request*'s input parameters.

    :param request: the Request object
    :return: dict containing the input parameters (empty, if no input data exist)
    """
    # initialize the return variable
    result: dict = {}

    # retrieve the input JSON
    try:
        result: dict = request.get_json()
    except BadRequest:
        resp: str = request.get_data(as_text=True)
        # does the request contain input data ?
        if len(resp) > 0:
            # yes, possibly mal-fomed JSON
            raise

    return result


def http_json_from_get(errors: list[str] | None, url: str, headers: dict = None,
                       params: dict = None, timeout: int = HTTP_GET_TIMEOUT,
                       logger: logging.Logger = None) -> dict:
    """
    Retrieve a *JSON* string by issuing a *GET* request to the given *url*.

    The contents of the *JSON* string are returned as a *dict* .
    The request might contain *headers* and *parameters*.

    :param errors: incidental error messages
    :param url: the destination URL
    :param headers: optional headers
    :param params: optional parameters
    :param timeout: timeout, in seconds (defaults to HTTP_GET_TIMEOUT - use None to omit)
    :param logger: optional logger
    :return: the contents of the JSON string
    """
    if logger is not None:
        logger.debug(f"Invoking GET: '{url}'")

    # initialize the return variable
    result: dict | None = None

    try:
        response: requests.Response = requests.get(url=url,
                                                   headers=headers,
                                                   params=params,
                                                   timeout=timeout)
        if logger is not None:
            logger.debug(f"Invoked '{url}', status: '{http_status_name(response.status_code)}'")
        result = response.json()
    except Exception as e:
        err_msg: str = f"Error invoking '{url}': '{exc_format(e, sys.exc_info())}'"
        if logger:
            logger.error(err_msg)
        if errors is not None:
            errors.append(err_msg)

    return result


def http_json_from_post(errors: list[str] | None, url: str, headers: dict = None,
                        params: dict = None, data: dict = None, json: dict = None,
                        timeout: int = HTTP_POST_TIMEOUT, logger: logging.Logger = None) -> dict:
    """
    Retrieve a *JSON* string by issuing a *POST* request to the given *url*.

    The contents of the *JSON* string are returned as a *dict*.
    The request might contain *headers* and *parameters*.

    :param errors: incidental error messages
    :param url: the destination URL
    :param headers: optional headers
    :param params: optional parameters
    :param data: optionaL data to send in the body of the request
    :param json: optional JSON to send in the body of the request
    :param timeout: timeout, in seconds (defaults to HTTP_POST_TIMEOUT - use None to omit)
    :param logger: optional logger to log the operation with
    :return: the contents of the JSON string
    """
    if logger is not None:
        logger.debug(f"Invoking POST: '{url}'")

    # initialize the return variable
    result: dict | None = None

    try:
        response: requests.Response = requests.post(url=url,
                                                    headers=headers,
                                                    data=data,
                                                    json=json,
                                                    params=params,
                                                    timeout=timeout)
        if logger is not None:
            logger.debug(f"Invoked '{url}', status: '{http_status_name(response.status_code)}'")
        result = response.json()
    except Exception as e:
        err_msg: str = f"Error invoking '{url}': '{exc_format(e, sys.exc_info())}'"
        if logger:
            logger.error(err_msg)
        if errors is not None:
            errors.append(err_msg)

    return result
