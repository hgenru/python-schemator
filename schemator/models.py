from schemator.fields import BaseField


class Model(object):

    """Base model."""

    def __init__(self, **kwargs):
        """Init.

        Args:
            **kwargs: Dict of values to populate.
        """
        schema = self.__schema__
        for attr_name in dir(schema):
            value = getattr(schema, attr_name, None)
            if isinstance(value, BaseField) and value.default:
                populated = kwargs.pop(attr_name, None)
                field_value = populated if populated else value.default
                setattr(self, attr_name, field_value)
        if kwargs:
            self.populate(**kwargs)

    def __setattr__(self, name, value):
        schema = self.__schema__
        field = getattr(schema, name, None)
        if field:
            parsed_value = field.parse_value(value)
            value = parsed_value
        return super().__setattr__(name, value)

    def populate(self, **kwargs):
        """Populate model.

        Args:
            **kwargs: Dict of values to populate.
        """
        for name, value in kwargs.items():
            setattr(self, name, value)

    def to_struct(self):
        """To structure."""
        schema = self.__schema__
        struct = dict()
        for name in dir(self):
            field = getattr(schema, name, None)
            if field and isinstance(field, BaseField):
                value = getattr(self, name)
                value = field.to_struct(value)
                struct[name] = value
        schema.validate(struct)
        return struct

    def validate(self):
        """Validate model fields."""
        self.to_struct()
