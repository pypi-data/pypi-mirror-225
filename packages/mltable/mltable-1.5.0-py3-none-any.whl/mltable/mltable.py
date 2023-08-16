# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""
Contains functionality to create and interact with MLTable objects
"""
import atexit
import os
import re
import yaml
from enum import Enum, auto
import random
import tempfile
import urllib.parse
import hashlib
from typing import List, Optional, Union
import pathlib

from azureml.dataprep.api._loggerfactory import track, _LoggerFactory
from azureml.dataprep.api._constants import ACTIVITY_INFO_KEY, ERROR_CODE_KEY, \
    COMPLIANT_MESSAGE_KEY, OUTER_ERROR_CODE_KEY
from azureml.dataprep.api._dataframereader import get_dataframe_reader, to_pyrecords_with_preppy, \
    _execute
from azureml.dataprep.api.mltable._mltable_helper import _download_mltable_yaml, _parse_path_format, _PathType, \
    _is_tabular, _read_yaml
from azureml.dataprep.rslex import PyRsDataflow
from azureml.dataprep.api.typeconversions import FieldType
from azureml.dataprep.api._rslex_executor import ensure_rslex_environment
from azureml.dataprep import UserErrorException
from azureml.dataprep.api.mltable._validation_and_error_handler import _reclassify_rslex_error, \
    _wrap_rslex_function_call

from ._aml_utilities._aml_rest_client_helper import _get_data_asset_by_id, _get_data_asset_by_asset_uri, \
    _try_resolve_workspace_info, _has_sufficient_workspace_info, STORAGE_OPTION_KEY_AZUREML_SUBSCRIPTION, \
    STORAGE_OPTION_KEY_AZUREML_RESOURCEGROUP, STORAGE_OPTION_KEY_AZUREML_WORKSPACE
from ._utils import _validate, _make_all_paths_absolute, _parse_workspace_context_from_longform_uri, _is_local_path, \
    _PATHS_KEY, MLTableYamlCleaner, _prepend_file_handler, _starts_with_file_handler, _is_remote_path, \
    _remove_file_handler
from ._validation_and_error_handler import _validate_downloads


try:
    from pkg_resources import get_distribution

    mltable_version = get_distribution('mltable').version
    _LoggerFactory.add_default_custom_dimensions({'MLTableVersion': mltable_version})
except Exception:
    pass

_APP_NAME = 'MLTable'
_PUBLIC_API = 'PublicApi'
_INTERNAL_API = 'InternalCall'
_TRAITS_SECTION_KEY = 'traits'
_INDEX_COLUMNS_KEY = 'index_columns'
_TIMESTAMP_COLUMN_KEY = 'timestamp_column'
_TRAITS_SCHEMA_NAME = 'traits'
_METADATA_SCHEMA_NAME = 'metadata'
_TRANSFORMATIONS_SCHEMA_KEY = 'transformations'
_logger = None

# keys for MLTable sections
_EXTRACT_PARTITION_FORMAT_KEY = 'extract_columns_from_partition_format'
_PARTITION_FORMAT_KEY = 'partition_format'
_READ_DELIMITED_KEY = 'read_delimited'
_READ_JSON_KEY = 'read_json_lines'

_AML_DATASTORE_URI_PATTERN = None
_AZURE_DATA_LAKE_GEN_1_URI_PATTERN = None
_AZURE_DATA_LAKE_GEN_2_URI_PATTERN = None
_AZURE_BLOB_STORAGE_URI_PATTERN = None
_HTTPS_URI_PATTERN = None

_SIMPLE_TYPES = {
    FieldType.INTEGER: 'int',
    FieldType.BOOLEAN: 'boolean',
    FieldType.STRING: 'string',
    FieldType.DECIMAL: 'float',
    FieldType.DATE: 'datetime',
    FieldType.STREAM: 'stream_info'
}


def _get_logger():
    global _logger
    if _logger is None:
        _logger = _LoggerFactory.get_logger(__name__)
    return _logger


# force to flush app insights at exit
# logs might not be flushed to app insight because of app insight buffer
def _exit_handler():
    for handler in _get_logger().handlers:
        handler.flush()


atexit.register(_exit_handler)


def _log_exception(activity_logger, exception):
    if hasattr(activity_logger, ACTIVITY_INFO_KEY):
        activity_logger.activity_info['message'] = getattr(exception, COMPLIANT_MESSAGE_KEY, '')
        activity_logger.activity_info['error_code'] = getattr(exception, ERROR_CODE_KEY, '')
        activity_logger.activity_info['outer_error_code'] = getattr(exception, OUTER_ERROR_CODE_KEY, '')


class MLTablePartitionSize(Enum):
    """
    Helper enum representing the memory allocated for reading various partitions for select file formats across
    different memory units. Currently used when reading delimited or JSON lines files.

    Supports bytes, kilobytes, megabytes, and gigabytes as memory units - in binary.
    """
    byte = 0
    kilobyte = 1
    megabyte = 2
    gigabyte = 3

    @staticmethod
    def _parse(partition_size, unit):
        if not (isinstance(partition_size, int) and partition_size > 0):
            raise UserErrorException('Expect `partition_size` to be a positive int.')

        if isinstance(unit, str):
            unit = unit.lower()

        if unit in ('b', 'byte', MLTablePartitionSize.byte):
            unit = MLTablePartitionSize.byte
        elif unit in ('kb', 'kilobyte', MLTablePartitionSize.kilobyte):
            unit = MLTablePartitionSize.kilobyte
        elif unit in ('mb', 'megabyte', MLTablePartitionSize.megabyte):
            unit = MLTablePartitionSize.megabyte
        elif unit in ('gb', 'gigabyte', MLTablePartitionSize.gigabyte):
            unit = MLTablePartitionSize.gigabyte
        else:
            raise UserErrorException("Expect `partition_size` unit to be a mltable.MLTablePartitionSizeUnit or "
                                     "string where a string is one of 'b', 'byte', 'kb', 'kilobyte', 'mb', "
                                     "'megabyte', 'gb', or 'gigabyte'.")

        return partition_size * (1024 ** unit.value)


class MLTableHeaders(Enum):
    """
    Defines options for how column headers are processed when reading data
    from files to create a MLTable.

    These enumeration values are used in the MLTable class.
    """
    #: No column headers are read
    no_header = auto()
    #: Read headers only from first row of first file, everything else is data.
    from_first_file = auto()
    #: Read headers from first row of each file, combining named columns.
    all_files_different_headers = auto()
    #: Read headers from first row of first file, drops first row from other files.
    all_files_same_headers = auto()

    @staticmethod
    def _parse(header):
        if isinstance(header, MLTableHeaders):
            return header

        if not isinstance(header, str):
            raise UserErrorException('The header should be a string or an MLTableHeader enum')

        try:
            return MLTableHeaders[header.lower()]
        except KeyError:
            raise UserErrorException(f"Given invalid header {str(header)}, supported headers are: 'no_header', "
                                     "'from_first_file', 'all_files_different_headers', and 'all_files_same_headers'.")


class MLTableFileEncoding(Enum):
    """
    Defines options for how encoding are processed when reading data from
    files to create a MLTable.

    These enumeration values are used in the MLTable class.
    """
    utf8 = auto()
    iso88591 = auto()
    latin1 = auto()
    ascii = auto()
    utf16 = auto()
    utf8bom = auto()
    windows1252 = auto()

    @staticmethod
    def _parse(encoding):
        if isinstance(encoding, MLTableFileEncoding):
            return encoding
        if not isinstance(encoding, str):
            raise UserErrorException('The encoding should be a string or an MLTableFileEncoding enum')

        if encoding in ("utf8", "utf-8", "utf-8 bom"):
            return MLTableFileEncoding.utf8
        if encoding in ("iso88591", "iso-8859-1"):
            return MLTableFileEncoding.iso88591
        if encoding in ("latin1", "latin-1"):
            return MLTableFileEncoding.latin1
        if encoding == "ascii":
            return MLTableFileEncoding.ascii
        if encoding in ("windows1252", "windows-1252"):
            return MLTableFileEncoding.windows1252

        raise UserErrorException(f"""Given invalid encoding '{encoding}', supported encodings are:
                                 - utf8 as "utf8", "utf-8", "utf-8 bom"
                                 - iso88591 as "iso88591" or "iso-8859-1"
                                 - latin1 as "latin1" or "latin-1"
                                 - utf16 as "utf16" or "utf-16"
                                 - windows1252 as "windows1252" or "windows-1252\"""")


