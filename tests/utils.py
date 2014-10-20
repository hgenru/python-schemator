import pytest

from schemator import errors


def check_field_on_wrong_values(field, list_of_values):
    for value in list_of_values:
        with pytest.raises(errors.ValidationError):
            field.parse_value(value)
