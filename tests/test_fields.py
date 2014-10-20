import pytest

from schemator import fields
from schemator import errors
from tests.utils import check_field_on_wrong_values


def test_base_field():

    simple_field = fields.BaseField()
    assert simple_field.parse_value(42) == 42
    assert simple_field.to_struct(42) == 42
    assert simple_field.validate(42)
    assert not simple_field.required

    required_field = fields.BaseField(required=True)
    assert required_field.required

    field_with_default_value = fields.BaseField(default=42)
    assert field_with_default_value.default == 42

    field_with_default_value_as_func = fields.BaseField(default=lambda: 2 + 2)
    assert field_with_default_value_as_func.default == 4


def TestBuiltItTypesFields(object):

    def test_string_field(self):
        string_field = fields.StringField()
        assert string_field.parse_value('string')

        wrong_input_values = [1, 0.123, ['list'], {'dict': 1}]
        check_field_on_wrong_values(string_field, wrong_input_values)

    def test_integer_field(self):
        integer_field = fields.IntegerField()
        assert integer_field.parse_value(123)

        wrong_input_values = ['1', 'string', 0.123, ['list'], {'dict': 1}]
        check_field_on_wrong_values(integer_field, wrong_input_values)

    def test_float_field(self):
        float_field = fields.FloatField()
        assert float_field.parse_value(0.123)

        wrong_input_values = ['string', '1', '0.123', ['list'], {'dict': 1}]
        check_field_on_wrong_values(float_field, wrong_input_values)

    def test_number_field(self):
        number_field = fields.NumberField()
        assert number_field.parse_value(123)
        assert number_field.parse_value(0.123)

        wrong_input_values = ['string', '1', '0.123', ['list'], {'dict': 1}]
        check_field_on_wrong_values(number_field, wrong_input_values)


def test_broken_default_value():

    with pytest.raises(errors.ValidationError):
        fields.StringField(default=1)


class TestJsonSchemaDraft4(object):

    def test_base_field(self):
        base_field = fields.BaseField()
        assert fields.BaseField.to_json_schema_draft4() == {'type': 'any'}
        assert base_field.to_json_schema_draft4() == {'type': 'any'}

    def test_string_field(self):
        string_field = fields.StringField()
        assert string_field.to_json_schema_draft4() == {'type': 'string'}

    def test_integer_field(self):
        integer_field = fields.IntegerField()
        assert integer_field.to_json_schema_draft4() == {'type': 'integer'}

    def test_float_field(self):
        float_field = fields.FloatField()
        assert float_field.to_json_schema_draft4() == {'type': 'float'}

    def test_number_field(self):
        number_field = fields.NumberField()
        assert number_field.to_json_schema_draft4() == {'type': 'number'}