class DataType:
    """
    Helper class for handling the proper manipulation of supported column types (int, bool, string, etc.).
    Currently used  with `MLTable.convert_column_types(...)` & `from_delimited_files(...)` for specifying which types
    to convert columns to. Different types are selected with `DataType.from_*(...)` methods.
    """

    _MISMATCH_AS_TYPES = ('error', 'true', 'false')

    @staticmethod
    def _from_raw(value):
        if isinstance(value, DataType):
            return value
        if value == 'string':
            return DataType.to_string()
        if value == 'int':
            return DataType.to_int()
        if value == 'float':
            return DataType.to_float()
        if value == 'boolean':
            return DataType.to_bool()
        if value == 'stream_info':
            return DataType.to_stream()
        raise UserErrorException(f"'{value}' is not a supported string conversion for `mltable.DataType`, "
                                 "supported types are 'string', 'int', 'float', 'boolean', & 'stream_info'")

    @staticmethod
    def _create(data_type):
        dt = DataType()
        dt._data_type = data_type
        dt._arguments = _SIMPLE_TYPES.get(data_type)
        return dt

    @staticmethod
    def _format_str_list(values, var_name):
        if values:
            if not isinstance(values, list):
                values = [values]
            if not all(isinstance(x, str) for x in values):
                raise UserErrorException(f'`{var_name}` must be a non-empty list of strings or None')
            if len(values) == 0:
                values = None
        return values

    @staticmethod
    def to_string():
        """Configure conversion to string."""
        return DataType._create(FieldType.STRING)

    @staticmethod
    def to_int():
        """Configure conversion to 64-bit integer."""
        return DataType._create(FieldType.INTEGER)

    @staticmethod
    def to_float():
        """Configure conversion to 64-bit float."""
        return DataType._create(FieldType.DECIMAL)

    @staticmethod
    def to_bool(true_values: Optional[List[str]] = None,
                false_values: Optional[List[str]] = None,
                mismatch_as: Optional[str] = None):
        """
        Configure conversion to bool. `true_values` & `false_values` must both be None or non-empty lists of,
        string else an error will be thrown.

        :param true_values: List of values in dataset to designate as True.
            For example, ['1', 'yes'] will be replaced as [True, True].
            The true_values need to be present in the dataset otherwise None will be returned for values not present.
        :type true_values: builtin.list[str]

        :param false_values: List of values in dataset to designate as False.
            For example, ['0', 'no'] will be replaced as [False, False].
            The false_values need to be present in the dataset otherwise None will be returned for values not present.
        :type false_values: builtin.list[str]

        :param mismatch_as: How cast strings that are neither in `true_values` or `false_values`; 'true' casts all as
            True, 'false' as False, and 'error' will error instead of casting. Defaults to None which equal to 'error'.
        :type mismatch_as: Optional[str]
        """
        dt = DataType._create(FieldType.BOOLEAN)

        if mismatch_as is not None and mismatch_as not in DataType._MISMATCH_AS_TYPES:
            raise UserErrorException(f"`mismatch_as` can only be {DataType._MISMATCH_AS_TYPES}")

        true_values = DataType._format_str_list(true_values, 'true_values')
        false_values = DataType._format_str_list(false_values, 'false_values')

        if (true_values is None) != (false_values is None):
            raise UserErrorException('`true_values` and `false_values` must both be None or non-empty list of strings')

        if true_values is not None and false_values is not None \
                and (len(set(true_values).intersection(false_values)) > 0):
            raise UserErrorException('`true_values` and `false_values` can not have overlapping values')

        type_name = dt._arguments
        args = {type_name: {}}
        if true_values and false_values:
            args[type_name]['true_values'] = true_values
            args[type_name]['false_values'] = false_values
            args[type_name]['mismatch_as'] = 'error'

        if mismatch_as:
            args[type_name]['mismatch_as'] = mismatch_as

        dt._arguments = args if args[type_name] else type_name
        return dt

    @staticmethod
    def to_stream():
        """Configure conversion to stream."""
        return DataType._create(FieldType.STREAM)

    @staticmethod
    def to_datetime(formats: Union[str, List[str]], date_constant: Optional[str] = None):
        """
        Configure conversion to datetime.

        :param formats: Formats to try for datetime conversion. For example `%d-%m-%Y` for data in "day-month-year",
            and `%Y-%m-%dT%H:%M:%S.%f` for "combined date and time representation" according to ISO 8601.

            * %Y: Year with 4 digits

            * %y: Year with 2 digits

            * %m: Month in digits

            * %b: Month represented by its abbreviated name in 3 letters, like Aug

            * %B: Month represented by its full name, like August

            * %d: Day in digits

            * %H: Hour as represented in 24-hour clock time

            * %I: Hour as represented in 12-hour clock time

            * %M: Minute in 2 digits

            * %S: Second in 2 digits

            * %f: Microsecond
            * %p: AM/PM designator

            * %z: Timezone, for example: -0700
        :type formats: str or builtin.list[str]

        :param date_constant: If the column contains only time values, a date to apply to the resulting DateTime.
        :type date_constant: Optional[str]
        """
        dt = DataType._create(FieldType.DATE)
        type_name = _SIMPLE_TYPES.get(FieldType.DATE)

        if isinstance(formats, str):
            formats = [formats]
        elif not (isinstance(formats, (list, tuple)) and len(formats) > 0 and all(isinstance(x, str) for x in formats)):
            raise UserErrorException(
                'Expect `columns` to be a single string, a non-empty list of strings, or a non-empty tuple of strings')

        dt._arguments = {type_name: {'formats': formats}}
        if date_constant is not None:
            dt._arguments[type_name]['date_constant'] = date_constant
        return dt


def _get_logger():
    global _logger
    if _logger is None:
        _logger = _LoggerFactory.get_logger(__name__)
    return _logger


# force to flush app insights at exit
# logs might not be flushed to app insight because of app insight buffer
def _exit_handler():
    for handler in _get_logger().handlers:
        handler.flush()


atexit.register(_exit_handler)


def _check_no_dup_cols(cols):
    """
    Raises a UserErrorException is there are any duplicate columns in the given list of column groups (single of
    multiple columns.
    :param cols:
    :type cols: dict[Union[str, tuple[str]], Union[str, mltable.DataType]]
    :return: None
    :rtype: None
    """
    seen_columns = set()
    for group in cols:
        if isinstance(group, str):
            group = (group,)

        for column in group:
            if column in seen_columns:
                raise UserErrorException(
                    f"Found duplicate column. Cannot convert column '{column}' to multiple `mltable.DataType`s.")

        seen_columns.update(group)


def _process_column_to_type_mappings(col_to_type_mappings, allow_stream_info=True):
    if not isinstance(col_to_type_mappings, dict) or len(col_to_type_mappings) == 0:
        raise UserErrorException('Expected a non-empty dict[Union[str, tuple[str]], Union[str, mltable.DataType]]')

    _check_no_dup_cols(col_to_type_mappings)

    def process_col_type(col, col_type):
        if not (isinstance(col, str) or (isinstance(col, tuple) and all(isinstance(x, str) for x in col))):
            raise UserErrorException('Expect dictionary keys to be strings or tuples of strings.')

        col_type = DataType._from_raw(col_type)
        if not allow_stream_info and col_type._data_type == FieldType.STREAM:
            raise UserErrorException(
                'Type overrides to stream are not supported, try mltable.MLTable.convert_column_types instead')

        return {'columns': col, 'column_type': col_type._arguments}

    return [process_col_type(col, col_type) for col, col_type in col_to_type_mappings.items()]


def _load_mltable_from_legacy_dataset(asset_id, storage_options=None):
    # only expect asset id in remote job in prod + local e2e test scenario
    asset = _get_data_asset_by_id(asset_id, storage_options)
    mltable_string = asset.legacy_dataflow
    if not mltable_string or mltable_string == '':
        raise RuntimeError(f'Data asset service returned invalid MLTable yaml for asset {asset_id}')
    mltable_yaml_dict = yaml.safe_load(mltable_string)

    if _PATHS_KEY in mltable_yaml_dict:
        first_path = list(mltable_yaml_dict[_PATHS_KEY][0].values())[0]
        regex = re.compile(r'^(azureml:\/\/.*datastores\/.*\/paths\/).*$')
        matches = regex.match(first_path)
        load_uri = matches.group(1)
    else:
        load_uri = None

    return mltable_yaml_dict, load_uri



def _load_mltable_from_data_asset_uri(asset_uri_match, storage_options=None, enable_validation=True):
    # asset uri can be from local or remote
    data_asset = _get_data_asset_by_asset_uri(asset_uri_match, storage_options)
    is_v2 = data_asset.additional_properties['isV2']
    data_uri = data_asset.data_version.data_uri
    if is_v2:
        if data_asset.data_version.data_type != _APP_NAME:
            raise UserErrorException('Can only load MLTable type asset')
        local_path = _download_mltable_yaml(data_asset.data_version.data_uri)
        mltable_dict = _read_yaml(local_path)
        mltable_dict, og_path_dict = _make_all_paths_absolute(mltable_dict, data_asset.data_version.data_uri)
        if enable_validation:
            _validate(mltable_dict)
    else:
        mltable_string = data_asset.additional_properties['legacyDataflow']
        if not mltable_string:
            raise RuntimeError('Data asset service returned invalid MLTable YAML file for asset '
                            f'{asset_uri_match[3]}:{asset_uri_match[4]}')
        mltable_dict = yaml.safe_load(mltable_string)
        og_path_dict = None

    return mltable_dict, data_uri, og_path_dict


@track(_get_logger,activity_type=_PUBLIC_API, custom_dimensions={'app_name': _APP_NAME})
def load(uri, storage_options: dict = None):
    """
    Loads the MLTable file (YAML) present at the given uri.

    .. remarks::

        There must be a valid MLTable YAML file named 'MLTable' present at
        the given uri.

        .. code-block:: python

            # load mltable from local folder
            from mltable import load
            tbl = load('.\\samples\\mltable_sample')

            # load mltable from azureml datastore uri
            from mltable import load
            tbl = load(
                'azureml://subscriptions/<subscription-id>/
                resourcegroups/<resourcegroup-name>/workspaces/<workspace-name>/
                datastores/<datastore-name>/paths/<mltable-path-on-datastore>/')

            # load mltable from azureml data asset uri
            from mltable import load
            tbl = load(
                  'azureml://subscriptions/<subscription-id>/
                  resourcegroups/<resourcegroup-name>/providers/Microsoft.MachineLearningServices/
                  workspaces/<workspace-name>/data/<data-asset-name>/versions/<data-asset-version>/')

    `storage_options` supports keys of 'subscription', 'resource_group',
    'workspace', or 'location'. All must locate an Azure machine learning
    workspace.

    :param uri: uri supports long-form datastore uri, storage uri, local path,
                or data asset uri
    :type uri: str
    :param storage_options: AML workspace info when URI is an AML asset
    :type storage_options: dict[str, str]
    :return: MLTable
    :rtype: mltable.MLTable
    """
    return _load(uri, storage_options, True)


