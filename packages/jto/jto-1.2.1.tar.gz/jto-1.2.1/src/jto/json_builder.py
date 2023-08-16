import logging
from dataclasses import is_dataclass, asdict

from jto.undefined_field import Undefined


class JsonBuilder:
    _log = logging.getLogger(__name__)

    @classmethod
    def build_json(cls, dataclass_obj,
                   drop_nones: bool) -> dict:
        cls._log.debug('Building json from dataclass object')

        if not is_dataclass(dataclass_obj):
            cls._log.error(f'Dataclass type object expected, but received "{str(type(dataclass_obj))}"', exc_info=True)
            raise ValueError(f'Dataclass type object expected, but received "{str(type(dataclass_obj))}"')

        result_dict = asdict(dataclass_obj)
        result_dict = cls._drop_undefined(result_dict)
        if drop_nones:
            result_dict = cls._drop_nones(result_dict)
        return result_dict

    @classmethod
    def _drop_undefined(cls, original_dict: dict) -> dict:
        cls._log.debug('Dropping undefined fields from dict')

        result_dict = {}
        for key, value in original_dict.items():
            if value != Undefined:
                if isinstance(value, dict):
                    result_dict[key] = cls._drop_undefined(value)
                elif isinstance(value, (list, set, tuple)):
                    result_dict[key] = cls._drop_undefined_in_list(value)
                else:
                    result_dict[key] = value
        return result_dict

    @classmethod
    def _drop_undefined_in_list(cls, original_list: list) -> list:
        cls._log.debug('Dropping undefined fields from list')

        result_list = []
        for value in original_list:
            if value != Undefined:
                if isinstance(value, dict):
                    result_list.append(cls._drop_undefined(value))
                elif isinstance(value, (list, set, tuple)):
                    result_list.append(cls._drop_undefined_in_list(value))
                else:
                    result_list.append(value)
        return result_list

    @classmethod
    def _drop_nones(cls, original_dict: dict) -> dict:
        cls._log.debug('Dropping None fields from dict')

        result_dict = {}
        for key, value in original_dict.items():
            if isinstance(value, dict):
                result_dict[key] = cls._drop_nones(value)
            elif isinstance(value, (list, set, tuple)):
                result_dict[key] = cls._drop_nones_in_list(value)
            elif value is not None:
                result_dict[key] = value
        return result_dict

    @classmethod
    def _drop_nones_in_list(cls, original_list: list) -> list:
        cls._log.debug('Dropping None fields from list')

        result_list = []
        for value in original_list:
            if isinstance(value, dict):
                result_list.append(cls._drop_nones(value))
            elif isinstance(value, (list, set, tuple)):
                result_list.append(cls._drop_nones_in_list(value))
            else:
                result_list.append(value)
        return result_list
