from enum import Enum, unique


@unique
class FilterTypeEnum(Enum):
    EQUAL = "equal"
    IN = "in"
    NOT = "not"
    NOT_IN = "not_in"

    LESS_THAN = "less_than"
    LESS_THAN_OR_EQUAL = "less_than_or_equal"

    GREATER_THAN = "greater_than"
    GREATER_THAN_OR_EQUAL = "greater_than_or_equal"
