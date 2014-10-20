from inspect import isclass

from jsonschema import Draft4Validator

from schemator.fields import BaseField


class _SchemaMeta(type):

    def __new__(self, cls, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if isclass(attr_value) and issubclass(attr_value, BaseField):
                field = attr_value()
                attrs[attr_name] = field
        return super().__new__(self, cls, bases, attrs)


class Schema(object, metaclass=_SchemaMeta):

    """Base schema class.

    Attributes:
        default_json_schema_draft (str): Default json schema draft.
    """

    @classmethod
    def get_required(cls):
        """Get required fields.

        Returns:
            `List` of required fields name.
        """
        required = []
        for name in dir(cls):
            value = getattr(cls, name, None)
            if isinstance(value, BaseField) and value.required:
                required.append(name)
        return required

    @classmethod
    def to_json_schema(cls):
        """Convert schema to JsonSchema.

        By default use current actual Json Schema draft.
        """
        return cls.to_json_schema_draft4()

    @classmethod
    def to_json_schema_draft4(cls):
        """Convert schema to JsonSchema Draft#4."""
        title = cls.__title__ if hasattr(cls, '__title__') else cls.__name__
        schema_draft = "http://json-schema.org/draft-04/schema#"
        required_fields = cls.get_required()
        properties = dict()

        for name in dir(cls):
            value = getattr(cls, name, None)
            if isinstance(value, BaseField):
                prop_schema = value.to_json_schema_draft4()
                properties[name] = prop_schema

        schema = {
            '$schema': schema_draft,
            'title': title,
            'type': 'object',
            'properties': properties,
            'required': required_fields
        }

        description = cls.__doc__
        if hasattr(cls, '__description__'):
            description = cls.__description__
        if description:
            schema['description'] = description

        return schema

    @classmethod
    def validate(cls, struct):
        return cls.validate_draft4(struct)

    @classmethod
    def validate_draft4(cls, struct):
        json_schema = cls.to_json_schema_draft4()
        validator = Draft4Validator(json_schema)
        return validator.validate(struct)
