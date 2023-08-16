import csv
import re

from ul_api_utils.const import CRON_EXPRESSION_VALIDATION_REGEX, MIN_UTC_OFFSET_SECONDS, MAX_UTC_OFFSET_SECONDS
from typing import TypeVar, Generic, List, Union, Generator, Callable
from pydantic import ValidationError, ConstrainedStr, ConstrainedInt, ConstrainedList
from pydantic.fields import ModelField


class NotEmptyList(ConstrainedList):
    """Type that can be used in pydantic field, that will validate empty lists."""
    min_items = 1


class CronScheduleStr(ConstrainedStr):
    """Type that can be used in pydantic field, that will validate cron-formatted strings."""
    regex = re.compile(CRON_EXPRESSION_VALIDATION_REGEX)


class WhiteSpaceStrippedStr(ConstrainedStr):
    """Type that can be used in pydantic field, that will strip whitespaces strings."""
    strip_whitespace = True


class UTCOffsetSeconds(ConstrainedInt):
    """Type that can be used for pydantic fields to represent the offset from UTC."""
    ge = MIN_UTC_OFFSET_SECONDS
    le = MAX_UTC_OFFSET_SECONDS


class PgTypePasswordStr(ConstrainedStr):
    """Type that can be used for pydantic fields to represent password with length from 6 to 72 characters."""
    min_length = 6
    max_length = 72


class PgTypeShortStr(ConstrainedStr):
    """Type that can be used for pydantic fields to represent short string with length from 0 to 255 characters."""
    min_length = 0
    max_length = 255


class PgTypeLongStr(ConstrainedStr):
    """Type that can be used for pydantic fields to represent short string with length from 0 to 1000 characters."""
    min_length = 0
    max_length = 1000


class PgTypeInt32(ConstrainedInt):
    """Type that can be used for pydantic fields to represent int32 number."""
    ge = -2147483648
    lt = 2147483648


class PgTypePositiveInt32(ConstrainedInt):
    """Type that can be used for pydantic fields to represent positive int32 number."""
    ge = 0
    lt = 2147483648


class PgTypeInt16(ConstrainedInt):
    """Type that can be used for pydantic fields to represent int16 (SMALLINT) number."""
    ge = -32768
    lt = 32768


class PgTypePositiveInt16(ConstrainedInt):
    """Type that can be used for pydantic fields to represent positive int16 (SMALLINT) number."""
    ge = 0
    lt = 32768


QueryParamsSeparatedListValueType = TypeVar('QueryParamsSeparatedListValueType')


class QueryParamsSeparatedList(Generic[QueryParamsSeparatedListValueType]):
    """
    Supports cases when query parameters are being sent as a string, but you have to assume
    that it is a list.

    F.E. Query string is ?foo=1,2

    Note:
        Sent as a string, but interpreted as List.
    """

    def __init__(self, contains_type: QueryParamsSeparatedListValueType) -> None:
        self.contains_type = contains_type

    def __repr__(self) -> str:
        return f'QueryParamsSeparatedList({super().__repr__()})'

    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[Union[List[str], str], ModelField], Union[List[QueryParamsSeparatedListValueType], List[str]]], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, query_param: Union[List[str], str], field: ModelField) -> Union[List[QueryParamsSeparatedListValueType], List[str]]:
        if not isinstance(query_param, List):
            query_param = [query_param]
        reader = csv.reader(query_param, skipinitialspace=True)
        splitted = next(reader)
        if not field.sub_fields:
            return splitted
        list_item = field.sub_fields[0]  # retrieving info about data type of the list
        errors = []
        for value in splitted:
            validated_list_item, error = list_item.validate(value, {}, loc="separated query param")
            if error:
                errors.append(error)
        if errors:
            raise ValidationError(errors, cls)  # type: ignore
        # Validation passed without errors, modify string to a list and cast the right type for every element
        return [list_item.type_(value) for value in splitted]
