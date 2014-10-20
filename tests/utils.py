import pytest
from jsonschema.exceptions import ValidationError


def check_field_on_wrong_values(field, list_of_values):
    for value in list_of_values:
        with pytest.raises(ValidationError):
            field.parse_value(value)
