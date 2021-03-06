from jsonschema import Draft4Validator


class BaseField(object):

    """Base field class.

    Attributes:
        required (bool): Do require this field or not.
        default (any): Computed default value.
        json_schema_draft4 (dict): JsonSchema definition.
    """

    json_schema_draft4 = dict()

    def __init__(
        self,
        required=False,
        default=None
    ):
        """Init.

        Args:
            required (bool, optional): Do require this field or not.
            default (any, optional): The default value for this field.
                The functions are called during initialization.
        """
        self.draft4validator = Draft4Validator(self.json_schema_draft4)

        self.required = required
        default = default() if callable(default) else default
        self.default = self.parse_value(default) if default else None

    def parse_value(self, value):
        """Parse ``value`` to the required form.

        Args:
            value (any): Value to parse.

        Returns:
            Parsed value.
        """
        self.validate(value)  # It is necessary to return only valid data
        return value

    def to_struct(self, value):
        """Transform `value` to python structure.

        Args:
            value (any): Value to structurize.

        Returns:
            Structurized value.
        """
        return value

    def validate(self, value):
        """Validate `value`.

        By default use ``self.validate_draft4``.
        """
        return self.validate_draft4(value)

    def validate_draft4(self, value):
        """Validate `value` with JsonSchema draft4.

        Args:
            value (any): Value to validate.

        Returns:
            Return `None`.
            Validation is successful if it was not raise any exception.

        Raises:
            ValidationError: An process of validation errors occurred.
        """
        return self.draft4validator.validate(value)

    @classmethod
    def to_json_schema_draft4(cls):
        """Return JsonSchema definition."""
        return cls.json_schema_draft4


class StringField(BaseField):

    """String type field."""

    types = (str,)
    json_schema_draft4 = {'type': 'string'}


class IntegerField(BaseField):

    """"Integer type field."""

    types = (int,)
    json_schema_draft4 = {'type': 'integer'}


class NumberField(BaseField):

    """Number type field."""

    types = (int, float)
    json_schema_draft4 = {'type': 'number'}
