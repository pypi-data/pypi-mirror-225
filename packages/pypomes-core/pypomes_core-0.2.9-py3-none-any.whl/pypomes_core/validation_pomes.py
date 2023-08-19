from datetime import date, datetime
from logging import Logger
from typing import Final
from .datetime_pomes import TIMEZONE_LOCAL
from .env_pomes import APP_PREFIX, env_get_str

VALIDATION_MSG_LANGUAGE: Final[str] = env_get_str(f"{APP_PREFIX}_VALIDATION_MSG_LANGUAGE", "pt")
VALIDATION_MSG_PREFIX: Final[str] = env_get_str(f"{APP_PREFIX}_VALIDATION_MSG_PREFIX", APP_PREFIX)


def validate_value(val: str | int | float, min_val: int = None,
                   max_val: int = None, default: bool | list[any] = None) -> str:
    """
    Validate *val* according to type, range, or membership in values list, as specified.

    :param val: the value to be validated
    :param min_val: if val is a string, specifies its minimum length; otherwise, specifies its minimum value
    :param max_val:  if val is a string, specifies its maximum length; otherwise, specifies its maximum value
    :param default: if boolean, requires val to be specified; if list, requires val to be in it
    :return: None if val passes validation, or the corresponding error message otherwise
    """
    # initialize the return variable
    result: str | None = None

    # 'val' can be None, and None can be in 'default'
    if isinstance(default, list):
        if val not in default:
            if val is None:
                result = __format_error(10)
            else:
                length: int = len(default)
                if length == 1:
                    result = __format_error(15, val, default[0])
                else:
                    # o último elemento da lista é None ?
                    if default[-1] is None:
                        # sim, omita-o da mensagem
                        length -= 1
                    result = __format_error(16, val, [default[:length]])
    elif val is None:
        if isinstance(default, bool) and default:
            result = __format_error(10)
    elif isinstance(val, str):
        length: int = len(val)
        if min_val is not None and max_val == min_val and length != min_val:
            result = __format_error(14, val, min_val)
        elif max_val is not None and max_val < length:
            result = __format_error(13, val, max_val)
        elif min_val is not None and length < min_val:
            result = __format_error(12, val, min_val)
    elif (min_val is not None and val < min_val) or \
         (max_val is not None and val > max_val):
        result = __format_error(17, val, [min_val, max_val])

    return result


def validate_bool(errors: list[str] | None, scheme: dict, attr: str,
                  default: bool = None, mandatory: bool = False, logger: Logger = None) -> bool:
    """
    Validate the boolean value associated with *attr* in *scheme*.

    If provided, this value must be a *bool*, or the string *t*, *true*, *f*, or *false*.

    :param errors: incidental error messages
    :param scheme: dictionary containing the value to be validated
    :param attr: the name of the attribute whose value is being validated
    :param default: default value, if not found
    :param mandatory: specifies whether the value must be provided
    :param logger: optional logger
    :return: the validated value, or None if validation failed
    """
    # initialize the return variable
    result: bool | None = None

    stat: str | None = None
    pos: int = attr.rfind(".") + 1
    suffix: str = attr[pos:]
    try:
        result = scheme[suffix]
        if isinstance(result, str):
            if result.lower() in ["t", "true"]:
                result = True
            elif result.lower() in ["f", "false"]:
                result = False
        if not isinstance(result, bool):
            stat = __format_error(18, result, "bool")
    except (KeyError, TypeError):
        if default is not None:
            result = default
        elif mandatory:
            stat = __format_error(10)

    if stat is not None:
        __validate_log(errors, f"{stat} @{attr}", logger)

    return result


def validate_int(errors: list[str] | None, scheme: dict, attr: str,
                 min_val: int = None, max_val: int = None,
                 default: bool | int | list[int] = None, logger: Logger = None) -> int:
    """
    Validate the *int* value associated with *attr* in *scheme*.

    If provided, this value must be a *int*, or a valid string representation of a *int*.

    :param errors: incidental error messages
    :param scheme: dictionary containing the value to be validated
    :param attr: the attribute associated with the value to be validated
    :param min_val: the minimum value accepted
    :param max_val:  the maximum value accepted
    :param default: if int, specifies the default value;
                    if bool, requires the value to be specified;
                    if list, requires the value to be in it
    :param logger: optional logger
    :return: the validated value, or None if validation failed
    """
    stat: str | None = None
    pos: int = attr.rfind(".") + 1
    suffix: str = attr[pos:]

    # retrieve the value
    result: int | None = scheme.get(suffix)

    # validate it
    if result is None:
        result = default
    elif isinstance(result, str):
        try:
            result = int(result)
        except ValueError:
            result = None
            stat = __format_error(18, result, "int")

    # bool is subtype of int
    if result is not None and \
            (isinstance(result, bool) or not isinstance(result, int)):
        stat = __format_error(18, result, "int")

    if stat is None:
        stat = validate_value(result, min_val, max_val, default)

    if stat is not None:
        __validate_log(errors, f"{stat} @{attr}", logger)

    return result


