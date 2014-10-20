from inspect import isclass

from schemator.fields import BaseField


class _SchemaMeta(type):

    def __new__(self, cls, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if isclass(attr_value) and issubclass(attr_value, BaseField):
                field = attr_value()
                attrs[attr_name] = field
        return super().__new__(self, cls, bases, attrs)


class Schema(object, metaclass=_SchemaMeta):

    """Base schema class."""

    def get_required(self):
        """Get required fields.

        Returns:
            `List` of required fields name.
        """
        required = []
        for name in dir(self):
            value = getattr(self, name, None)
            if isinstance(value, BaseField) and value.required:
                required.append(name)
        return required
