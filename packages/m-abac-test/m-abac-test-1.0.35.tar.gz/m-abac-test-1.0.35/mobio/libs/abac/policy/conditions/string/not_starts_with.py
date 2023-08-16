"""
    String not starts with conditions
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class NotStartsWith(StringCondition):
    """
        Condition for string `self.what` starts with `value`
    """

    def _is_satisfied(self) -> bool:
        if self.qualifier == self.Qualifier.ForAnyValue:
            for i in self.values:
                if self.case_insensitive:
                    if self.delimiter:
                        if self.what.lower().startswith(i.lower() + self.delimiter) or i.lower() == self.what.lower():
                            return False
                    else:
                        if self.what.lower().startswith(i.lower()):
                            return False
                else:
                    if self.delimiter:
                        if self.what.startswith(i + self.delimiter) or i == self.what:
                            return False
                    else:
                        if self.what.startswith(i):
                            return False
            return True
        else:
            for i in self.values:
                if self.case_insensitive:
                    if self.delimiter:
                        if self.what.lower().startswith(i.lower() + self.delimiter) or i.lower() == self.what.lower():
                            return False
                    else:
                        if self.what.lower().startswith(i.lower()):
                            return False
                else:
                    if self.delimiter:
                        if self.what.startswith(i + self.delimiter) or i == self.what:
                            return False
                    else:
                        if self.what.startswith(i):
                            return False
            return True


class NotStartsWithSchema(StringConditionSchema):
    """
        JSON schema for starts with string condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return NotStartsWith(**data)
