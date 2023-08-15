"""
Classes and functions using when dealing with data.
"""
from archipelagos.common.protobuf.common.data import AtomicValue_pb2, DataEntry_pb2

from enum import Enum, IntEnum
from typing import List, Any
from datetime import datetime, date
from pandas import Timestamp, Timedelta
import pandas as pd

_is_null_field_name = "isNull"
_fields_field_name = "fields"
_date_field_name = "dateValue"

PYTHON_CLIENT = "Python Client"


def parse_timestamp_str(ts: str) -> Timestamp or None:
    """
    Parses a date/time in YYYY-MM-dd[THH:mm:ss[%f]] format.

    :param ts: The timestamp.
    :type ts: str

    :return: The timestamp representing ts, or None if it could not be parsed.
    :rtype: Timestamp or None
    """
    try:
        return pd.to_datetime(ts, format='%Y-%m-%dT%H:%M:%S.%f')
    except:
        try:
            return pd.to_datetime(ts, format='%Y-%m-%dT%H:%M:%S')
        except:
            try:
                return pd.to_datetime(ts, format='%Y-%m-%d')
            except:
                return None


def get_timestamp_str(ts: Timestamp or datetime or date) -> str:
    """
    Gets a 'yyyy-MM-ddTHH:mm:ss.SSS' str representation of a timestamp.

    :param ts: The timestamp.
    :type ts: Timestamp or datetime or date

    :return: "" if ts is None else the str representation.
    :rtype: str
    """
    return "" if ts is None else ts.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]


class Frequency(IntEnum):
    """
    The different frequencies that data can occur.
    """
    NONE = 0
    ONE_MINUTE = 1
    FIVE_MINUTES = 2
    TEN_MINUTES = 3
    FIFTEEN_MINUTES = 4
    THIRTY_MINUTES = 5
    HOURLY = 6
    DAILY = 7
    WEEKLY = 8
    MONTHLY = 8
    QUARTERLY = 10
    ANNUAL = 11
    BIANNUAL = 12
    IRREGULAR = 13


def is_valid_token(token: str or None) -> bool:
    """
    Used to determine if a string is a valid token.

    :param token: The token.
    :type token: str

    :return: True if token is a valid token, otherwise False.
    :rtype: bool
    """
    if token is None:
        return False
    else:
        len_token = len(token)

        if len_token:
            valid = True

            for ch in token:
                if not str.isdigit(ch) and not str.isalpha(ch) and ('_' != ch) and ('-' != ch):
                    valid = False
                    break

            return valid and len_token <= 30
        else:
            return False


def get_secs_from_timestamp(dt: Timestamp) -> int:
    """
    Used to obtain the secs since the UNIX epoch from a datetime.

    :param dt: The datetime.
    :type dt: datetime

    :return: The number of seconds since the UNIX epoch.
    :rtype: int
    """
    return int((dt - datetime(1970, 1, 1)).total_seconds())


def get_nanos_from_timestamp(dt: Timestamp) -> int:
    """
    Used to obtain the number of nanoseconds within the second represented by dt.

    :param dt: The datetime.
    :type dt: Timestamp

    :return: The number of nanoseconds within the second represented by dt.
    :rtype: int
    """
    return dt.microsecond * 1_000


def get_timestamp(epoch_seconds: int,
                  nanoseconds: int) -> Timestamp:
    """
    Used to obtain the datetime representing a specified number of seconds and nanoseconds since the UNIX epoch.

    :param epoch_seconds: The number of seconds since the UNIX epoch.
    :type epoch_seconds: int

    :param nanoseconds: The number of nanoseconds within epoch_seconds.
    :type nanoseconds: int

    :return: The Timestamp representing epoch_seconds and nanoseconds.
    :rtype: Timestamp
    """
    return Timestamp(epoch_seconds, unit='s') + Timedelta(nanoseconds, unit='ns')


