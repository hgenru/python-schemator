from schemator.schema import Schema
from schemator import fields


def test_simple_json_schema():

    class PersonSchema(Schema):

        """Person schema"""

        name = fields.StringField(required=True)
        age = fields.IntegerField(required=True)
        description = fields.StringField

    person = PersonSchema()
    person_json_schema = person.to_json_schema()
    expected_json_schema = {
        '$schema': "http://json-schema.org/draft-04/schema#",
        'title': 'PersonSchema',
        'description': 'Person schema',
        'type': 'object',
        'properties': {
            'age': {'type': 'integer'},
            'description': {'type': 'string'},
            'name': {'type': 'string'}
        },
        'required': ['age', 'name']
    }
    assert person_json_schema == expected_json_schema


def test_schema_with_special_attributes():

    class SpecialSchema(Schema):
        __title__ = 'super-schema'
        __description__ = 'this is super-schema'

    special_json_schema = SpecialSchema.to_json_schema()
    expected_schema = {
        '$schema': "http://json-schema.org/draft-04/schema#",
        'title': 'super-schema',
        'description': 'this is super-schema',
        'type': 'object',
        'properties': {},
        'required': []
    }
    assert special_json_schema == expected_schema