def validate_float(errors: list[str] | None, scheme: dict, attr: str,
                   min_val: float = None, max_val: float = None,
                   default: bool | int | float | list[float | int] = None, logger: Logger = None) -> float:
    """
    Validate the *float* value associated with *attr* in *scheme*.

    If provided, this value must be a *float*, or a valid string representation of a *float*.

    :param errors: incidental error messages
    :param scheme: dictionary containing the value to be validated
    :param attr: the attribute associated with the value to be validated
    :param min_val: the minimum value accepted
    :param max_val:  the maximum value accepted
    :param default: if float, specifies the default value;
                    if bool, requires the value to be specified;
                    if list, requires the value to be in it
    :param logger: optional logger
    :return: the validated value, or None if validation failed
    """
    stat: str | None = None
    pos: int = attr.rfind(".") + 1
    suffix: str = attr[pos:]

    # retrieve the value
    result: float | None = scheme.get(suffix)

    # validate it
    if result is None:
        result = default
    elif isinstance(result, str | int):
        try:
            result = float(result)
        except ValueError:
            stat = __format_error(18, result, "int")

    if result is not None and not isinstance(result, float):
        stat = __format_error(18, result, "float")

    if stat is None:
        stat = validate_value(result, min_val, max_val, default)

    if stat is not None:
        result = None
        __validate_log(errors, f"{stat} @{attr}", logger)

    return result


def validate_str(errors: list[str] | None, scheme: dict, attr: str,
                 min_length: int = None, max_length: int = None,
                 default: bool | str | list[str] = None, logger: Logger = None) -> str:
    """
    Validate the *str* value associated with *attr* in *scheme*.

    If provided, this value must be a *str*.

    :param errors: incidental error messages
    :param scheme: dictionary containing the value to be validated
    :param attr: the attribute associated with the value to be validated
    :param min_length: the minimum length accepted
    :param max_length:  the maximum length accepted
    :param default: if str, specifies the default value;
                    if bool, requires the value to be specified;
                    if list, requires the value to be in it
    :param logger: optional logger
    :return: the validated value, or None if validation failed
    """
    stat: str | None = None
    pos: int = attr.rfind(".") + 1
    suffix: str = attr[pos:]

    # obtain and validate the value
    result: str = scheme.get(suffix)
    if result is not None and not isinstance(result, str):
        stat = __format_error(18, result, "str")
    elif isinstance(default, str):
        if result is None:
            result = default
        else:
            stat = validate_value(result, min_length, max_length)
    else:
        stat = validate_value(result, min_length, max_length, default)

    if stat is not None:
        __validate_log(errors, f"{stat} @{attr}", logger)

    return result


def validate_date(errors: list[str] | None, scheme: dict, attr: str,
                  default: bool | date = None, day_first: bool = True, logger: Logger = None) -> date:
    """
    Validate the *date* value associated with *attr* in *scheme*.

    If provided, this value must be a *date*, or a valid string representation of a *date*.

    :param errors: incidental error messages
    :param scheme: dictionary containing the value to be validated
    :param attr: the attribute associated with the value to be validated
    :param day_first: indicates that the day precedes the month in the string representing the date
    :param default: if date, specifies the default value;
                    if bool, requires the value to be specified
    :param logger: optional logger
    :return: the validated value, or None if validation failed
    """
    # import needed module
    from .datetime_pomes import date_parse

    # initialize the return variable
    result: date | None = None

    stat: str | None = None
    pos: int = attr.rfind(".") + 1
    suffix: str = attr[pos:]
    try:
        date_str: str = scheme[suffix]
        result = date_parse(date_str, dayfirst=day_first)
        if result is None:
            stat = __format_error(11, date_str)
        elif result > datetime.now(TIMEZONE_LOCAL).date():
            stat = __format_error(19, date_str)
    except KeyError:
        if isinstance(default, bool) and default:
            stat = __format_error(10)
        elif isinstance(default, date):
            result = default

    if stat is not None:
        __validate_log(errors, f"{stat} @{attr}", logger)

    return result


