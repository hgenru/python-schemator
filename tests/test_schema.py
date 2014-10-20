from schemator.schema import Schema
from schemator.fields import BaseField


def test_modify_fields():

    class TestSchema(Schema):
        field_as_class = BaseField
        field_as_inst = BaseField()

    test_schema = TestSchema()
    assert isinstance(test_schema.field_as_class, BaseField)
    assert isinstance(test_schema.field_as_inst, BaseField)


def test_get_required():

    class TestSchema(Schema):
        required_field_one = BaseField(required=True)
        required_field_two = BaseField(required=True)
        not_required_field = BaseField(required=False)

    test_schema = TestSchema()
    required_fields = test_schema.get_required()

    assert required_fields == ['required_field_one', 'required_field_two']


def test_schema_child():

    class TestSchema(Schema):
        required_field = BaseField(required=True)
        not_required_field = BaseField(required=False)

    class TestSchemaChild(TestSchema):
        requirecd_field_two = BaseField(required=True)
        not_required_field_two = BaseField(required=False)

    test_schema_child = TestSchemaChild()
    assert 'required_field' in dir(test_schema_child)
    assert 'not_required_field_two' in dir(test_schema_child)

    required_fields = test_schema_child.get_required()
    expected_fields = ['requirecd_field_two', 'required_field']
    assert required_fields == expected_fields
