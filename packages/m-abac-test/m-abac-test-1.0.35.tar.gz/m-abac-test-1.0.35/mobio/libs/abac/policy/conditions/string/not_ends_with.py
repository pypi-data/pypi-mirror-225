"""
    String not ends with conditions
"""

from marshmallow import post_load

from .base import StringCondition, StringConditionSchema


class NotEndsWith(StringCondition):
    """
        Condition for string `self.what` ends with `value`
    """

    def _is_satisfied(self,) -> bool:
        if self.qualifier == self.Qualifier.ForAnyValue:
            for i in self.values:
                if self.case_insensitive:
                    if self.delimiter:
                        if self.what.lower().endswith(self.delimiter + i.lower()) or i.lower() == self.what.lower():
                            return False
                    else:
                        if self.what.lower().endswith(i.lower()):
                            return False
                else:
                    if self.delimiter:
                        if self.what.endswith(self.delimiter + i) or i == self.what:
                            return False
                    else:
                        if self.what.endswith(i):
                            return False
            return True
        else:
            for i in self.values:
                if self.case_insensitive:
                    if self.delimiter:
                        if self.what.lower().endswith(self.delimiter + i.lower()) or i.lower() == self.what.lower():
                            return False
                    else:
                        if self.what.lower().endswith(i.lower()):
                            return False
                else:
                    if self.delimiter:
                        if self.what.endswith(self.delimiter + i) or i == self.what:
                            return False
                    else:
                        if self.what.endswith(i):
                            return False
            return True


class NotEndsWithSchema(StringConditionSchema):
    """
        JSON schema for ends with string condition
    """

    @post_load
    def post_load(self, data, **_):  # pylint: disable=missing-docstring,no-self-use
        # self.validate(data)
        return NotEndsWith(**data)