@track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
def _load(uri, storage_options: dict = None, enable_validate=False):
    """
    Loads the MLTable file (YAML) present at the given uri. This is private api without validations compare to load()
    """
    custom_dimensions = {'app_name': _APP_NAME}
    workspace_context = _parse_workspace_context_from_longform_uri(uri)
    if workspace_context:
        custom_dimensions.update(workspace_context)

    try:
        og_path_pairs = None
        path_type, base_path, match = _parse_path_format(uri)
        if path_type == _PathType.local:
            base_path = os.path.abspath(base_path)
            mltable_dict = _read_yaml(base_path)
            load_uri = os.path.normpath(uri)
            if enable_validate:
                _validate(mltable_dict)
        elif path_type == _PathType.cloud:
            local_path = _download_mltable_yaml(uri)
            mltable_dict = _read_yaml(local_path)
            load_uri = uri
            if enable_validate:
                _validate(mltable_dict)
        elif path_type == _PathType.legacy_dataset:
            # skip mltable yaml validation for v1 legacy dataset
            # because of some legacy schema generated in converter
            mltable_dict, load_uri = _load_mltable_from_legacy_dataset(uri, storage_options)
            # this is to skip path conversion logic, all paths will be absolute path
            base_path = None
        elif path_type == _PathType.data_asset_uri:
            # map load_uri to what was actually used to fetch MLTable
            mltable_dict, load_uri, og_path_pairs \
                = _load_mltable_from_data_asset_uri(match, storage_options, enable_validate)
            # path has been mapped to absolute path in _load_mltable_from_data_asset_uri
            base_path = None
        else:
            raise UserErrorException(
                'The uri should be a valid path to a local or cloud directory which contains an MLTable file.')
        # v1 sql dataset doesnt have paths
        if og_path_pairs is None:  # may have been set in _load_mltable_from_data_asset_uri
            mltable_dict, og_path_pairs = _make_all_paths_absolute(mltable_dict, base_path)
        mltable_loaded = MLTable._create_from_dict(mltable_yaml_dict=mltable_dict,
                                                    path_pairs=og_path_pairs,
                                                    load_uri=load_uri)
        mltable_loaded._workspace_context = _parse_workspace_context_from_longform_uri(load_uri)
        _LoggerFactory.trace(_get_logger(), "load", workspace_context)
        return mltable_loaded
    except Exception as ex:
        _reclassify_rslex_error(ex)


@track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
def from_delimited_files(paths, header='all_files_same_headers', delimiter=",", support_multi_line=False,
                         empty_as_string=False, encoding='utf8', include_path_column=False, infer_column_types=True):
    """
    Creates a MLTable from the given list of delimited files.

    .. remarks::

        There must be a valid paths string.

        .. code-block:: python

            # load mltable from local delimited file
            from mltable import from_delimited_files
            paths = [{"file": "./samples/mltable_sample/sample_data.csv"}]
            mltable = from_delimited_files(paths)

    :param paths: Paths supports files or folders with local or cloud paths. Relative local file paths are assumed to be
        relative to the current working directory. If the parent directory a local file path is relative to is not the
        current working directory, instead recommend passing that path as a absolute file path.
    :type paths: list[dict[str, str]]
    :param header: How column headers are handled when reading from files. Options specified using the enum
        :class:`mltable.MLTableHeaders`. Supported headers are 'no_header', 'from_first_file',
        'all_files_different_headers', and 'all_files_same_headers'.
    :type header: typing.Union[str, mltable.MLTableHeaders]
    :param delimiter: separator used to split columns
    :type delimiter: str
    :param support_multi_line: If False, all line breaks, including those in quoted field values, will be interpreted
        as a record break. Reading data this way is faster and more optimized for parallel execution on multiple CPU
        cores. However, it may result in silently producing more records with misaligned field values. This should be
        set to True when the delimited files are known to contain quoted line breaks.

        .. remarks::

            Given this csv file as example, the data will be read differently
            based on support_multi_line.

                A,B,C
                A1,B1,C1
                A2,"B
                2",C2

            .. code-block:: python

                from mltable import from_delimited_files

                # default behavior: support_multi_line=False
                mltable = from_delimited_files(path)
                print(mltable.to_pandas_dataframe())
                #      A   B     C
                #  0  A1  B1    C1
                #  1  A2   B  None
                #  2  2"  C2  None

                # to handle quoted line breaks
                mltable = from_delimited_files(path, support_multi_line=True)
                print(mltable.to_pandas_dataframe())
                #      A       B   C
                #  0  A1      B1  C1
                #  1  A2  B\\r\\n2  C2

    :type support_multi_line: bool
    :param empty_as_string: How empty fields should be handled. If True will read empty fields as empty strings, else
        read as nulls. If True and column contains datetime or numeric data, empty fields still read as nulls.
    :type empty_as_string: bool
    :param encoding: Specifies the file encoding using the enum :class:`mltable.MLTableFileEncoding`. Supported
                     encodings are:
                     - utf8 as "utf8", "utf-8", "utf-8 bom"
                     - iso88591 as "iso88591" or "iso-8859-1"
                     - latin1 as "latin1" or "latin-1"
                     - utf16 as "utf16" or "utf-16"
                     - windows1252 as "windows1252" or "windows-1252"
    :type encoding: typing.Union[str, mltable.MLTableFileEncoding]
    :param include_path_column: Keep path information as a column in the MLTable, is useful when reading multiple files
        and you want to know which file a particular record came from, or to keep useful information that may be stored
        in a file path.
    :type include_path_column: bool
    :param infer_column_types: If True, automatically infers all column types. If False, leaves columns as strings. If
        a dictionary, represents columns whose types are to be set to given types (with all other columns being
        inferred). The dictionary may contain a key named `sample_size` mapped to a positive integer number,
        representing the number of rows to use for inferring column types. The dictionary may also contain a key named
        'column_type_overrides'. Each key in the dictionary is either a string representing a column name or a tuple
        of strings representing a group of column names. Each value is either a string (one of 'boolean', 'string',
        'float', or 'int') or a :class:`mltable.DataType`. mltable.DataType.to_stream() is not supported. If an empty
        dictionary is given, assumed to be True. Defaults to True.

        .. remarks::

            An example of how to format `infer_column_types`.

            .. code-block:: python

                from mltable import from_delimited_files

                # default behavior: support_multi_line=False
                mltable = from_delimited_files(paths, infer_column_types={
                    'sample_size': 100,
                    'column_type_overrides': {
                        'colA': 'boolean'
                        ('colB', 'colC'): DataType.to_int()
                    }
                })

    :type infer_column_types:
        typing.Union[bool, dict[str, typing.Union[str, dict[typing.Union[typing.Tuple[str], str], mltable.DataType]]]
    :return: MLTable object
    :return: MLTable
    :rtype: mltable.MLTable
    """
    if not isinstance(infer_column_types, (bool, dict)):
        raise UserErrorException('`infer_column_types` must be a bool or a dictionary.')

    if isinstance(infer_column_types, dict):
        if not infer_column_types:
            infer_column_types = True
        elif len(set(infer_column_types) - set(['sample_size', 'column_type_overrides'])) > 0:
            raise UserErrorException('If `infer_column_types` is a dictionary, may only contain keys '
                                     '`sample_size` and `column_type_overrides`.')
        elif 'sample_size' in infer_column_types \
                and not (isinstance(infer_column_types['sample_size'], int) and infer_column_types['sample_size'] > 0):
            raise UserErrorException('If `infer_column_types` is a dictionary with a `sample_size` key, '
                                     'its value must be a positive integer.')
        elif 'column_type_overrides' in infer_column_types:
            if not isinstance(infer_column_types['column_type_overrides'], dict):
                raise UserErrorException('If `infer_column_types` is a dictionary with a `column_type_overrides` key, '
                                         'its value must be a dictionary of strings to `mltable.DataType`s or strings.')

            infer_column_types['column_type_overrides'] \
                = _process_column_to_type_mappings(infer_column_types['column_type_overrides'], allow_stream_info=False)

    header = MLTableHeaders._parse(header)
    encoding = MLTableFileEncoding._parse(encoding)
    return from_paths(paths)._add_transformation_step(_READ_DELIMITED_KEY,
                                                      {'delimiter': delimiter,
                                                       'header': MLTableHeaders._parse(header).name,
                                                       'support_multi_line': support_multi_line,
                                                       'empty_as_string': empty_as_string,
                                                       'encoding': MLTableFileEncoding._parse(encoding).name,
                                                       'include_path_column': include_path_column,
                                                       'infer_column_types': infer_column_types})


@track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
def from_parquet_files(paths, include_path_column=False):
    """
    Create the MLTable from the given list of parquet files.

    .. remarks::

        There must be a valid paths dictionary

        .. code-block:: python

            # load mltable from local parquet paths
            from mltable import from_parquet_files
            paths = [{'file': './samples/mltable_sample/sample.parquet'}]
            mltable = from_parquet_files(paths)

    :param paths: Paths supports files or folders with local or cloud paths. Relative local file paths are assumed to be
        relative to the current working directory. If the parent directory a local file path is relative to is not the
        current working directory, instead recommend passing that path as a absolute file path.
    :type paths: list[dict[str, str]]
    :param include_path_column: Keep path information as a column, useful when reading multiple files and you want
        to know which file a particular record came from, or to keep useful information that may be stored in a file
        path.
    :type include_path_column: bool
    :return: MLTable instance
    :rtype: mltable.MLTable
    """
    return from_paths(paths)._add_transformation_step('read_parquet', {"include_path_column": include_path_column})


@track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
def from_json_lines_files(paths, invalid_lines="error", encoding="utf8", include_path_column=False):
    """
    Create a MLTable from the given list of JSON file paths.

    .. remarks::

        There must be a valid paths dictionary

        .. code-block:: python

            # load mltable from local JSON paths
            from mltable import from_json_lines_files
            paths = [{'file': './samples/mltable_sample/sample_data.jsonl'}]
            mltable = from_json_lines_files(paths)

    :param paths: Paths supports files or folders with local or cloud paths. Relative local file paths are assumed to be
        relative to the current working directory. If the parent directory a local file path is relative to is not the
        current working directory, instead recommend passing that path as a absolute file path.
    :type paths: list[dict[str, str]]
    :param invalid_lines: How to handle lines that are invalid JSON, can be 'drop' or 'error'. If 'drop' invalid lines
        are dropped, else error is raised.
    :type invalid_lines: str
    :param encoding: Specifies the file encoding using the enum :class:`mltable.MLTableFileEncoding`. Supported file
        encodings:
        - utf8 as "utf8", "utf-8", "utf-8 bom"
        - iso88591 as "iso88591" or "iso-8859-1"
        - latin1 as "latin1" or "latin-1"
        - utf16 as "utf16" or "utf-16"
        - windows1252 as "windows1252" or "windows-1252"
    :type encoding: typing.Union[str, mltable.MLTableFileEncoding]
    :param include_path_column: Keep path information as a column, useful when reading multiple files and you want
        to know which file a particular record came from, or to keep useful information that may be stored in a file
        path.
    :type include_path_column: bool
    :return: MLTable
    :rtype: mltable.MLTable
    """
    if invalid_lines not in ['error', 'drop']:
        raise UserErrorException("Invalid value for invalid_lines, the supported values are ['error', 'drop']")

    return from_paths(paths)._add_transformation_step(_READ_JSON_KEY,
                                                      {"invalid_lines": invalid_lines,
                                                       "encoding": MLTableFileEncoding._parse(encoding).name,
                                                       "include_path_column": include_path_column})


