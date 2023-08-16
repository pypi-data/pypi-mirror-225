import logging
from dataclasses import dataclass
from typing import List

from jto.undefined_field import Undefined


def to_camel_case(text):
    s = text.replace("-", " ").replace("_", " ")
    s = s.split()
    if len(text) == 0:
        return text
    return ''.join(i.capitalize() for i in s)


@dataclass
class FieldTemplate:
    field_name: str
    field_type: str
    json_field_name: str
    default_value: any = Undefined.__name__
    required: bool = False

    def build_field_string(self) -> str:
        field_string = f"{self.field_name}: Optional[{self.field_type}] = field(default={str(self.default_value)}, " \
                       f"metadata={{'name': '{self.json_field_name}', 'required': {str(self.required)}}})"
        return field_string


class ClassTemplate:
    _log = logging.getLogger(__name__)

    def __init__(self, class_name: str):
        self.class_name = class_name
        self.class_fields: List[FieldTemplate] = []

    def build_class_string(self):
        self._log.debug('Building class string for class template')

        class_string = f'@dataclass\nclass {self.class_name}:\n'
        class_field_strings = [cls_field.build_field_string() for cls_field in self.class_fields]
        fields_string = '\n    '.join(class_field_strings)
        return class_string + '    ' + fields_string


class DataclassGenerator:
    _log = logging.getLogger(__name__)

    def __init__(self):
        self._class_templates: List[ClassTemplate] = []

    def build_classes_string(self, root_class_name: str,
                             json_data: dict):
        self._log.debug('Building classes string from class templates')

        self._parse_dict(root_class_name, json_data)
        class_strings = [cls_temp.build_class_string() for cls_temp in self._class_templates]
        result_string = '\n\n'.join(class_strings)
        return result_string

    def _parse_dict(self, dict_name: str,
                    dict_data: dict) -> FieldTemplate:
        self._log.debug('Parsing dict')

        class_name = to_camel_case(dict_name)
        class_template = ClassTemplate(class_name)
        for key, value in dict_data.items():
            if isinstance(value, dict):
                class_template.class_fields.append(self._parse_dict(key, value))
            elif isinstance(value, list):
                class_template.class_fields.append(self._parse_list(key, value))
            else:
                class_template.class_fields.append(FieldTemplate(key, type(value).__qualname__, key))
        self._class_templates.append(class_template)
        return FieldTemplate(dict_name, class_name, dict_name)

    def _parse_list(self, list_name: str,
                    list_data: list) -> FieldTemplate:
        self._log.debug('Parsing list')

        if len(list_data) == 0:
            field_type = f'List[{object}]'
        else:
            list_element = list_data[0]
            if isinstance(list_element, dict):
                field_type = f'List[{self._parse_dict(list_name, list_element).field_type}]'
            else:
                field_type = f'List[{type(list_element).__qualname__}]'
        return FieldTemplate(list_name, field_type, list_name)
