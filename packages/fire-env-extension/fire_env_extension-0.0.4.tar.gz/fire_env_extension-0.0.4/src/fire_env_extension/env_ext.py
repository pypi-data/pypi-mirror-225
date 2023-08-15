'''classes for supporting env.parameter in fire cli'''
import logging
import os

logger = logging.getLogger(__name__)

TRUE_SET = {'ON', 'YES', 'Y', 'TRUE', 'T'}
FALSE_SET = {'OFF', 'NO', 'N', 'FALSE', 'F'}


class ParameterEnvValidator():
    ''' validates cmdline params or associated env.vars'''
    err_messages: list[str] = []
    info_messages: list[str] = []

    def str_validate(self, value: str, value_name: str, default_value, env_name: str) -> str:
        ''' cmdline param has env.vars priority set default value alway to 'None' '''
        retval = None
        if value != 'None':
            retval = value
            self.info_messages.append(f"{value_name}: '{retval}'")
        else:
            retval = os.getenv(env_name, None)
            if retval:
                self.info_messages.append(f"env.{env_name}: '{retval}'")
            else:
                retval = default_value
                self.info_messages.append(f"{value_name}: '{retval}'")
        if default_value is None:
            self.info_messages.append(
                f"{value_name}, env.{env_name}  -- no default")
        else:
            self.info_messages.append(
                f"{value_name}, env.{env_name}  -- default: '{default_value}'")
        if retval is None:
            self.err_messages.append(
                f"{value_name}, env.{env_name} is not set")
        return str(retval)

    def int_validate(self, value: str, value_name: str, default_value, env_name: str) -> int:
        ''' cmdline param has env.vars priority set default value alway to 'None' '''
        retstr = self.str_validate(value, value_name, default_value, env_name)
        retint: int = 0
        try:
            retint = int(retstr)
        except ValueError:
            self.err_messages.append(
                f"{value_name} or env.{env_name} must be an int number not '{retstr}'")
        return retint

    def float_validate(self, value: str, value_name: str, default_value, env_name: str) -> int:
        ''' cmdline param has env.vars priority set default value alway to 'None' '''
        retstr = self.str_validate(value, value_name, default_value, env_name)
        retfloat: float = 0
        try:
            retfloat = int(retstr)
        except ValueError:
            self.err_messages.append(
                f"{value_name} or env.{env_name} must be a float number not '{retstr}'")
        return retfloat

    def bool_validate(self, value: str, value_name: str, default_value, env_name: str) -> bool:
        ''' cmdline param has env vars priority set default value always to 'None' '''
        retstr = self.str_validate(value, value_name, default_value, env_name)
        retbool: bool = True
        if retstr.upper() in TRUE_SET:
            retbool = True
        elif retstr.upper() in FALSE_SET:
            retbool = False
        else:
            self.err_messages.append(
                f"{value_name} or env.{env_name} must be either in\n{TRUE_SET} or in {FALSE_SET}  not '{retstr}'")
        return retbool

    def get_info_messages(self) -> str:
        ''' return all info messages'''
        return '\n' + '\n'.join(self.info_messages)

    def get_err_messages(self) -> str:
        ''' return all error messages'''
        return '\n'.join(self.err_messages)


def to_bool(value, value_name: str) -> bool:
    ''' checks if value is a boolean '''
    if not value:
        msg = f"{value_name}: {value} is set to False"
        logger.info(msg)
        return False
    if isinstance(value, bool):
        msg = f"{value_name}: {value}"
        logger.info(msg)
        return value
    if isinstance(value, str):
        if value.upper() in TRUE_SET:
            msg = f"{value_name}: {value} is set to True"
            logger.info(msg)
            return True
        elif value.upper() in FALSE_SET:
            msg = f"{value_name}: {value} is set to False"
            logger.info(msg)
            return False
        else:
            msg = f"cannot convert {value_name}: {value} to bool"
            logger.error(msg)
            raise ValueError(msg)
    msg = f"cannot convert value: {value} to bool - unknown type"
    logger.error(msg)
    raise ValueError(msg)


def to_int(value, value_name: str) -> int:
    ''' checks if value is an int value '''
    if not value:
        msg = f"{value_name} must be set and from type int"
        logger.error(msg)
        raise ValueError(msg)
    try:
        return int(value)
    except ValueError as ver:
        msg = f"cannot cast {value_name}: {value} to int"
        logger.error(msg)
        raise TypeError(msg) from ver


def to_float(value, value_name: str) -> float:
    ''' checks if value is an int value '''
    if not value:
        msg = f"{value_name} must be set and from type float"
        logger.error(msg)
        raise ValueError(msg)
    try:
        if isinstance(value, str):
            value = value.replace(',', '.')
        return float(value)
    except ValueError as ver:
        msg = f"cannot cast {value_name}: {value} to float"
        logger.error(msg)
        raise TypeError(msg) from ver