@track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
def from_paths(paths):
    """
    Create the MLTable from the given paths.

    .. remarks::

        There must be a valid paths dictionary

        .. code-block:: python

            # load mltable from local paths
            from mltable import from_paths
            tbl = from_paths([{'file': "./samples/mltable_sample"}])

            # load mltable from cloud paths
            from mltable import load
            tbl = from_paths(
                [{'file': "https://<blob-storage-name>.blob.core.windows.net/<path>/sample_file"}])

    :param paths: Paths supports files or folders with local or cloud paths. Relative local file paths are assumed to be
        relative to the current working directory. If the parent directory a local file path is relative to is not the
        current working directory, instead recommend passing that path as a absolute file path.
    :type paths: list[dict[str, str]]
    :return: MLTable instance
    :rtype: mltable.MLTable
    """
    base_path = os.getcwd()
    mltable_yaml_dict, path_pairs = _make_all_paths_absolute({_PATHS_KEY: paths}, base_path=base_path)
    _validate(mltable_yaml_dict)
    return MLTable._create_from_dict(mltable_yaml_dict=mltable_yaml_dict, path_pairs=path_pairs, load_uri=base_path)


@track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
def from_delta_lake(delta_table_uri, timestamp_as_of=None, version_as_of=None, include_path_column=False):
    """
    Creates an MLTable object to read in Parquet files from delta lake table.

    .. remarks::

        **from_delta_lake** creates an MLTable object which defines the operations to
        load data from delta lake folder into tabular representation.

        For the data to be accessible by Azure Machine Learning, `path` must point to the delta table directory
        and the delta lake files that are referenced must be accessible by AzureML services or behind public web urls.

        **from_delta_lake** supports reading delta lake data from a uri
        pointing to: local path, Blob, ADLS Gen1 and ADLS Gen2

        Users are able to read in and materialize the data by calling `to_pandas_dataframe()` on the returned MLTable

        .. code-block:: python

            # create an MLTable object from a delta lake using timestamp versioning and materialize the data
            from mltable import from_delta_lake
            mltable_ts = from_delta_lake(delta_table_uri="./data/delta-01", timestamp_as_of="2021-05-24T00:00:00Z")
            pd = mltable_ts.to_pandas_dataframe()

            # create  an MLTable object from a delta lake using integer versioning and materialize the data
            from mltable import from_delta_lake
            mltable_version = from_delta_lake(delta_table_uri="./data/delta-02", version_as_of=1)
            pd = mltable_version.to_pandas_dataframe()

    :param delta_table_uri: URI pointing to the delta table directory containing the delta lake parquet files to read.
        Supported URI types are: local path URI, storage URI, long-form datastore URI, or data asset uri.
    :type delta_table_uri: str
    :param timestamp_as_of: datetime string in RFC-3339/ISO-8601 format to use to read in matching parquet files
        from a specific point in time.
        ex) "2022-10-01T00:00:00Z", "2022-10-01T00:00:00+08:00", "2022-10-01T01:30:00-08:00"
    :type timestamp_as_of: string
    :param version_as_of: integer version to use to read in a specific version of parquet files.
    :type version_as_of: int
    :param include_path_column: Keep path information as a column, useful when reading multiple files and you want
        to know which file a particular record came from, or to keep useful information that may be stored in a file
        path.
    :type include_path_column: bool
    :return: MLTable instance
    :rtype: mltable.MLTable
    """
    if timestamp_as_of and version_as_of:
        raise UserErrorException("Both timestamp_as_of and version_as_of parameters were provided, but only one of "
                                 "version_as_of or timestamp_as_of can be specified.")

    if timestamp_as_of:
        rfc3339_checker = re.compile(r'^((?:(\d{4}-(0[1-9]|1[0-2])-([0-3]\d))'
                                     r'T(\d{2}:\d{2}:\d{2}(?:\.\d+)?))(Z|[\+-]\d{2}:\d{2})?)$')
        if rfc3339_checker.match(timestamp_as_of) is None:
            raise UserErrorException(f'Provided timestamp_as_of: {timestamp_as_of} is not in RFC-3339/ISO-8601 format. '
                                     'Please make sure that it adheres to RFC-3339/ISO-8601 format. For example: '
                                     '"2022-10-01T00:00:00Z", "2022-10-01T22:10:57+02:00", '
                                     '"2022-10-01T16:32:11.8+00:00" are correctly formatted.')

    mltable = from_paths([{"folder": delta_table_uri}])
    return mltable._add_transformation_step('read_delta_lake',
                                            {'version_as_of': version_as_of,
                                             'timestamp_as_of': timestamp_as_of,
                                             'include_path_column': include_path_column})