def get_utc_milliseconds(dt: datetime) -> int:
    """
    Gets the number of milliseconds since the UNIX epoch (1/1/1970) for a specified date.

    :param dt: The date/time.
    :type dt: datetime

    :return: The number of milliseconds since the UNIX epoch.
    :rtype: int
    """
    epoch = datetime.utcfromtimestamp(0)
    diff = dt - epoch

    return int(diff.total_seconds() * 1_000 + diff.microseconds // 1_000)


def get_yyyy_mm_dd(dt: date) -> str:
    """
    Returns a string representing a date in YYYY-MM-DD format.

    :param dt: The date.
    :type dt: date

    :return: Representing date in YYYY-MM-DD format.
    :rtype: str
    """
    day = dt.day
    month = dt.month

    return str(dt.year) + "-" + ("0" + str(month) if (month < 10) else str(month)) + "-" + "0" + str(day) if (day < 10)\
        else str(day)


def get_yyyy_mm_dd_hh_mm_ss_n(dt: datetime or Timestamp = None) -> str:
    """
    Returns a string representing a date in YYYY-MM-DDTHH:MM:SS.n format.

    :param dt: The date/time.
    :type dt: datetime or Timestamp

    :return: Representing date in YYYY-MM-DDTHH:MM:SS.n format, or "" if dt was None.
    :rtype: str
    """
    if dt is None:
        return ""
    else:
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%f") + "000"


def get_yyyy_mm_dd_hh_mm_ss(dt: datetime or Timestamp = None) -> str:
    """
    Returns a string representing a date in YYYY-MM-DDTHH:MM:SS format.

    :param dt: The date/time.
    :type dt: datetime or Timestamp

    :return: Representing date in YYYY-MM-DDTHH:MM:SS.n format, or "" if dt was None.
    :rtype: str
    """
    if dt is None:
        return ""
    else:
        return dt.strftime("%Y-%m-%dT%H:%M:%S")


def get_list(items: List[str]) -> str:
    """
    Generates a str containing a comma separate list from a List of str.

    :param items: The list of strings.
    :type items: List[str]

    :return: A comma separate list containing the items in items.
    :rtype: str
    """
    sb = ""
    size = len(items)
    i = 0

    while i < size - 1:
        sb += items[i]
        sb += ", "
        i = i + 1

    sb += items[i]
    return sb


def from_list(comma_separated: str) -> List[str]:
    """
    Generates a list from a string containing the elements of a list separated by commas.

    :param comma_separated: The comma separated list of items.
    :type comma_separated: str

    :return: The list.
    :rtype: List[str]
    """
    to_return = list()

    if comma_separated is not None:
        list_items = comma_separated.split(",")
        to_return.extend(list_items)

    return to_return


def _get_atomic_feature_value(feature_value: Any) -> AtomicValue_pb2.AtomicValue:
    """
    Used to obtain the Protobuf object to represent a feature value that is of an atomic data type.

    :param feature_value: The value of a feature.
    :type feature_value: Any

    :return: The Protobuf object.
    :rtype: AtomicValue_pb2.AtomicValue
    """
    if feature_value is None:
        atomic_value = AtomicValue_pb2.AtomicValue()
        atomic_value.isNull = True
        return atomic_value

    elif isinstance(feature_value, str):
        atomic_value = AtomicValue_pb2.AtomicValue()
        atomic_value.stringValue = feature_value
        return atomic_value

    elif isinstance(feature_value, int):
        atomic_value = AtomicValue_pb2.AtomicValue()
        atomic_value.longValue = feature_value
        return atomic_value

    elif isinstance(feature_value, float):
        atomic_value = AtomicValue_pb2.AtomicValue()
        atomic_value.doubleValue = feature_value
        return atomic_value

    elif isinstance(feature_value, bool):
        atomic_value = AtomicValue_pb2.AtomicValue()
        atomic_value.boolValue = feature_value
        return atomic_value

    elif isinstance(feature_value, date):
        atomic_value = AtomicValue_pb2.AtomicValue()
        dt = datetime.combine(feature_value, datetime.min.time())
        atomic_value.dateValue = get_utc_milliseconds(dt)
        return atomic_value

    elif isinstance(feature_value, bytes):
        atomic_value = AtomicValue_pb2.AtomicValue()
        atomic_value.bytesValue = feature_value
        return atomic_value

    else:
        return None


def _get_feature_value(feature_value: Any) -> Any:
    """
    Used to obtain the Protobuf object to represent a feature value.

    :param feature_value: The value of a feature.
    :type feature_value: Any

    :return: The Protobuf object.
    :rtype: Any
    """
    if isinstance(feature_value, list):
        time_series_entry = DataEntry_pb2.DataEntry()
        time_series_entry.isMap = False
        time_series_entry.isList = True
        time_series_entry.isAtomic = False

        for list_entry in feature_value:
            time_series_entry.listValue.append(_get_feature_value(list_entry))

        return time_series_entry

    elif isinstance(feature_value, dict):
        time_series_entry = DataEntry_pb2.DataEntry()
        time_series_entry.isMap = True
        time_series_entry.isList = False
        time_series_entry.isAtomic = False

        for key in feature_value:
            time_series_entry.mapValue[key].CopyFrom(_get_feature_value(feature_value[key]))

        return time_series_entry

    else:
        atomic_value = _get_atomic_feature_value(feature_value)

        if atomic_value is None:
            raise ValueError("feature_value is not a valid value for a feature")

        else:
            time_series_entry = DataEntry_pb2.DataEntry()
            time_series_entry.isMap = False
            time_series_entry.isList = False
            time_series_entry.isAtomic = True
            time_series_entry.atomicValue.CopyFrom(atomic_value)

            return time_series_entry


def _valid_feature_value(feature_value: Any) -> bool:
    """
    Determines if the value of a feature is valid.

    :param feature_value: The value of a feature.
    :type feature_value: Any

    :return: True if the value of the feature is valid, False otherwise.
    :rtype: bool
    """
    try:
        _get_feature_value(feature_value)
        return True
    except ValueError:
        return False


def _atomic_feature_value_equals(value1: Any,
                                 value2: Any) -> bool:
    """
    Determines if the values of two features containing atomic values are equal.

    :param value1: The 1st feature value.
    :type value1: Any

    :param value2: The 2nd feature value.
    :type value2: Any

    :return: True if the feature values are the same and atomic, False otherwise.
    :rtype: bool
    """
    if value1 is None:
        return value2 is None
    elif isinstance(value1, str) or isinstance(value1, int) or isinstance(value1, float) or isinstance(value1, bool) \
            or isinstance(value1, date) or isinstance(value1, bytes):
        return value1 == value2
    else:
        return False


def _feature_value_equals(value1: Any,
                          value2: Any) -> bool:
    """
    Determines if the values of two features are equal.

    :param value1: The 1st feature value.
    :type value1: Any

    :param value2: The 2nd feature value.
    :type value2: Any

    :return: True if the two values are equals, False otherwise.
    :rtype: bool
    """
    if isinstance(value1, list):
        if isinstance(value2, list):
            if len(value1) != len(value2):
                return False
            else:
                for i, v1 in enumerate(value1):
                    if not _feature_value_equals(v1, value2[i]):
                        return False

                return True
        else:
            return False

    elif isinstance(value1, dict):
        if isinstance(value2, dict):
            if len(value1) != len(value2):
                return False
            else:
                for k1 in value1:
                    if k1 not in value2:
                        return False
                    else:
                        if not _feature_value_equals(value1[k1], value2[k1]):
                            return False

                return True
        else:
            return False
    else:
        return _atomic_feature_value_equals(value1, value2)


def _get_atomic_feature_value_from_proto(feature_value: AtomicValue_pb2.AtomicValue) -> Any or None:
    """
    Used to obtain the value for a feature from a Protobuf object.

    :param feature_value: The protobuf object.
    :type feature_value: AtomicValue_pb2.AtomicValue

    :return: The value for the feature, or None if it has no value.
    :rtype: Any or None
    """
    field_name = feature_value.WhichOneof(_fields_field_name)
    field_value = getattr(feature_value, field_name)

    if field_name == _is_null_field_name:
        return None
    elif field_name == _date_field_name:
        millis = feature_value.dateValue
        secs = millis // 1_000
        nanos = (millis - secs * 1_000) * 1_000_000
        return get_timestamp(secs, nanos).date()
    else:
        return field_value


def _get_feature_value_from_proto(feature_value_proto: DataEntry_pb2.DataEntry) -> Any or None:
    """
    Used to obtain the value for a feature from a Protobuf object.

    :param feature_value_proto: The protobuf object.
    :type feature_value_proto: DataEntry_pb2.DataEntry

    :return: The value for the feature, or None if it has no value.
    :rtype: Any or None
    """
    if feature_value_proto.isMap:
        feature_value_map = {}

        for key in feature_value_proto.mapValue:
            value = feature_value_proto.mapValue[key]
            feature_value_map[key] = _get_feature_value_from_proto(value)

        return feature_value_map

    elif feature_value_proto.isList:
        feature_value_list = []

        for list_entry in feature_value_proto.listValue:
            feature_value_list.append(_get_feature_value_from_proto(list_entry))

        return feature_value_list

    elif feature_value_proto.isAtomic:
        return _get_atomic_feature_value_from_proto(feature_value_proto.atomicValue)

    else:
        raise ValueError("Unrecognised entry type")


class DataType(Enum):
    """
    The different types of data that may be stored in the platform.
    """
    TIME_SERIES = 0
    COLLECTION = 1
    FILE_STORE = 2


def get_data_type_display_str(data_type: DataType) -> str:
    """
    Returns the str that should be used to display a DataType.

    :param data_type: The data type.
    :type data_type: DataType

    :return: str that should be used to display a DataType.
    :rtype: str
    """
    if isinstance(data_type, DataType):
        if data_type == DataType.TIME_SERIES:
            return "time-series"

        elif data_type == DataType.COLLECTION:
            return "collection"

        elif data_type == DataType.FILE_STORE:
            return "file store"

        else:
            return ""
    else:
        return ""


class DatasetId:
    """
    Represents the ID for a dataset.
    """
    def __init__(self,
                 data_type: DataType,
                 source: str,
                 category: str,
                 label: str):
        """
        :param data_type: The DataType for the dataset.
        :type data_type: DataType

        :param source: The source for the dataset.
        :type source: str

        :param category: The category for the dataset.
        :type category: str

        :param label: The label for the dataset.
        :type label: str
        """
        # Check the arguments

        if not isinstance(data_type, DataType):
            raise ValueError(f'The data type "{data_type}" is not valid')

        if not is_valid_token(source):
            raise ValueError(f'The source "{source}" is not a valid token')

        if not is_valid_token(category):
            raise ValueError(f'The category "{category}" is not a valid token')

        if not is_valid_token(label):
            raise ValueError(f'The label "{label}" is not a valid token')

        # Create the object

        self._data_type = data_type
        self._source = source
        self._category = category
        self._label = label

        self._hash_code = 0
        self._build_hash_code()

    def _build_hash_code(self):
        """
        Builds and caches the hash code associated with this.
        """
        prime = 31
        result = 1
        result = prime * result + (0 if self._source is None else hash(self._data_type.name))
        result = prime * result + (0 if self._source is None else hash(self._source))
        result = prime * result + (0 if self._category is None else hash(self._category))
        result = prime * result + (0 if self._label is None else hash(self._label))
        self._hash_code = result

    @property
    def data_type(self) -> DataType:
        """
        The DataType for the data.
        """
        return self._data_type

    @property
    def source(self) -> str:
        """
        The source for the data.
        """
        return self._source

    @property
    def category(self) -> str:
        """
        The category for the data.
        """
        return self._category

    @property
    def label(self) -> str:
        """
        The label for the data.
        """
        return self._label

    def __eq__(self, other):
        """
        """
        if other is DatasetId:
            if self._data_type is None:
                if other.data_type is None:
                    return False
            else:
                if self._data_type != other.data_type:
                    return False

            if self._source is None:
                if other.source is None:
                    return False
            else:
                if self._source != other.source:
                    return False

            if self._category is None:
                if other.category is None:
                    return False
            else:
                if self._category != other.category:
                    return False

            if self._label is None:
                if other.label is None:
                    return False
            else:
                if self._label != other.label:
                    return False

            return True

        else:
            return False

    def __hash__(self) -> int:
        """
        """
        return self._hash_code

    def __str__(self):
        """
        """
        to_return = ""

        to_return += "DataType = \""
        to_return += self._data_type
        to_return += "Source = \""
        to_return += self._source
        to_return += "\", Category = \""
        to_return += self._category
        to_return += "\", Label = \""
        to_return += self._label
        to_return += "\""

        return to_return


def parse_bool_str(value: str) -> bool:
    """
    Parses a str to return a bool.

    :param value: The str to parse.
    :type value: str

    :return: The Boolean.
    :rtype: bool
    """
    value_lower = value.lower()

    if value_lower == "true":
        return True

    elif value_lower == "false":
        return False

    else:
        raise ValueError(f"Unrecognised str '{value}'")


class DataProperties:
    """
    The (optional) properties that a dataset (time-series, collection, file store...) may have.
    """
    WEBSITE = 'Website'
    URI = 'URI'
    LICENCE = 'Licence'
    LICENCE_URL = 'Licence-URL'
    INGESTED = 'Ingested'
    COPYRIGHT = 'Copyright'
    COPYRIGHT_URL = 'Copyright-URL'
    LONGITUDE = 'Longitude'
    LATITUDE = 'Latitude'


class DataLicence:
    """
    The different licences that may be associated with datasets.
    """
    FREE_LICENCE = 'Free for personal and commercial use'
    APACHE_2_LICENCE = 'Apache License, Version 2.0'
    APACHE_2_LICENCE_URL = 'https://www.apache.org/licenses/LICENSE-2.0'
    MIT_LICENCE = 'MIT License'
    MIT_LICENCE_URL = 'http://opensource.org/licenses/MIT'
    CREATIVE_COMMONS_4_LICENCE = 'Creative Commons Attribution 4.0 International License'
    CREATIVE_COMMONS_4_LICENCE_URL = 'https://creativecommons.org/licenses/by/4.0'
