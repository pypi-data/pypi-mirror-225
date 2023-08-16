from dataclasses import dataclass, field
from typing import List, Optional

import pytest

from jto import JTOConverter
from jto.undefined_field import Undefined


def test_convert_json_to_dataclass():
    data = {
        'name': 'John Doe',
        'ages': [10, 20, 30],
        'book': {
            'title': 'Python'
        },
        'addresses': [
            {'address': '123 Main St'},
        ]
    }

    @dataclass
    class Book:
        title: Optional[str] = field(default=Undefined, metadata={'name': 'title', 'required': False})

    @dataclass
    class Addresses:
        address: Optional[str] = field(default=Undefined, metadata={'name': 'address', 'required': False})

    @dataclass
    class Data:
        name: Optional[str] = field(default=Undefined, metadata={'name': 'name', 'required': False})
        ages: Optional[List[int]] = field(default=Undefined, metadata={'name': 'ages', 'required': False})
        book: Optional[Book] = field(default=Undefined, metadata={'name': 'book', 'required': False})
        addresses: Optional[List[Addresses]] = field(default=Undefined, metadata={'name': 'addresses', 'required': False})

    data_object = JTOConverter.from_json(Data, data)
    assert data_object == Data(name='John Doe', ages=[10, 20, 30], book=Book(title='Python'),
                               addresses=[Addresses(address='123 Main St')])


def test_not_nullable_field():
    data = {"f1": None}

    @dataclass
    class Test:
        f1: str = field(default=Undefined, metadata={'name': 'f1', 'required': False})

    with pytest.raises(ValueError, match='Field "f1" cannot be null'):
        JTOConverter.from_json(Test, data)


def test_convert_empty_dict():
    data = {}

    @dataclass
    class Test:
        f1: Optional[str] = field(default=Undefined, metadata={'name': 'f1', 'required': False})

    dataclass_object = JTOConverter.from_json(Test, data)
    assert dataclass_object == Test()

    json_object = JTOConverter.to_json(dataclass_object, drop_nones=True)
    assert json_object == {}


def test_convert_empty_list():
    data = {"f1": []}

    @dataclass
    class Test:
        f1: Optional[List[str]] = field(default=Undefined, metadata={'name': 'f1', 'required': False})

    dataclass_object = JTOConverter.from_json(Test, data)
    assert dataclass_object == Test(f1=[])


def test_convert_dict_missing_required_field():
    data = {}

    @dataclass
    class Test:
        f1: Optional[str] = field(default=Undefined, metadata={'name': 'f1', 'required': True})

    with pytest.raises(ValueError, match='Required field "f1" not found in the data "{}"'):
        JTOConverter.from_json(Test, data)


def test_convert_dict_field_with_null_value():
    data = {"f1": None}

    @dataclass
    class Test:
        f1: Optional[str] = field(default=Undefined, metadata={'name': 'f1', 'required': False})

    dataclass_object = JTOConverter.from_json(Test, data)
    assert dataclass_object == Test(f1=None)


def test_convert_dict_with_unexpected_values():
    data = {"one": 1}

    @dataclass
    class Test:
        f1: Optional[str] = field(default=Undefined, metadata={'name': 'f1', 'required': False})

    dataclass_object = JTOConverter.from_json(Test, data)
    assert dataclass_object == Test()


def test_convert_value_with_unexpected_type():
    data = {"f1": 1}

    @dataclass
    class Test:
        f1: Optional[str] = field(default=Undefined, metadata={'name': 'f1', 'required': False})

    with pytest.raises(TypeError, match='Expected value type is "<class \'str\'>", but received "<class \'int\'>"'):
        JTOConverter.from_json(Test, data)


def test_convert_dataclass_to_json():
    @dataclass
    class Request:
        Id: Optional[int] = field(default=Undefined, metadata={'name': 'Id', 'required': False})
        Customer: Optional[str] = field(default=Undefined, metadata={'name': 'Customer', 'required': False})
        Quantity: Optional[int] = field(default=Undefined, metadata={'name': 'Quantity', 'required': False})
        Price: Optional[float] = field(default=Undefined, metadata={'name': 'Price', 'required': False})

    dataclass_object = Request(1, 'aaa', 2, 3.33)

    json_object = JTOConverter.to_json(dataclass_object, drop_nones=False)

    expected_json = {'Id': 1, 'Customer': 'aaa', 'Quantity': 2, 'Price': 3.33}
    assert json_object == expected_json

