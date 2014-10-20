from schemator import errors


class BaseField(object):

    """Base field class.

    Attributes:
        required (bool): Do require this field or not.
        default (any): Computed default value.
    """

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
            Structurize value.
        """
        return value

    def validate(self, value):
        """Validate `value`.

        Args:
            value (any): Value to validate.

        Returns:
            Return `None`.
            Validation is successful if it was not raise any exception.

        Raises:
            ValidationError: An process of validation errors occurred.
        """
        # TODO: Посмотреть что лучше отдавать.
        return True


class BuiltInTypesField(BaseField):

    """Built-in types field.

    Attributes:
        types (tuple): Supported types.
    """

    types = tuple()

    def parse_value(self, value):
        self.validate(value)
        return value

    def validate(self, value):
        if isinstance(value, self.types):
            return True
        raise errors.ValidationError()


class StringField(BuiltInTypesField):

    """String type field."""

    types = (str,)


class IntegerField(BuiltInTypesField):

    """"Integer type field."""

    types = (int,)


class FloatField(BuiltInTypesField):

    """Float type field."""

    types = (float,)


class NumberField(BuiltInTypesField):

    """Number type field."""

    types = (int, float)