class MLTable:
    """
    Represents a MLTable.

    A MLTable defines a series of lazily-evaluated, immutable operations to
    load data from the data source. Data is not loaded from the source until
    MLTable is asked to deliver data.
    """

    def __init__(self):
        """
        Initialize a new MLTable.

        This constructor is not supposed to be invoked directly. MLTable is
        intended to be created using :func:`mltable.load`.
        """
        self._loaded = False

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _to_yaml_dict(self):
        """
        Returns all the information associated with MLTable as a YAML-style dictionary.

        :return: dict representation of this MLTable
        :rtype: dict
        """
        return yaml.safe_load(str(self))

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def __repr__(self):
        """
        Returns all the information associated with MLTable as a YAML-style
        string representation.

        :return: string representation of this MLTable
        :rtype: str
        """
        self._check_loaded()
        # _dataflow.to_yaml_string() serializes Serde units (anonymous value containing no data) as nulls
        # this results in nested fields with empty values being serialized with nulls as value.
        mltable_yaml_str = _wrap_rslex_function_call(lambda: self._dataflow.to_yaml_string())
        mltable_yaml_dict = yaml.safe_load(mltable_yaml_str)
        mltable_yaml_helper = MLTableYamlCleaner(mltable_yaml_dict=mltable_yaml_dict)
        return str(mltable_yaml_helper)

    def __str__(self):
        """
        Returns all the information associated with MLTable as a YAML-style
        string representation.

        :return: string representation of this MLTable
        :rtype: str
        """
        return self.__repr__()

    def __eq__(self, other):
        """
        Returns if given object equals this MLTable.

        :param other: given object to compare
        :type other: Any
        :return: is given object equals this MLTable
        :rtype: bool
        """
        if not isinstance(other, MLTable):
            return False

        self_yaml = self._to_yaml_dict()
        other_yaml = other._to_yaml_dict()

        def have_same_key(key):
            return self_yaml.get(key) == other_yaml.get(key)

        return have_same_key(_TRANSFORMATIONS_SCHEMA_KEY) \
            and have_same_key(_METADATA_SCHEMA_NAME) \
                and have_same_key(_TRAITS_SECTION_KEY) \
                    and self.paths == other.paths  # want to compare using original paths

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def validate(self):
        """
        Validates if this MLTable's data can be loaded, requires the MLTable's
        data source(s) to be accessible from the current compute.

        :return: None
        :rtype: None
        """
        failed_to_load_error_msg = \
            'Can not load data from this MLTable\'s associated datastores. Please check the associated paths.'

        mltable_yaml_str = str(self.take(1))
        try:
            records = _wrap_rslex_function_call(lambda: to_pyrecords_with_preppy('MLTable.validate', mltable_yaml_str))
        except Exception:  # this is broad, but dataprepreader throws different errors
            raise RuntimeError(failed_to_load_error_msg)

        if len(records) < 1:
            raise RuntimeError(failed_to_load_error_msg)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _ensure_random_seed(self, seed):
        """
        If the given seed is not an integer or None, raises a UserErrorException. If
        None selects a random seed randomly between 1 and 1000.

        :param seed: possible value for random seed
        :type seed: object
        :return: valid random seed
        :rtype: int
        """
        if seed is None:
            return random.randint(1, 1000)
        if not isinstance(seed, int):
            raise UserErrorException('A random seed must be an integer')
        return seed

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _check_loaded(self):
        if not self._loaded:
            raise UserErrorException('MLTable does not appear to be loaded correctly. Please use MLTable.load() to '
                                     'load a MLTable YAML file into memory.')

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _add_transformation_step(self, step, args, index=None):
        """
        Adds the given transformation step and its associated arguments to
        this MLTable's PyRsDataflow at the given index in the list of all
        added transformation steps. Returns a new MLTable whose PyRsDataflow
        is the PyRsDataflow resulting from the prior addition.

        :param step: transformation step
        :type step: str
        :param args: arguments for given transformation step
        :type: object
        :param index: optional argument to indicate which index to add the step
        :type: int
        :return: MLTable with resulting PyRsDataflow
        :rtype: mltable.MLTable
        """
        new_dataflow = _wrap_rslex_function_call(lambda: self._dataflow.add_transformation(step, args, index))
        return MLTable._create_from_dataflow(new_dataflow, self._path_pairs, self._load_uri)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _normalize_partition_int_list(self, columns):
        if isinstance(columns, int):
            return [columns]
        elif isinstance(columns, list) and len(columns) > 0 \
                and all(isinstance(index, int) for index in columns):
            return columns
        raise UserErrorException('Columns should be a int or list of int with at least one element')

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _get_columns_in_traits(self):
        """
        Gets all the columns that are set in this MLTable's Traits.

        :return: set of all Traits
        :rtype: set[str]
        """
        columns_in_traits = set()
        if self.traits:
            timestamp_col = self.traits._check_and_get_trait(
                _TIMESTAMP_COLUMN_KEY)
            if timestamp_col is not None:
                columns_in_traits.add(timestamp_col)

            index_cols = self.traits._check_and_get_trait(_INDEX_COLUMNS_KEY)
            if index_cols is not None:
                columns_in_traits.update(index_cols)

        return columns_in_traits

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _download(self, stream_column=None, target_path=None, ignore_not_found=False, storage_options=None):
        if target_path is None:
            target_path = tempfile.mkdtemp()

        if stream_column is None:
            stream_column = 'Path'

        if stream_column != 'Path':
            new_mltable = self._add_transformation_step('rename_columns', {stream_column: 'Path'})
        else:
            new_mltable = MLTable._create_from_dataflow(self._dataflow, None, None)

        function_source_str = '{"r":["Function",[[],{"r":[]},{"r":["Function",[["row"],{"r":[]},' \
                              '{"r":["Invoke",[{"r":["Identifier","GetPortablePath"]},' \
                              '[{"r":["RecordField",[{"r":["Identifier","row"]},"Path"]]},""]]]}]]}]]}'
        new_mltable = new_mltable._add_transformation_step('add_columns',
                                                           {
                                                               'language': 'Native',
                                                               'expressions':
                                                                   [
                                                                       {
                                                                           'new_column': 'Portable Path',
                                                                           'prior_column': 'Path',
                                                                           'function_source': function_source_str
                                                                       }
                                                                   ]
                                                           })

        new_mltable = new_mltable._add_transformation_step('write_streams_to_files',
                                                           {
                                                               'streams_column': 'Path',
                                                               'destination':
                                                                   {
                                                                       'directory': str(target_path),
                                                                       'handler': 'Local'
                                                                   },
                                                               'file_names_column': 'Portable Path'
                                                           })

        # append workspace information for the stream_column for backwards support
        # AmlDatastore://workspaceblobstore/data/images/animals folder/1d.jpg
        workspace_info = _try_resolve_workspace_info(storage_options)
        if _has_sufficient_workspace_info(workspace_info):
            new_mltable = \
                MLTable._append_workspace_to_stream_info_conversion(new_mltable, workspace_info, stream_column)

        download_records = _wrap_rslex_function_call(
            lambda: to_pyrecords_with_preppy('MLTable._download', str(new_mltable)))
        return _validate_downloads(download_records, ignore_not_found, _get_logger())

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _with_partition_size(self, partition_size, partition_size_unit='b'):
        """
        Updates delimited files and JSON lines files to utilize the given parition size.

        :param partition_size: Minimum batch size data be will be partitioned against.
        :type partition_size: int
        :param partition_size_unit: The memory unit give partition_size is in, default to bytes. Supported options are
            a :class:`mltable.MLTablePartitionSizeUnit` or a string as one of 'byte' ('b'), 'kilobyte' ('kb'),
            'megabyte' ('mb'), or 'gigabyte' ('gb').
        :type partition_size_unit:  Union[str, mltable.MLTablePartitionSizeUnit]
        :return: MLTable with updated partition size
        :rtype: mltable.MLTable
        """
        self._check_loaded()
        partition_size = MLTablePartitionSize._parse(partition_size, partition_size_unit)
        if hasattr(self._dataflow, 'set_partition_size'):
            new_py_rs_dataflow = _wrap_rslex_function_call(lambda: self._dataflow.set_partition_size(partition_size))
            return MLTable._create_from_dataflow(new_py_rs_dataflow, self._path_pairs, self._load_uri)
        else:  # TODO (nathof) remove fallback after release
            mltable_yaml_dict = self._to_yaml_dict()
            for key in [_READ_DELIMITED_KEY, _READ_JSON_KEY]:
                if key in mltable_yaml_dict[_TRANSFORMATIONS_SCHEMA_KEY][0]:
                    mltable_yaml_dict[_TRANSFORMATIONS_SCHEMA_KEY][0][key]['partition_size'] = partition_size
                    return MLTable._create_from_dict(mltable_yaml_dict, self._path_pairs, self._load_uri)
            raise UserErrorException(
                'transformation step read_delimited or read_json_lines is required to update partition_size')

    @track(_get_logger, activity_type=_PUBLIC_API, custom_dimensions={'app_name': _APP_NAME})
    def to_pandas_dataframe(self):
        """
        Load all records from the paths specified in the MLTable file into a
        Pandas DataFrame.

        .. remarks::

            The following code snippet shows how to use the
            to_pandas_dataframe api to obtain a pandas dataframe corresponding
            to the provided MLTable.

            .. code-block:: python

                from mltable import load
                tbl = load('.\\samples\\mltable_sample')
                pdf = tbl.to_pandas_dataframe()
                print(pdf.shape)

        :return: Pandas Dataframe containing the records from paths in this
                 MLTable
        :rtype: pandas.DataFrame
        """
        self._check_loaded()
        custom_dimensions = {'app_name': _APP_NAME}
        if self._workspace_context:
            custom_dimensions.update(self._workspace_context)

        mltable_yaml_str = str(self)
        try:
            return _wrap_rslex_function_call(lambda: get_dataframe_reader().to_pandas_dataframe(mltable_yaml_str))
        except Exception as e:
            raise e

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def get_partition_count(self) -> int:
        """
        Calculates the partitions for the current mltable and returns their count.

        :return: The count of partitions.
        """
        from azureml.dataprep.api._dataframereader import get_partition_count_with_rslex
        return _wrap_rslex_function_call(lambda: get_partition_count_with_rslex(str(self)))

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def select_partitions(self, partition_index_list):
        """
        Adds a transformation step to select the partition.

        .. remarks::

            The following code snippet shows how to use the select_partitions api to selected partitions
            from the provided MLTable.

            .. code-block:: python

                partition_index_list = [1, 2]
                mltable = mltable.select_partitions(partition_index_list)

        :param partition_index_list: list of partition index
        :type partition_index_list: list of int
        :return: MLTable with partition size updated
        :rtype: mltable.MLTable
        """
        self._check_loaded()
        partition_index_list = self._normalize_partition_int_list(partition_index_list)
        return self._add_transformation_step('select_partitions', partition_index_list)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def extract_columns_from_partition_format(self, partition_format):
        """
        Adds a transformation step to use the partition information of each path and extract them into columns
        based on the specified partition format.

        Format part '{column_name}' creates string column, and '{column_name:yyyy/MM/dd/HH/mm/ss}' creates
        datetime column, where 'yyyy', 'MM', 'dd', 'HH', 'mm' and 'ss' are used to extract year, month, day,
        hour, minute and second for the datetime type.

        The format should start from the position of first partition key until the end of file path.
        For example, given the path '/Accounts/2019/01/01/data.csv' where the partition is by department name
        and time, partition_format='/{Department}/{PartitionDate:yyyy/MM/dd}/data.csv'
        creates a string column 'Department' with the value 'Accounts' and a datetime column 'PartitionDate'
        with the value '2019-01-01'.

        :param partition_format: Partition format to use to extract data into columns
        :type partition_format: str
        :return: MLTable whose partition format is set to given format
        :rtype: mltable.MLTable
        """
        self._check_loaded()
        return self._add_transformation_step('extract_columns_from_partition_format',
                                             {_PARTITION_FORMAT_KEY: partition_format},
                                             0)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _get_partition_key_values(self, partition_keys=None):
        """Return unique key values of partition_keys.

        validate if partition_keys is a valid subset of full set of partition keys, return unique key values of
        partition_keys, default to return the unique key combinations by taking the full set of partition keys of this
        dataset if partition_keys is None

        .. code-block:: python

            # get all partition key value pairs
            partitions = mltable.get_partition_key_values()
            # Return [{'country': 'US', 'state': 'WA', 'partition_date': datetime('2020-1-1')}]

            partitions = mltable.get_partition_key_values(['country'])
            # Return [{'country': 'US'}]

        :param partition_keys: partition keys
        :type partition_keys: builtin.list[str]
        """
        self._check_loaded()
        if not partition_keys:
            partition_keys = self.partition_keys
        if not self.partition_keys:
            raise UserErrorException("cannot retrieve partition key values for a mltable that has no partition keys")

        invalid_keys = [
            x for x in partition_keys if x not in self.partition_keys]
        if len(invalid_keys) != 0:
            raise UserErrorException(f"{invalid_keys} are invalid partition keys")

        # currently use summarize to find the distinct result
        mltable = self.take(count=1)
        pd = mltable.to_pandas_dataframe()
        no_partition_key_columns = [
            x for x in pd.columns if x not in partition_keys]
        mltable = self
        if len(no_partition_key_columns) > 0:
            mltable = mltable._add_transformation_step('summarize',
                                                       {"aggregates":
                                                            [{"source_column": no_partition_key_columns[0],
                                                              "aggregate": "count",
                                                              "new_column": "new_count"}],
                                                        "group_by": partition_keys})
        mltable = mltable.keep_columns(partition_keys)
        # need to implement distinct from rlex https://msdata.visualstudio.com/Vienna/_workitems/edit/1749317
        # mltable = self.distinct_rows()
        pd = mltable.to_pandas_dataframe()
        pd = pd.drop_duplicates()
        partition_key_values = pd.to_dict(
            orient='records') if pd.shape[0] != 0 else []
        return partition_key_values

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def filter(self, expression):
        """
        Filter the data, leaving only the records that match the specified expression.

        .. remarks::

            Expressions are started by indexing the mltable with the name of a column. They support a variety of
                functions and operators and can be combined using logical operators. The resulting expression will be
                lazily evaluated for each record when a data pull occurs and not where it is defined.

            .. code-block:: python

                filtered_mltable = mltable.filter('feature_1 == \"5\" and target > \"0.5)\"')
                filtered_mltable = mltable.filter('col("FBI Code") == \"11\"')

        :param expression: The expression to evaluate.
        :type expression: string
        :return: MLTable after filter
        :rtype: mltable.MLTable
        """
        self._check_loaded()
        return self._add_transformation_step('filter', expression)

    @property
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def paths(self):
        """
        Returns a list of dictionaries containing the original paths given to this MLTable. Relative local file paths
        are assumed to be relative to the directory where the MLTable YAML file this MLTable instance was loaded from.

        :return: list of dicts containing paths specified in the MLTable
        :rtype: list[dict[str, str]]
        """
        self._check_loaded()
        return list(map(lambda x: x[0], self._path_pairs))

    @property
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def partition_keys(self):
        """Return the partition keys.

        :return: the partition keys
        :rtype: builtin.list[str]
        """
        self._check_loaded()

        def parse_partition_format(partition_format):
            date_parts = ['yyyy', 'MM', 'dd', 'HH', 'mm', 'ss']
            date_part_map = {d: '_sys_{}'.format(d) for d in date_parts}
            defined_date_parts = []
            date_column = None
            columns = []
            i = 0
            pattern = ''
            while i < len(partition_format):
                c = partition_format[i]
                if c == '/':
                    pattern += '\\/'
                elif partition_format[i:i + 2] in ['{{', '}}']:
                    pattern += c
                    i += 1
                elif c == '{':
                    close = i + 1
                    while close < len(partition_format) and partition_format[close] != '}':
                        close += 1
                    key = partition_format[i + 1:close]
                    if ':' in key:
                        date_column, date_format = key.split(':')
                        for date_part in date_parts:
                            date_format = date_format.replace(
                                date_part, '{' + date_part_map[date_part] + '}')
                        partition_format = partition_format[:i] + \
                                           date_format + partition_format[close + 1:]
                        continue
                    else:
                        found_date = False
                        for k, v in date_part_map.items():
                            if partition_format.startswith(v, i + 1):
                                pattern_to_add = '(?<{}>\\d{{{}}})'.format(
                                    v, len(k))
                                if pattern_to_add in pattern:
                                    pattern += '(\\d{{{}}})'.format(len(k))
                                else:
                                    pattern += pattern_to_add
                                    defined_date_parts.append(k)
                                found_date = True
                                break

                        if not found_date:
                            pattern_to_add = '(?<{}>[^\\.\\/\\\\]+)'.format(key)
                            if pattern_to_add in pattern:
                                pattern += '([^\\.\\/\\\\]+)'
                            else:
                                columns.append(key)
                                pattern += pattern_to_add
                        i = close
                elif c == '*':
                    pattern += '(.*?)'
                elif c == '.':
                    pattern += '\\.'
                else:
                    pattern += c
                i += 1
            if date_column is not None:
                columns.append(date_column)

            if defined_date_parts and 'yyyy' not in defined_date_parts:
                raise UserErrorException(f'Invalid partition_format "{partition_format}". '
                                         f'{validation_error["NO_YEAR"]}')
            return pattern, defined_date_parts, columns

        if len(self._partition_keys) > 0:
            return self._partition_keys

        mltable_dict = self._to_yaml_dict()
        if _TRANSFORMATIONS_SCHEMA_KEY in mltable_dict:
            for mltable_transformation in mltable_dict[_TRANSFORMATIONS_SCHEMA_KEY]:
                if _EXTRACT_PARTITION_FORMAT_KEY in mltable_transformation:
                    parsed_result = parse_partition_format(
                        mltable_transformation[_EXTRACT_PARTITION_FORMAT_KEY][_PARTITION_FORMAT_KEY])
                    if len(parsed_result) == 3 and parsed_result[2]:
                        self._partition_keys = parsed_result[2]
                        return parsed_result[2]
        return []

    @property
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _is_tabular(self):
        """
        check if this mltable is tabular using its yaml
        """
        self._check_loaded()
        mltable_yaml = self._to_yaml_dict()
        return _is_tabular(mltable_yaml)

    @staticmethod
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _create_from_dict(mltable_yaml_dict, path_pairs, load_uri):
        """
        Creates a new MLTable from a YAML dictionary containing information from a MLTable file.

        :param mltable_yaml_dict: MLTable dict to read from
        :type mltable_yaml_dict: dict
        :param path_pairs: pairings from original given data file paths to transformed data paths, usually relative
            file paths made absolute
        :type path_pairs: list[tuple[dict[str, str], dict[str, str]]]
        :param load_uri: directory path where MLTable was originally loaded from, or intended to be but doesn't
            actually exist yet if created with `MLTable.from_*`
        :type load_uri: str
        :return: MLTable from given dict
        :rtype: mltable.MLTable
        """
        mltable_yaml_string = yaml.safe_dump(mltable_yaml_dict)
        dataflow = _wrap_rslex_function_call(lambda: PyRsDataflow(mltable_yaml_string))
        return MLTable._create_from_dataflow(dataflow, path_pairs, load_uri)

    @staticmethod
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _create_from_dataflow(dataflow, path_pairs, load_uri):
        """
        Creates a new MLTable from a PyRsDataflow.

        :param new_dataflow: PyRsDataflow to read from
        :type new_dataflow: PyRsDataflow
        :param path_pairs: pairings from original given data file paths to transformed data paths, usually relative
            file paths made absolute
        :type path_pairs: list[tuple[dict[str, str], dict[str, str]]]
        :param load_uri: directory path where MLTable was originally loaded from, or if created with `MLTable.from_*`,
            where directory is intended to be
        :type load_uri: str
        :return: MLTable from given PyRsDataflow
        :rtype: mltable.MLTable
        """
        new_mltable = MLTable()
        new_mltable._dataflow = dataflow
        new_mltable._loaded = True
        new_mltable._path_pairs = path_pairs
        new_mltable._partition_keys = []
        new_mltable.traits = Traits._create(new_mltable)
        new_mltable.metadata = Metadata._create(new_mltable)
        new_mltable._workspace_context = None
        new_mltable._load_uri = load_uri
        return new_mltable

    @staticmethod
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _append_workspace_to_stream_info_conversion(mltable, workspace_info, stream_column):
        def _is_stream_column_in_column_conversion(columns_item):
            return 'stream_info' == columns_item['column_type'] \
                and ((isinstance(columns_item['columns'], str) and columns_item['columns'] == stream_column)
                     or (isinstance(columns_item['columns'], list) and stream_column in columns_item['columns']))

        mltable_dict = mltable._to_yaml_dict()
        if _TRANSFORMATIONS_SCHEMA_KEY in mltable_dict:
            columns_conversion_list = [columns_item for t in mltable_dict[_TRANSFORMATIONS_SCHEMA_KEY]
                                       for k, v in t.items()
                                       if k == 'convert_column_types'
                                       for columns_item in v
                                       if _is_stream_column_in_column_conversion(columns_item)]

            if len(columns_conversion_list) == 0:
                return mltable

            for columns in columns_conversion_list:
                columns['column_type'] = {
                    'stream_info': {
                        'subscription': workspace_info[STORAGE_OPTION_KEY_AZUREML_SUBSCRIPTION],
                        'resource_group': workspace_info[STORAGE_OPTION_KEY_AZUREML_RESOURCEGROUP],
                        'workspace_name': workspace_info[STORAGE_OPTION_KEY_AZUREML_WORKSPACE],
                        'escaped': False
                    }
                }

            return MLTable._create_from_dict(mltable_dict, mltable._path_pairs, mltable._load_uri)

        # else skip update
        return mltable

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def take(self, count=20):
        """
        Adds a transformation step to select the first `count` rows of this
        MLTable.

        :param count: number of rows from top of table to select
        :type count: int
        :return: MLTable with added "take" transformation step
        :rtype: mltable.MLTable
        """
        self._check_loaded()
        if not (isinstance(count, int) and count > 0):
            raise UserErrorException('Number of rows must be a positive integer')
        return self._add_transformation_step('take', count)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def show(self, count=20):
        """
        Retrieves the first `count` rows of this MLTable as a Pandas Dataframe.

        :param count: number of rows from top of table to select
        :type count: int
        :return: first `count` rows of the MLTable
        :rtype: Pandas Dataframe
        """
        return self.take(count).to_pandas_dataframe()

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def take_random_sample(self, probability, seed=None):
        """
        Adds a transformation step to randomly select each row of this MLTable
        with `probability` chance. Probability must be in range [0, 1]. May
        optionally set a random seed.

        :param probability: chance that each row is selected
        :type: probability: float
        :param seed: optional random seed
        :type seed: Optional[int]
        :return: MLTable with added transformation step
        :rtype: mltable.MLTable
        """
        self._check_loaded()
        if not (isinstance(probability, float) and 0 < probability < 1):
            raise UserErrorException('Probability should an float greater than 0 and less than 1')
        seed = self._ensure_random_seed(seed)
        return self._add_transformation_step('take_random_sample',
                                             {"probability": probability,
                                              "seed": seed})

    def _is_valid_col_selector(self, columns):
        if not (isinstance(columns, str) or \
                (isinstance(columns, (list, tuple)) and len(columns) > 0 and all(isinstance(x, str) for x in columns))):
            raise UserErrorException(
                'Expect `columns` to be a single string, a non-empty list of strings, or a non-empty tuple of strings')

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def drop_columns(self, columns: Union[str, List[str]]):
        """
        Adds a transformation step to drop desired columns from the dataset.

        If a timeseries column is dropped, the corresponding capabilities will
        be dropped for the returned MLTable.

        :param columns: The name or a list of names for the columns to drop
        :type columns: Union[str, builtin.list[str]]
        :return: MLTable with added transformation step
        :rtype: mltable.MLTable
        """
        self._check_loaded()
        self._is_valid_col_selector(columns)

        # columns can't contain traits
        columns_in_traits = self._get_columns_in_traits()
        if (isinstance(columns, str) and columns in columns_in_traits) or columns_in_traits.intersection(columns):
            raise UserErrorException('Columns in traits must be kept and cannot be dropped')

        return self._add_transformation_step('drop_columns', columns)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def keep_columns(self, columns: Union[str, List[str]]):
        """
        Adds a transformation step to keep the specified columns and drop all
        others from the dataset.

        If a timeseries column is dropped, the corresponding capabilities will
        be dropped for the returned MLTable.

        :param columns: The name or a list of names for the columns to keep
        :type columns: Union[str, builtin.list[str]]
        :return: MLTable with added transformation step
        :rtype: mltable.MLTable
        """
        self._check_loaded()
        self._is_valid_col_selector(columns)

        # traits must be in columns
        columns_in_traits = self._get_columns_in_traits()
        if (isinstance(columns, str) and len(columns_in_traits) != 0 and {columns, } != columns_in_traits) or any(
                x not in columns for x in columns_in_traits):
            raise UserErrorException('Columns in traits must be kept and cannot be dropped')

        return self._add_transformation_step('keep_columns', columns)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def random_split(self, percent=.5, seed=None):
        """
        Randomly splits this MLTable into two MLTables, one having
        approximately "percent"% of the original MLTable's data and the other
        having the remainder (1-"percent"%).

        :param percent: percent of the MLTable to split between
        :type percent: Union[int, float]
        :param seed: optional random seed
        :type seed: Optional[int]
        :return: two MLTables with this MLTable's data split between them by
                 "percent"
        :rtype: Tuple[mltable.MLTable, mltable.MLTable]
        """
        if not (isinstance(percent, float) and 0 < percent < 1):
            raise UserErrorException('Percent should be a float greater than 0 and less than 1')
        seed = self._ensure_random_seed(seed)
        split_a = self._add_transformation_step('sample', {"sampler": "random_percent",
                                                           "sampler_arguments": {
                                                               "probability": percent,
                                                               "probability_lower_bound": 0.0,
                                                               "seed": seed}})
        split_b = self._add_transformation_step('sample', {"sampler": "random_percent",
                                                           "sampler_arguments": {
                                                               "probability": 1.0,
                                                               "probability_lower_bound": percent,
                                                               "seed": seed}})
        return split_a, split_b

    def _parse_uri_dirc(self, uri):
        """
        Attempts to parse out the directory component of a given URI. Current supported URIs are local filesystems,
        AML datastores, Azure Data Lake Gen 1, Azure Data Lake Gen 2, and Azure Blob Storage.

        :param uri: URI to parse
        :type uri: str
        :return: directory component of `uri`
        :rtype: str
        """
        global _AML_DATASTORE_URI_PATTERN, _AZURE_BLOB_STORAGE_URI_PATTERN, _AZURE_DATA_LAKE_GEN_1_URI_PATTERN, \
            _AZURE_DATA_LAKE_GEN_2_URI_PATTERN, _HTTPS_URI_PATTERN

        # local path
        if _is_local_path(uri):
            return os.path.normpath(uri)

        _AML_DATASTORE_URI_PATTERN = _AML_DATASTORE_URI_PATTERN or re.compile(r'^azureml:\/\/.*datastores\/(.*)\/paths\/(.*)$')
        matches = _AML_DATASTORE_URI_PATTERN.match(uri)
        if matches:
            # join datastore with relative path properly
            return pathlib.Path(matches.group(1), matches.group(2)).as_posix()

        _AZURE_BLOB_STORAGE_URI_PATTERN = _AZURE_BLOB_STORAGE_URI_PATTERN or re.compile(r'^wasbs:\/\/.*@.*.blob.core.windows.net\/(.*)$')
        matches = _AZURE_BLOB_STORAGE_URI_PATTERN.match(uri)
        if matches:
            return matches.group(1)

        _AZURE_DATA_LAKE_GEN_2_URI_PATTERN = _AZURE_DATA_LAKE_GEN_2_URI_PATTERN or re.compile(r'^abfss:\/\/.*@.*.dfs.core.windows.net\/(.*)$')
        matches = _AZURE_DATA_LAKE_GEN_2_URI_PATTERN.match(uri)
        if matches:
            return matches.group(1)


        _AZURE_DATA_LAKE_GEN_1_URI_PATTERN = _AZURE_DATA_LAKE_GEN_1_URI_PATTERN or re.compile(r'^adl:\/\/.*.azuredatalakestore.net\/(.*)$')
        matches = _AZURE_DATA_LAKE_GEN_1_URI_PATTERN.match(uri)
        if matches:
            return matches.group(1)

        _HTTPS_URI_PATTERN = _HTTPS_URI_PATTERN or re.compile(r'^https:\/\/.*\..*\/(.*)$')
        matches = _HTTPS_URI_PATTERN.match(uri)
        if matches:
            return matches.group(1)

        raise UserErrorException(f'MLTable was loaded from {uri} which is not supported for saving')

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def save(self, path=None, overwrite=True, colocated=False, show_progress=False):
        """
        Save this MLTable as a MLTable YAML file & its assoicated paths to the given directory path.

        If `path` is not given, defaults to the current working directory. If `path` does not exist, it is created.
        If `path` is remote, the underlying data store must already exist. If `path` is a local directory & is not
        absolute, it is made absolute.

        If `path` points to a file, a UserErrorException is raised. If `path` is a directory path that already contain
        one or more files being saved (including the MLTable YAML file) and `overwrite` is set to False - a
        UserErrorException is raised. If `path` is remote, any local files paths not given as a colocated path
        (file path relative to the directory that MLTable was loaded from) will raise a UserErrorException.

        `colocated` controls how associated paths are saved to `path`. If True, files are copied to `path` alongside
        the MLTable YAML file as relative file paths. Otherwise associated files are not copied, remote paths remain as
        given and local file paths are made relative with path redirection if needed. Note that False may result in
        noncolocated MLTable YAML files which is not recommended, furthermore if `path` is remote this will result in
        a UserErrorException as relative path redirection is not supported for remote URIs.

        Note that if the MLTable is created programatically with methods like `from_paths()` or
        `from_read_delimited_files()` with local relative paths, the MLTable directory path is assumed to be the
        current working directory.

        :param path: directory path to save to, default to current working directory
        :type path: str
        :param colocated: If True, saves copies of local & remote file paths in this MLTable under `path` as
            relative paths. Otherwise no file copying occurs and remote file paths are saved as given to the saved
            MLTable YAML file and local file paths as relative file paths with path redirection. If `path` is remote
            & this MLTable contains local file paths, a UserErrorException will be raised.
        :type colocated: bool
        :param overwrite: overwrites any existing MLTable YAML file and associated files that may already exist in
            `path`
        :type overwrite: bool
        :param show_progress: displays copying progress to stdout
        :type show_progress: bool
        :return: this MLTable instance
        :rtype: mltable.MLTable
        """
        self._check_loaded()
        save_path_dirc = path or os.getcwd()
        is_save_path_dirc_local = _is_local_path(save_path_dirc)

        if is_save_path_dirc_local:
            save_path_dirc = _prepend_file_handler(os.path.normpath(os.path.abspath(save_path_dirc)))

        from azureml.dataprep.rslex import Copier, PyLocationInfo, PyIfDestinationExists
        _wrap_rslex_function_call(ensure_rslex_environment)  # TODO (nathof) append as follow up task

        mltable_yaml_dict = self._to_yaml_dict()
        overwrite \
            = PyIfDestinationExists.MERGE_WITH_OVERWRITE if overwrite else PyIfDestinationExists.FAIL_ON_FILE_CONFLICT

        def save(from_path, to_path, base):
            def execute_save():
                dest_info = PyLocationInfo.from_uri(to_path)
                source_info = PyLocationInfo.from_uri(from_path)
                copier = Copier(dest_info, base, overwrite)
                # TODO (nathof) follow up task to allow continuation on errors
                # TODO (nathof) follow up task to remove files if True & error occurs
                # source_info, traceparent, show_progress, break_on_first_err
                copier.copy_volume(source_info, 'MLTable.save', show_progress, True)

            _wrap_rslex_function_call(execute_save)

        def make_non_colocated_local_path_relative(file_path):
            abs_dirc_path = _remove_file_handler(save_path_dirc)
            file_path = _remove_file_handler(file_path)

            # finds the shortest path from this file path to the save directory, if they are on different
            # mounts / drives leaves path as is
            # ex: file_path = D:\home\user\tmp\file.csv, abs_dirc_path = C:\system\tmp --> file_path stays the same
            if os.path.splitdrive(file_path)[0] != os.path.splitdrive(abs_dirc_path)[0]:
                return file_path

            rel_path = os.path.normpath(os.path.relpath(file_path, abs_dirc_path))

            # `file_path` is absolute so if `rel_path` has parent directory shifts ('../') just keep `file_path`,
            # should only trigger on systems that Posix paths
            # ex: rel_path could end up as ../../home/user/files/data.csv when /home/user/files/data.csv will suffice
            return file_path if rel_path.endswith(file_path) else rel_path

        if self._path_pairs:
            load_uri_is_remote = _is_remote_path(self._load_uri)
            load_uri = self._parse_uri_dirc(self._load_uri)

            def save_path_pair(og_path_dict, processed_path_dict):
                path_type, og_path = list(og_path_dict.items())[0]
                # processing only occurs on relative local paths
                _, processed_path = list(processed_path_dict.items())[0]  # file location to save from

                if not colocated:
                    if _is_local_path(processed_path):
                        if not is_save_path_dirc_local:
                            raise UserErrorException(
                                'Local paths can not be uploaded to remote storage if `colocated` is False. This may '
                                'result in non-colocated file paths which are not supported with remote URIs.')
                        return {path_type: make_non_colocated_local_path_relative(processed_path)}

                    # if was given as remote path
                    if _is_remote_path(og_path):
                        return og_path_dict

                    # if a relative path but loaded from remote URI
                    if load_uri_is_remote:
                        return processed_path_dict

                # for remote paths that don't exist under load_uri
                # TODO (nathof) follow up for how this works with local absolute paths in other mounts
                if _is_remote_path(processed_path) and not processed_path.startswith(load_uri):
                    base_dirc = self._parse_uri_dirc(processed_path)

                # edge case of local, non-colocated path
                if _is_local_path(og_path) and (os.path.isabs(og_path) or '..' in og_path):
                    # make base_dirc point to directory file is loaded from vs MLTable was loaded from
                    # add one more directory as next level are both children of common_path
                    headless_processed_path = _remove_file_handler(processed_path)
                    common_path = os.path.commonpath([load_uri, headless_processed_path])
                    rel_path = os.path.relpath(headless_processed_path, common_path)
                    child_dirc, remainder = rel_path.split(os.path.sep, maxsplit=1)
                    base_dirc = os.path.join(common_path, child_dirc)
                    save_path_dict = {path_type: remainder}
                else:
                    base_dirc = load_uri
                    save_path_dict = og_path_dict

                save(processed_path, save_path_dirc, base_dirc)

                return save_path_dict

            mltable_yaml_dict[_PATHS_KEY] = [save_path_pair(og_path_dict, processed_path_dict)
                                             for og_path_dict, processed_path_dict in self._path_pairs]

        with tempfile.TemporaryDirectory() as temp_dirc:
            mltable_path = os.path.join(temp_dirc, 'MLTable')
            with open(mltable_path, 'w') as f:
                yaml.safe_dump(mltable_yaml_dict, f)
            save(_prepend_file_handler(mltable_path), save_path_dirc, temp_dirc)

        return self

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def skip(self, count):
        """
        Adds a transformation step to skip the first `count` rows of this
        MLTable.

        :param count: number of rows to skip
        :type count: int
        :return: MLTable with added transformation step
        :type: mltable.MLTable
        """
        self._check_loaded()
        if not isinstance(count, int) or count < 1:
            raise UserErrorException('Count must be an integer > 0.')
        return self._add_transformation_step('skip', count)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def convert_column_types(self, column_types):
        """
        Adds a transformation step to convert the specified columns into their respective specified new types.

        :param column_types: Dictionary of column: types the user desires to convert
        :type column_types: dict[typing.Union[typing.Tuple[str], str], mltable.DataType]
        :return: MLTable with added transformation step
        :rtype: mltable.MLTable

        .. code-block:: python

            from mltable import DataType
                data_types = {
                    'ID': DataType.to_string(),
                    'Date': DataType.to_datetime('%d/%m/%Y %I:%M:%S %p'),
                    'Count': DataType.to_int(),
                    'Latitude': DataType.to_float(),
                    'Found': DataType.to_bool(),
                    'Stream': DataType.to_stream()
                }
        """
        self._check_loaded()
        column_types = _process_column_to_type_mappings(column_types)
        return self._add_transformation_step('convert_column_types', column_types)

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _mount(self, stream_column="Path", mount_point=None, **kwargs):
        """Create a context manager for mounting file streams defined by the mltable as local files.

        .. remarks::

            A context manager will be returned to manage the lifecycle of the mount. To mount, you will need to
            enter the context manager and to unmount, exit from the context manager.

            Mount is only supported on Unix or Unix-like operating systems with the native package libfuse installed.
            If you are running inside a docker container, the docker container must be started with the `--privileged`
            flag or started with `--cap-add SYS_ADMIN --device /dev/fuse`.

           .. code-block:: python

                exp_path_1 = os.path.normpath(os.path.join(cwd, '../dataset/data/crime-spring.csv'))
                paths = [{'file': exp_path_1}]
                mltable = from_paths(paths)

                with mltable._mount() as mount_context:
                    # list top level mounted files and folders in the mltable
                    os.listdir(mount_context.mount_point)

                # You can also use the start and stop methods
                mount_context = mltable._mount()
                mount_context.start()  # this will mount the file streams
                mount_context.stop()  # this will unmount the file streams

           If target_path starts with a /, then it will be treated as an absolute path. If it doesn't start
           with a /, then it will be treated as a relative path relative to the current working directory.

        :param stream_column: The stream column to mount.
        :type stream_column: str
        :param mount_point: The local directory to mount the files to. If None, the data will be mounted into a
            temporary directory, which you can find by calling the `MountContext.mount_point` instance method.
        :type mount_point: str
        :return: Returns a context manager for managing the lifecycle of the mount.
        :rtype: MountContext: the context manager. Upon entering the context manager, the dataflow will be
            mounted to the mount_point. Upon exit, it will remove the mount point and clean up the daemon process
            used to mount the dataflow.
        """

        def _ensure_path(path):
            if not path or path.isspace():
                return (tempfile.mkdtemp(), True)

            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                    return (os.path.abspath(path), True)
                except FileExistsError:
                    # There is a chance that the directory may be created after we check for existence and
                    # before we create it. In this case, we can no-op as though the directory already existed.
                    pass

            is_empty = not any(files or dirnames for _,
            dirnames, files in os.walk(path))
            return (os.path.abspath(path), is_empty)

        mltable_yaml_str = str(self)
        hash_object = hashlib.md5(str(self).encode()).hexdigest()
        dataflow_in_memory_uri = f'inmemory://dataflow/{hash_object}'

        _wrap_rslex_function_call(ensure_rslex_environment)
        from azureml.dataprep.rslex import add_in_memory_stream
        _wrap_rslex_function_call(lambda: add_in_memory_stream(dataflow_in_memory_uri, mltable_yaml_str))

        dataflow_in_memory_uri_encoded = urllib.parse.quote(dataflow_in_memory_uri.encode('utf8'), safe='')

        stream_column_encode = urllib.parse.quote(stream_column.encode('utf8'), safe='')
        dataflow_uri = f"rsdf://dataflowfs/{dataflow_in_memory_uri_encoded}/{stream_column_encode}/"

        mount_point, is_empty = _ensure_path(mount_point)
        if os.path.ismount(mount_point):
            raise UserErrorException(
                f'"{mount_point}" is already mounted. Run `sudo umount "{mount_point}"` to unmount it.')

        if not is_empty:
            raise UserErrorException(
                'mltable mount point must be empty, mounting to non-empty folder is not supported.')

        from azureml.dataprep.fuse.dprepfuse import rslex_uri_volume_mount, MountOptions
        mount_options = kwargs.get('mount_options', None)
        # this can be remove after default permission set for MountOption is ready
        if not mount_options:
            mount_options = MountOptions(data_dir_suffix=None)

        return _wrap_rslex_function_call(
            lambda: rslex_uri_volume_mount(uri=dataflow_uri, mount_point=mount_point, options=mount_options))

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _execute(self) -> None:
        """
        Runs the current mltable using the local execution runtime.
        """
        force_clex = False
        allow_fallback_to_clex = True
        if '_TEST_USE_CLEX' in os.environ and os.environ['_TEST_USE_CLEX'] == 'True':
            force_clex = True
        elif '_TEST_USE_CLEX' in os.environ and os.environ['_TEST_USE_CLEX'] == 'False':
            allow_fallback_to_clex = False

        _wrap_rslex_function_call(
            lambda: _execute('mltable._execute',
                             dataflow=str(self),
                             force_clex=force_clex,
                             allow_fallback_to_clex=allow_fallback_to_clex))