def validate_datetime(errors: list[str] | None, scheme: dict, attr: str,
                      default: bool | datetime = None, day_first: bool = True, logger: Logger = None) -> datetime:
    """
    Validate the *datetime* value associated with *attr* in *scheme*.

    If provided, this value must be a *date*, or a valid string representation of a *date*.

    :param errors: incidental error messages
    :param scheme: dictionary containing the value to be validated
    :param attr: the attribute associated with the value to be validated
    :param day_first: indicates that the day precedes the month in the string representing the date
    :param default: if datetime, specifies the default value;
                    if bool, requires the value to be specified
    :param logger: optional logger
    :return: the validated value, or None if validation failed
    """
    # import needed module
    from .datetime_pomes import datetime_parse

    # initialize the return variable
    result: datetime | None = None

    stat: str | None = None
    pos: int = attr.rfind(".") + 1
    suffix: str = attr[pos:]
    try:
        date_str: str = scheme[suffix]
        result = datetime_parse(date_str, dayfirst=day_first)
        if result is None:
            stat = __format_error(21, date_str)
        elif result > datetime.now(TIMEZONE_LOCAL):
            stat = __format_error(18, date_str)
    except KeyError:
        if isinstance(default, bool) and default:
            stat = __format_error(10)
        elif isinstance(default, datetime):
            result = default

    if stat is not None:
        __validate_log(errors, f"{stat} @{attr}", logger)

    return result


def validate_ints(errors: list[str] | None, scheme: dict, attr: str,
                  min_val: int = None, max_val: int = None,
                  mandatory: bool = False, logger: Logger = None) -> list[int]:
    """
    Validate the list of *int* values associated with *attr* in *scheme*.

    If provided, this list must contain *ints*, or valid string representations of *ints*.

    :param errors: incidental error messages
    :param scheme: dictionary containing the list of values to be validated
    :param attr: the attribute associated with the list of values to be validated
    :param min_val: the minimum value accepted
    :param max_val:  the maximum value accepted
    :param mandatory: whether the list of values must be provided
    :param logger: optional logger
    :return: the list of validated values, or None if validation failed
    """
    # initialize the return variable
    result: list[any] | None = None

    err_msg: str | None = None
    pos: int = attr.rfind(".") + 1
    suffix: str = attr[pos:]
    try:
        values: list[any] = scheme[suffix]
        if isinstance(values, list):
            result = []
            if len(values) > 0:
                for inx, value in enumerate(values):
                    result.append(value)
                    if isinstance(value, int):
                        stat: str = validate_value(value, min_val, max_val)
                    else:
                        stat: str = __format_error(18, value, "int")
                    if stat is not None:
                        err_msg = f"{stat} @{attr}[{inx+1}]"
            elif mandatory:
                err_msg = __format_error(10, f"@{attr}")
        else:
            err_msg = __format_error(18, result, "list", f"@{attr}")
    except (KeyError, TypeError):
        if mandatory:
            err_msg = __format_error(10, f"@{attr}")

    if err_msg:
        __validate_log(errors, err_msg, logger)

    return result


def validate_strs(errors: list[str] | None, scheme: dict,
                  attr: str, min_length: int, max_length: int,
                  mandatory: bool = False, logger: Logger = None) -> list[str]:
    """
    Validate the list of *str* values associated with *attr* in *scheme*.

    If provided, this list must contain *strs*.

    :param errors: incidental error messages
    :param scheme: dictionary containing the list of values to be validated
    :param attr: the attribute associated with the list of values to be validated
    :param min_length: the minimum length accepted
    :param max_length:  the maximum length accepted
    :param mandatory: whether the list of values must be provided
    :param logger: optional logger
    :return: the list of validated values, or None if validation failed
    """
    # initialize the return variable
    result: list[any] | None = None

    err_msg: str | None = None
    pos: int = attr.rfind(".") + 1
    suffix: str = attr[pos:]
    try:
        values: list[any] = scheme[suffix]
        if isinstance(values, list):
            result = []
            if len(values) > 0:
                for inx, value in enumerate(values):
                    result.append(value)
                    if isinstance(value, str):
                        stat: str = validate_value(value, min_length, max_length)
                    else:
                        stat: str = __format_error(18, value, "str")
                    if stat is not None:
                        err_msg = f"{stat} @{attr}[{inx+1}]"
            elif mandatory:
                err_msg = __format_error(11, f"@{attr}")
        else:
            err_msg = __format_error(18, result, "list", f"@{attr}")
    except (KeyError, TypeError):
        if mandatory:
            err_msg = __format_error(11, f"@{attr}")

    if err_msg:
        __validate_log(errors, err_msg, logger)

    return result


