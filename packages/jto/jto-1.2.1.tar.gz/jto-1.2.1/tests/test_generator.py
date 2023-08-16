from jto.dataclass_generator import DataclassGenerator, FieldTemplate, ClassTemplate
from jto.undefined_field import Undefined


def test_happy_day():
    data = {
        "status": 200,
        "data": {
            "first": "foo",
            "last": "bar",
            "struct": [
                {"f1": "1"},
                {"f1": "2"}
            ]
        }
    }

    classes = DataclassGenerator()
    classes_str = classes.build_classes_string('Response', data)
    assert classes_str == ("@dataclass\nclass Struct:\n"
                           "    f1: Optional[str] = field(default=Undefined, metadata={'name': 'f1', 'required': False})\n\n"
                           "@dataclass\nclass Data:\n"
                           "    first: Optional[str] = field(default=Undefined, metadata={'name': 'first', 'required': False})\n"
                           "    last: Optional[str] = field(default=Undefined, metadata={'name': 'last', 'required': False})\n"
                           "    struct: Optional[List[Struct]] = field(default=Undefined, metadata={'name': 'struct', 'required': False})\n\n"
                           "@dataclass\nclass Response:\n"
                           "    status: Optional[int] = field(default=Undefined, metadata={'name': 'status', 'required': False})\n"
                           "    data: Optional[Data] = field(default=Undefined, metadata={'name': 'data', 'required': False})")


def test_parse_empty_dict():
    data = {}

    generator = DataclassGenerator()
    classes_str = generator.build_classes_string('Response', data)

    assert classes_str == "@dataclass\nclass Response:\n    "


def test_empty_list_value():
    data = {'var': []}

    generator = DataclassGenerator()
    classes_str = generator.build_classes_string('Response', data)

    assert classes_str == "@dataclass\nclass Response:\n    var: Optional[List[<class 'object'>]] = " \
                          "field(default=Undefined, metadata={'name': 'var', 'required': False})"