class Metadata:
    """
    Class that maps to the metadata section of the MLTable.

    Supports the getting & adding of arbritrary metadata properties.
    """

    @staticmethod
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _create(mltable):
        metadata = Metadata()
        metadata._mltable = mltable
        return metadata

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _key_name_type_check(self, name):
        if not isinstance(name, str):
            raise UserErrorException(f'Metadata only supports string property names, but encountered {type(name)}.')

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def has(self, key):
        """
        Returns if this MLTable's metadata has a property named `key`.

        :param key: property name to check for
        :type key: str
        :return: if metadata contains a property named `key`
        :rtype: bool
        """
        self._key_name_type_check(key)
        return _wrap_rslex_function_call(
            lambda: self._mltable._dataflow.has_schema_property(_METADATA_SCHEMA_NAME, key))

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def get(self, key):
        """
        Returns the value associated with the property `key` in this
        MLTable's metadata. If no such property exists, returns None.

        :param key: property name to retrieve value of
        :type key: str
        :return: value associated with `key`, or None if nonexistant
        :rtype: Optional[object]
        """
        return _wrap_rslex_function_call(
            lambda: self._mltable._dataflow.get_schema_property(_METADATA_SCHEMA_NAME, key)) \
            if self.has(key) else None

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def add(self, key, value):
        """
        Sets the value of the property named `key` in this MLTable's metadata
        to `value`. If the value of `key` was previously set, the value is
        overriden.

        :param key: property name to check
        :type key: str
        :param value: value to set
        :type value: object
        :return: None
        :rtype: None
        """
        self._key_name_type_check(key)
        self._mltable._dataflow = _wrap_rslex_function_call(
            lambda: self._mltable._dataflow.set_schema_property(_METADATA_SCHEMA_NAME, key, value))


