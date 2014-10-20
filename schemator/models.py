from schemator import errors
from schemator.fields import BaseField


class Model(object):

    """Base model."""

    def __init__(self, *args, **kwargs):
        schema = self.__schema__
        for attr_name in dir(schema):
            value = getattr(schema, attr_name, None)
            if isinstance(value, BaseField) and value.default:
                setattr(self, attr_name, value.default)

    def validate(self):
        """Validate model fields."""
        schema = self.__schema__
        # Check missing required fields
        required_fields = schema.get_required()
        missing_fields = []
        for field_name in required_fields:
            if not hasattr(self, field_name):
                missing_fields.append(field_name)
        if missing_fields:
            raise errors.ValidationError(
                "Not defined these required fields: {}".format(missing_fields)
            )
        return True

    def __setattr__(self, name, value):
        schema = self.__schema__
        field = getattr(schema, name, None)
        if field:
            parsed_value = field.parse_value(value)
            value = parsed_value
        return super().__setattr__(name, value)
