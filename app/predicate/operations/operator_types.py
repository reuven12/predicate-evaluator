from enum import Enum

class OperatorType(str, Enum):
    # unary
    IS_NONE = "isNone"
    IS_NOT_NONE = "isNotNone"
    # binary
    EQ_TO = "eqTo"
    NOT_EQ_TO = "notEqualTo"
    GT = "isGreaterThan"
    LT = "isLessThan"
    # group
    AND = "and"
    OR = "or"
