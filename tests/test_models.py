import pytest

from schemator.models import Model
from schemator.schema import Schema
from schemator import fields
from schemator import errors


def test_base_model():

    class TestSchema(Schema):
        string = fields.StringField
        required_field = fields.BaseField(required=True)
        required_field_with_default_value = fields.BaseField(
            required=True, default=1)

    class TestModel(Model):
        __schema__ = TestSchema()

    test_model = TestModel()

    with pytest.raises(errors.ValidationError) as ex:
        test_model.validate()
        missed_field_text = (
            "['required_field', "
            "'required_field_with_default_value']")
        assert missed_field_text in ex.info

    test_model.string = 'this_is_string'

    with pytest.raises(errors.ValidationError):
        test_model.string = 1

    test_model.required_field = 123
    # Validation will be successful because the second required
    # field has a default value
    test_model.validate()