def validate_format_error(error_id: int, err_msgs: dict, *args) -> str:
    """
    Format and return the error message identified by *err_id* in *err_msgs*.

    The message is built from the message element in *err_msgs* identified by *err_id*.
    The occurrences of '{}' in the element are sequentially replaced by the given *args*.

    :param error_id: the identification of the message element
    :param err_msgs: the message elements
    :param args: optional arguments to format the error message with
    :return: the formatted error message
    """
    # initialize the return variable
    result: str = VALIDATION_MSG_PREFIX + str(error_id) + ": " + err_msgs.get(error_id)

    if result is not None:
        # apply the provided  arguments
        for arg in args:
            if arg is None:
                result = result.replace(" {}", "", 1)
            elif isinstance(arg, str) and arg.startswith("@"):
                result += " " + arg
            elif isinstance(arg, str) and arg.find(" ") > 0:
                result = result.replace("{}", arg, 1)
            else:
                result = result.replace("{}", f"'{arg}'", 1)

    return result


# formata itens na lista de erros: <codigo> <descricao> [@<atributo>]
def validate_format_errors(errors: list[str]) -> list[dict]:
    """
    Build and return a *dict* to be used as the value representing a list of errors.

    This list is tipically used in a returning *JSON* string.

    :param errors: the errors to build the list with
    :return: the list built
    """
    # import needed module
    from .str_pomes import str_find_whitespace

    # initialize the return variable
    result: list[dict] = []

    # extract error code, description, and attribute from text
    for error in errors:
        # localiza o último indicador do atributo
        pos = error.rfind("@")

        # is there a whitespace in the attribute ?
        if pos > 0 and str_find_whitespace(error[pos:]) > 0:
            # yes, disregard it
            pos = -1

        # does the text contain the attribute ?
        if pos == -1:
            # no
            out_error: dict = {}
            desc: str = error
        else:
            # yes
            term: str = "attribute" if VALIDATION_MSG_LANGUAGE == "en" else "atributo"
            out_error: dict = {term: error[pos + 1:]}
            desc = error[:pos - 1]

        # does the text contain an error code ?
        if desc.startswith(VALIDATION_MSG_PREFIX):
            # yes
            term: str = "code" if VALIDATION_MSG_LANGUAGE == "en" else "codigo"
            pos: int = desc.find(":")
            out_error[term] = desc[0:pos]
            desc = desc[pos+1:]

        term: str = "description" if VALIDATION_MSG_LANGUAGE == "en" else "descricao"
        out_error[term] = desc
        result.append(out_error)

    return result


def __format_error(err_id: int, *args) -> str:
    """
    Format and return the error message identified by *err_id*.

    The message is built from the message element in the error list herein, identified by *err_id*.
    The occurrences of '{}' in the element are sequentially replaced by the given *args*.

    :param error_id: the identification of the message element
    :param err_msgs: the message elements
    :param args: optional arguments to format the error message with
    :return: the formatted error message
    """
    err_msgs_en: Final[dict] = {
        10: "Value must be provided",
        11: "Invalid value {}",
        12: "Invalid value {}: length shorter than {}",
        13: "Invalid value {}: length longer than {}",
        14: "Invalid value {}: length must be {}",
        15: "Invalid value {}: must be {}",
        16: "Invalid value {}: must be one of {}",
        17: "Invalid value {}: must be in the range {}",
        18: "Invalid value {}: must be type {}",
        19: "Invalid value {}: date is later than the current date"
    }

    err_msgs_pt: Final[dict] = {
        10: "Valor deve ser fornecido",
        11: "Valor {} inválido",
        12: "Valor {} inválido: comprimento menor que {}",
        13: "Valor {} inválido: comprimento maior que {}",
        14: "Valor {} inválido: comprimento deve ser {}",
        15: "Valor {} inválido: deve ser {}",
        16: "Valor {} inválido: deve ser um de {}",
        17: "Valor {} inválido: deve estar no intervalo {}",
        18: "Valor {} inválido: deve ser do tipo {}",
        19: "Valor {} inválido: data posterior à data atual"
    }

    err_msgs: dict | None = None
    match VALIDATION_MSG_LANGUAGE:
        case "en":
            err_msgs = err_msgs_en
        case "pt":
            err_msgs = err_msgs_pt

    return validate_format_error(err_id, err_msgs, args)


def __validate_log(errors: list[str], err_msg: str, logger: Logger) -> None:

    if logger:
        logger.error(err_msg)
    if errors is not None:
        errors.append(err_msg)