class Traits:
    """
    Class that maps to the traits section of the MLTable.

    Currently supported traits: timestamp_column and index_columns
    """

    @staticmethod
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _create(mltable):
        traits = Traits()
        traits._mltable = mltable
        return traits

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _has_trait(self, trait_name):
        return _wrap_rslex_function_call(
            lambda: self._mltable._dataflow.has_schema_property(_TRAITS_SCHEMA_NAME, trait_name))

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _get_trait(self, trait_name):
        return _wrap_rslex_function_call(
            lambda: self._mltable._dataflow.get_schema_property(_TRAITS_SCHEMA_NAME, trait_name))

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _check_and_get_trait(self, trait_name):
        return self._get_trait(trait_name) if self._has_trait(trait_name) else None

    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def _set_trait(self, trait_name, trait_value):
        self._mltable._dataflow = _wrap_rslex_function_call(
            lambda: self._mltable._dataflow.set_schema_property(_TRAITS_SCHEMA_NAME, trait_name, trait_value))

    @property
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def timestamp_column(self):
        """
        If set returns timestamp column name, else rasies a UserErrorException.

        :return: timestamp column name
        :rtype: str
        """
        col = self._check_and_get_trait(_TIMESTAMP_COLUMN_KEY)
        if col is None:
            raise UserErrorException('Timestamp column does not appear to be set. Please make sure you have set it.')
        return col

    @timestamp_column.setter
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def timestamp_column(self, column_name):
        """
        Setter for timestamp_column trait.

        :param column_name: Name of the timestamp column.
        :type column_name: str
        :return: MLTable with timestamp column set to given column
        :rtype: mltable.MLTable
        """
        if not isinstance(column_name, str):
            raise UserErrorException(f'An object of type string is expected, but encountered type: {type(column_name)}')
        self._set_trait(_TIMESTAMP_COLUMN_KEY, column_name)

    @property
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def index_columns(self):
        """
        If set returns a list of index columns' names, else raises a UserErrorException.

        :return: list of index column names
        :rtype: list[str]
        """
        col = self._check_and_get_trait(_INDEX_COLUMNS_KEY)
        if col is None:
            raise UserErrorException('Index columns do not appear to be set. Please make sure you have set them.')
        return col

    @index_columns.setter
    @track(_get_logger, custom_dimensions={'app_name': _APP_NAME})
    def index_columns(self, index_columns_list):
        """
        Setter for index_columns trait.

        :param index_columns_list: List containing names of index columns.
        :type index_columns_list: list[str]
        :return: MLTable with timestamp column set to given column
        :rtype: mltable.MLTable
        """
        if index_columns_list and not isinstance(index_columns_list, list):
            raise UserErrorException('An object of type list is expected, but encountered type: '
                                     f'{type(index_columns_list)}')
        self._set_trait(_INDEX_COLUMNS_KEY, index_columns_list)
