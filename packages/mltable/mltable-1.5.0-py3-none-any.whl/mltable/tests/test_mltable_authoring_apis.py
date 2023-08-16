import os
import tempfile
import shutil

import pytest
import yaml
from azureml.dataprep.native import StreamInfo
from azureml.dataprep import UserErrorException

from mltable.mltable import load, from_paths, from_delimited_files, from_parquet_files, from_json_lines_files,\
    DataType
from .helper_functions import get_mltable_and_dicts, mltable_as_dict, mltable_was_loaded, list_of_dicts_equal


@pytest.mark.mltable_sdk_unit_test
class TestMLTableAuthoringApis:
    def test_convert_column_types_with_simple_types_sdk(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'mltable_with_type')
        mltable = load(path)
        old_df = mltable.to_pandas_dataframe()
        old_column_types = old_df.dtypes

        # checking types without transformations
        assert old_column_types['Fare'].name == 'object'
        assert old_column_types['PassengerId'].name == 'object'
        assert old_column_types['Pclass'].name == 'object'
        assert old_column_types['Ticket'].name == 'object'
        assert old_column_types['Survived'].name == 'object'

        new_mltable = mltable.convert_column_types(column_types={'PassengerId': DataType.to_int(),
                                                                 'Fare': DataType.to_float(),
                                                                 'Pclass': 'int',
                                                                 'Ticket': 'string',
                                                                 'Survived': 'boolean'})

        new_column_types = new_mltable.to_pandas_dataframe().dtypes
        assert new_column_types['PassengerId'].name == 'int64'
        assert new_column_types['Fare'].name == 'float64'
        assert new_column_types['Pclass'].name == 'int64'
        assert new_column_types['Ticket'].name == 'object'
        assert new_column_types['Survived'].name == 'bool'

        # Testing with string type.
        # All values are string by default in pandas, so we need to do some extra logic to check
        pre_mltable = mltable.convert_column_types({'Sex': DataType.to_int()})
        pre_column_types = pre_mltable.to_pandas_dataframe().dtypes
        assert pre_column_types['Sex'].name == 'int64'

        post_mltable = mltable.convert_column_types(
            {'Sex': DataType.to_string()})
        post_column_types = post_mltable.to_pandas_dataframe().dtypes
        # string is object type
        assert post_column_types['Sex'].name == 'object'

    def test_convert_column_types_with_datetime_sdk(self, get_data_folder_path):
        # data types are not automatically inferred for sake of this test
        path = os.path.join(get_data_folder_path, 'traits_timeseries')
        mltable = load(path)
        old_column_types = mltable.to_pandas_dataframe().dtypes
        assert old_column_types['datetime'].name == 'object'
        assert old_column_types['date'].name == 'object'
        assert old_column_types['only_timevalues'].name == 'object'
        data_types = {
            'datetime': DataType.to_datetime('%Y-%m-%d %H:%M:%S'),
            'date': DataType.to_datetime('%Y-%m-%d'),
            'only_timevalues': DataType.to_datetime('%Y-%m-%d %H:%M:%S', '2020-01-01 ')
        }
        new_mltable = mltable.convert_column_types(data_types)
        new_column_types = new_mltable.to_pandas_dataframe().dtypes
        assert new_column_types['datetime'].name == 'datetime64[ns]'
        assert new_column_types['date'].name == 'datetime64[ns]'
        assert new_column_types['only_timevalues'].name == 'datetime64[ns]'

    def test_convert_column_types_with_multiple_columns(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'traits_timeseries')
        mltable = load(path)
        old_column_types = mltable.to_pandas_dataframe().dtypes
        assert old_column_types['datetime'].name == 'object'
        assert old_column_types['date'].name == 'object'
        assert old_column_types['latitude'].name == 'object'
        assert old_column_types['windSpeed'].name == 'object'
        assert old_column_types['precipTime'].name == 'object'
        assert old_column_types['wban'].name == 'object'
        assert old_column_types['usaf'].name == 'object'
        data_types = {
            ('datetime', 'date'): DataType.to_datetime(['%Y-%m-%d %H:%M:%S', '%Y-%m-%d']),
            ('latitude', 'windSpeed'): DataType.to_float(),
            ('wban', 'usaf'): DataType.to_int(),
            'precipTime': DataType.to_float()
        }
        new_mltable = mltable.convert_column_types(data_types)
        new_column_types = new_mltable.to_pandas_dataframe().dtypes
        assert new_column_types['datetime'].name == 'datetime64[ns]'
        assert new_column_types['date'].name == 'datetime64[ns]'
        assert new_column_types['latitude'].name == 'float64'
        assert new_column_types['windSpeed'].name == 'float64'
        assert new_column_types['precipTime'].name == 'float64'
        assert new_column_types['wban'].name == 'int64'
        assert new_column_types['usaf'].name == 'int64'

    def test_convert_column_types_with_boolean_sdk(self, get_data_folder_path):
        # data types are not automatically inferred for sake of this test
        path = os.path.join(get_data_folder_path, 'mltable_with_type')
        mltable = load(path)
        old_column_types = mltable.to_pandas_dataframe().dtypes
        assert old_column_types['Sex'].name == 'object'

        # Using incorrect mismatch_as string
        with pytest.raises(UserErrorException, match='.*`mismatch_as` can only be.*'):
            mltable.convert_column_types({'Sex': DataType.to_bool(false_values=['0'], mismatch_as='dummyVar')})

        # false_values & true_values must either both be None, empty lists, or non-empty lists
        with pytest.raises(UserErrorException,
                           match="`true_values` and `false_values` must both be None or non-empty list of strings"):
            mltable.convert_column_types({'Sex': DataType.to_bool(true_values=['1'])})

        with pytest.raises(UserErrorException,
                           match="`true_values` and `false_values` must both be None or non-empty list of strings"):
            mltable.convert_column_types({'Sex': DataType.to_bool(false_values=['0'])})

        mltable_without_inputs = mltable.convert_column_types({'Sex': DataType.to_bool()})
        mltable_with_full_inputs = mltable.convert_column_types(
            {'Sex': DataType.to_bool(true_values=['1'], false_values=['0'], mismatch_as='error')})

        mltable_without_inputs_types = mltable_without_inputs.to_pandas_dataframe().dtypes
        mltable_with_full_inputs_types = mltable_with_full_inputs.to_pandas_dataframe().dtypes

        assert mltable_without_inputs_types['Sex'].name == 'bool'
        assert mltable_with_full_inputs_types['Sex'].name == 'bool'

    def test_convert_column_types_errors_sdk(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'traits_timeseries')
        mltable = load(path)

        exp_err_msg \
            = "Expect `columns` to be a single string, a non-empty list of strings, or a non-empty tuple of strings"
        with pytest.raises(UserErrorException, match=exp_err_msg):
            mltable.convert_column_types({'datetime': DataType.to_datetime(formats=None)})

        exp_err_msg = 'Expected a non-empty dict\\[Union\\[str, tuple\\[str\\]\\], Union\\[str, mltable.DataType\\]\\]'
        with pytest.raises(UserErrorException, match=exp_err_msg):
            mltable.convert_column_types({})

        exp_err_msg = "Found duplicate column. Cannot convert column 'latitude' to multiple `mltable.DataType`s."
        with pytest.raises(UserErrorException, match=exp_err_msg):
            mltable.convert_column_types({('latitude', 'windSpeed'): DataType.to_float(),
                                          ('wban', 'latitude'): DataType.to_int()})

    def test_convert_column_types_with_mltable_yaml(self, get_data_folder_path):
        string_path = 'mltable_convert_column_types/simple_types_yaml'
        path = os.path.join(get_data_folder_path, string_path)
        mltable = load(path)
        column_types = mltable.to_pandas_dataframe().dtypes
        assert column_types['datetime'].name == 'datetime64[ns]'
        assert column_types['date'].name == 'datetime64[ns]'
        assert column_types['latitude'].name == 'float64'
        assert column_types['stationName'].name == 'object'
        assert column_types['wban'].name == 'int64'
        assert column_types['gender'].name == 'bool'
        assert column_types['only_timevalues'].name == 'datetime64[ns]'

    def test_convert_column_types_with_mltable_yaml_multiple_cols(self, get_data_folder_path):
        string_path = 'mltable_convert_column_types/simple_types_multiple_cols'
        path = os.path.join(get_data_folder_path, string_path)
        mltable = load(path)
        column_types = mltable.to_pandas_dataframe().dtypes
        assert column_types['datetime'].name == 'datetime64[ns]'
        assert column_types['date'].name == 'datetime64[ns]'
        assert column_types['latitude'].name == 'float64'
        assert column_types['windSpeed'].name == 'float64'
        assert column_types['wban'].name == 'int64'
        assert column_types['usaf'].name == 'int64'

    def test_convert_column_types_with_stream_info_no_workspace_sdk(self, get_data_folder_path):
        string_path = 'mltable_convert_column_types/stream_info_uri_formats'
        path = os.path.join(get_data_folder_path, string_path)
        mltable = load(path)
        data_types = {
            'image_url': DataType.to_stream(),
            'long_form_uri': DataType.to_stream(),
            'direct_uri_wasbs': DataType.to_stream(),
            'direct_uri_abfss': DataType.to_stream(),
            'direct_uri_adl': DataType.to_stream()
        }
        new_mltable = mltable.convert_column_types(data_types)
        df = new_mltable.to_pandas_dataframe()
        stream_info_class_name = StreamInfo.__name__
        none_uri = type(df['image_url'][0]).__name__
        long_form_uri = type(df['long_form_uri'][0]).__name__
        direct_uri_wasbs = type(df['direct_uri_wasbs'][0]).__name__
        direct_uri_abfss = type(df['direct_uri_abfss'][0]).__name__
        direct_uri_adl = type(df['direct_uri_adl'][0]).__name__
        assert none_uri == 'NoneType'  # None since this url has no workspace info in it
        assert long_form_uri == stream_info_class_name
        assert direct_uri_wasbs == stream_info_class_name
        assert direct_uri_abfss == stream_info_class_name
        assert direct_uri_adl == stream_info_class_name

    def test_convert_column_types_with_stream_info_with_mltable_yaml(self, get_data_folder_path):
        string_path = 'mltable_convert_column_types/stream_info_yaml'
        path = os.path.join(get_data_folder_path, string_path)
        mltable = load(path)
        df = mltable.to_pandas_dataframe()
        stream_info_class_name = StreamInfo.__name__
        long_form_uri = type(df['long_form_uri'][0]).__name__
        direct_uri_wasbs = type(df['direct_uri_wasbs'][0]).__name__
        direct_uri_abfss = type(df['direct_uri_abfss'][0]).__name__
        direct_uri_adl = type(df['direct_uri_adl'][0]).__name__
        assert long_form_uri == stream_info_class_name
        assert direct_uri_wasbs == stream_info_class_name
        assert direct_uri_abfss == stream_info_class_name
        assert direct_uri_adl == stream_info_class_name

    def test_traits_from_mltable_file(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        data_folder_path = os.path.join(
            cwd, 'data/mltable/traits_timeseries')
        mltable = load(data_folder_path)

        mltable_yaml = yaml.safe_load(mltable._dataflow.to_yaml_string())
        assert mltable.traits.timestamp_column == 'datetime'
        assert mltable.traits.index_columns == ['datetime']
        assert mltable_yaml['traits']['index_columns'] == ['datetime']

        mltable.traits.timestamp_column = 'random_column_name'
        mltable_yaml = yaml.safe_load(mltable._dataflow.to_yaml_string())
        assert mltable.traits.timestamp_column == 'random_column_name'
        assert mltable_yaml['traits']['timestamp_column'] == 'random_column_name'

        mltable.traits.index_columns = ['col1', 'col2']
        mltable_yaml = yaml.safe_load(mltable._dataflow.to_yaml_string())
        assert mltable.traits.index_columns == ['col1', 'col2']
        assert mltable_yaml['traits']['index_columns'] == ['col1', 'col2']

    def test_set_get_traits(self, get_mltable):
        mltable = get_mltable
        mltable.traits.index_columns = ['PassengerId']
        mltable.traits.timestamp_column = 'Pclass'
        assert mltable.traits.index_columns == ['PassengerId']
        assert mltable.traits.timestamp_column == 'Pclass'

    def test_take(self, get_mltable):
        mltable = get_mltable
        new_mltable = mltable.take(count=5)

        assert '- take: 5' in new_mltable._dataflow.to_yaml_string()
        df = new_mltable.to_pandas_dataframe()
        assert df.shape[0] == 5

    def test_take_invalid_count(self, get_mltable):
        for invalid in -1, 0, "number":
            with pytest.raises(UserErrorException, match='Number of rows must be a positive integer'):
                get_mltable.take(count=invalid)

    def test_show(self, get_mltable):
        mltable = get_mltable
        new_mltable = mltable.show(count=5)
        assert new_mltable.shape[0] == 5

    def test_show_invalid_count(self, get_mltable):
        for invalid in -1, 0, "number":
            with pytest.raises(UserErrorException, match='Number of rows must be a positive integer'):
                get_mltable.show(count=invalid)

    def test_take_random_sample_no_seed(self, get_mltable):
        mltable = get_mltable
        new_mltable = mltable.take_random_sample(probability=.05, seed=None)
        new_mltable.to_pandas_dataframe()
        assert 'probability: 0.05' in new_mltable._dataflow.to_yaml_string()

    def test_take_random_sample_with_seed(self, get_mltable):
        mltable = get_mltable
        new_mltable = mltable.take_random_sample(probability=.05, seed=5)
        new_mltable.to_pandas_dataframe()
        assert 'probability: 0.05' in new_mltable._dataflow.to_yaml_string()

    def test_take_random_sample_invalid_prob(self, get_mltable):
        for invalid in -.01, 0.0, 'number':
            with pytest.raises(UserErrorException, match='Probability should an float greater than 0 and less than 1'):
                get_mltable.take_random_sample(probability=invalid)

    def add_step_at_start(self, mltable, idx):
        mltable_info_dict = mltable_as_dict(mltable)
        added_transformations = mltable_info_dict['transformations']

        # only one transformation added
        assert len(added_transformations) == 1
        assert list(added_transformations[0].keys())[0] == 'read_delimited'

        # add `take 5` step, if `idx` is `None` resort to default arg (also `None`)
        take_dataflow = mltable._dataflow.add_transformation('take', 5, idx)
        added_transformations = yaml.safe_load(take_dataflow.to_yaml_string())[
            'transformations']

        # two transformations added, `take 5` at end
        assert len(added_transformations) == 2
        assert added_transformations[0] == {'take': 5}

    def test_add_step_at_start_zero_idx(self, get_mltable):
        mltable = get_mltable
        self.add_step_at_start(mltable, 0)

    def test_add_step_at_start_neg_idx(self, get_mltable):
        mltable = get_mltable
        self.add_step_at_start(mltable, -1)

    def add_step_at_end(self, mltable, idx):
        mltable_info_dict = mltable_as_dict(mltable)
        added_transformations = mltable_info_dict['transformations']

        # only one transformation added
        assert len(added_transformations) == 1
        assert list(added_transformations[0].keys())[0] == 'read_delimited'

        # add `take 5` step to end
        if idx is None:
            take_dataflow = mltable._dataflow.add_transformation('take', 5)
        else:
            take_dataflow = mltable._dataflow.add_transformation(
                'take', 5, idx)
        added_transformations = yaml.safe_load(take_dataflow.to_yaml_string())[
            'transformations']

        # two transformations added, `take 5` at end
        assert len(added_transformations) == 2
        assert added_transformations[-1] == {'take': 5}

    def test_add_step_at_end_none_idx(self, get_mltable):
        mltable = get_mltable
        self.add_step_at_end(mltable, None)

    def test_add_step_at_end_pos_idx(self, get_mltable):
        mltable = get_mltable
        self.add_step_at_end(mltable, 1)

    def test_add_mult_steps(self, get_mltable):
        mltable = get_mltable
        mltable_info_dict = mltable_as_dict(mltable)
        added_transformations = mltable_info_dict['transformations']

        # only one transformation added
        assert len(added_transformations) == 1
        assert list(added_transformations[0].keys())[0] == 'read_delimited'

        # add `take 10` step
        mltable = mltable.take(10)
        mltable_info_dict = mltable_as_dict(mltable)
        added_transformations = mltable_info_dict['transformations']

        # two transformations added, `take 10` at end
        assert len(added_transformations) == 2
        assert added_transformations[-1] == {'take': 10}

        # add `take 20` step to the middle
        take_dataflow = mltable._dataflow.add_transformation('take', 20, -1)
        added_transformations = yaml.safe_load(take_dataflow.to_yaml_string())[
            'transformations']

        # three transformation steps added, `take 20` in middle and `take 10` at end
        assert len(added_transformations) == 3
        assert added_transformations[-2] == {'take': 20}
        assert added_transformations[-1] == {'take': 10}

    def test_drop_columns_with_string(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'traits_timeseries')
        mltable = load(path)
        pre_drop_columns = mltable.to_pandas_dataframe().columns
        assert "elevation" in pre_drop_columns
        new_mltable = mltable.drop_columns(columns="elevation")
        post_drop_columns = new_mltable.to_pandas_dataframe().columns
        # all columns in df.columns except elevation should be present in original mltable columns
        assert set(post_drop_columns).issubset(pre_drop_columns)
        assert "elevation" not in post_drop_columns

    def test_drop_columns_with_list(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'traits_timeseries')
        mltable = load(path)
        pre_drop_columns = mltable.to_pandas_dataframe().columns
        columns_to_drop = ["latitude", "elevation", "usaf"]
        assert all(col in pre_drop_columns for col in columns_to_drop)
        new_mltable = mltable.drop_columns(columns=columns_to_drop)
        post_drop_columns = new_mltable.to_pandas_dataframe().columns
        assert all(col not in post_drop_columns for col in columns_to_drop)

    def test_drop_columns_traits(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'traits_timeseries')
        mltable = load(path)

        assert "datetime" == mltable.traits.timestamp_column
        assert "datetime" == mltable.traits.index_columns[0]

        with pytest.raises(UserErrorException, match='Columns in traits must be kept and cannot be dropped'):
            mltable.drop_columns(columns="datetime")

        with pytest.raises(UserErrorException, match='Columns in traits must be kept and cannot be dropped'):
            mltable.drop_columns(columns=["datetime", "index"])

        mltable.drop_columns(columns="index")
        mltable.drop_columns(columns=["elevation", "index"])

    def test_keep_columns_with_string(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'mltable_with_type')
        mltable = load(path)
        pre_keep_columns = mltable.to_pandas_dataframe().columns
        assert "Name" in pre_keep_columns
        new_mltable = mltable.keep_columns(columns="Name")
        post_keep_columns = new_mltable.to_pandas_dataframe().columns
        assert len(post_keep_columns) == 1
        assert "Name" in post_keep_columns

    def test_keep_columns_with_list(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'mltable_with_type')
        mltable = load(path)
        pre_keep_columns = mltable.to_pandas_dataframe().columns
        columns_to_keep = ["Name", "Age"]
        assert all(col in pre_keep_columns for col in columns_to_keep)
        new_mltable = mltable.keep_columns(columns=columns_to_keep)
        post_keep_columns = new_mltable.to_pandas_dataframe().columns
        assert len(post_keep_columns) == 2
        assert all(col in post_keep_columns for col in columns_to_keep)

    def test_keep_columns_traits(self, get_data_folder_path):
        path = os.path.join(get_data_folder_path, 'traits_timeseries')
        mltable = load(path)

        assert "elevation" != mltable.traits.timestamp_column
        assert "elevation" != mltable.traits.index_columns[0]
        assert "datetime" == mltable.traits.timestamp_column
        assert "datetime" == mltable.traits.index_columns[0]

        with pytest.raises(UserErrorException, match='Columns in traits must be kept and cannot be dropped'):
            mltable.keep_columns(columns="elevation")

    def test_create_mltable_from_parquet_files_with_local_path(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/crime.parquet'}]
        mltable = from_parquet_files(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (10, 22)
        assert list(df.columns) == [
            'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Location Description',
            'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code', 'X Coordinate',
            'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]

    def test_create_mltable_from_parquet_files_with_local_folder_path(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'folder': 'data/mltable/mltable_folder_parquet'}]
        mltable = from_parquet_files(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (20, 22)
        assert list(df.columns) == [
            'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Location Description',
            'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code', 'X Coordinate',
            'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]

    def test_create_mltable_from_parquet_files_with_local_paths(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/mltable/mltable_folder_parquet/crime.parquet'},
                 {'file': 'data/mltable/mltable_folder_parquet/crime_2.parquet'}]
        mltable = from_parquet_files(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (20, 22)
        assert list(df.columns) == [
            'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Location Description',
            'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code', 'X Coordinate',
            'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]

    def test_create_mltable_from_parquet_files_with_local_abs_path(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        exp_path_1 = os.path.normpath(
            os.path.join(cwd, 'data/crime.parquet'))
        paths = [{'file': exp_path_1}]
        mltable = from_parquet_files(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (10, 22)
        assert list(df.columns) == [
            'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description', 'Location Description',
            'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code', 'X Coordinate',
            'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]

    def test_create_mltable_from_parquet_files_include_path_column(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/crime.parquet'}]
        mltable = from_parquet_files(paths, include_path_column=True)
        df = mltable_was_loaded(mltable)
        assert df.shape == (10, 23)
        assert list(df.columns) == [
            'Path', 'ID', 'Case Number', 'Date', 'Block', 'IUCR', 'Primary Type', 'Description',
            'Location Description', 'Arrest', 'Domestic', 'Beat', 'District', 'Ward', 'Community Area', 'FBI Code',
            'X Coordinate', 'Y Coordinate', 'Year', 'Updated On', 'Latitude', 'Longitude', 'Location'
        ]

    def test_create_mltable_from_paths_with_local_abs_path(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        exp_path_1 = os.path.normpath(
            os.path.join(cwd, 'data/crime-spring.csv'))
        paths = [{'file': exp_path_1}]
        mltable = from_paths(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (1, 1)
        assert list(df.columns) == ['Path']

    def test_create_mltable_from_paths_with_local_path(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/crime-spring.csv'}]
        mltable = from_paths(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (1, 1)
        assert list(df.columns) == ['Path']

    def test_create_mltable_from_paths_with_local_paths(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/crime-spring.csv'},
                 {'file': 'data/crime-winter.csv'}]
        mltable = from_paths(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (2, 1)
        assert list(df.columns) == ['Path']

    def test_create_mltable_from_paths_with_folder_local_path(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'folder': 'data/mltable/mltable_folder'}]
        mltable = from_paths(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (2, 1)
        assert list(df.columns) == ['Path']

    def test_create_mltable_from_paths_with_cloud_path(self):
        paths = [
            {'file': "https://dprepdata.blob.core.windows.net/demo/Titanic2.csv"}]
        mltable = from_paths(paths)
        df = mltable_was_loaded(mltable)
        assert df.shape == (1, 1)
        assert list(df.columns) == ['Path']

    def check_random_split(self, mltable, percent):
        mltable = mltable.take(20)
        a, b = mltable.random_split(percent=percent, seed=10)

        a = a.to_pandas_dataframe()
        b = b.to_pandas_dataframe()
        c = mltable.to_pandas_dataframe()

        bound = .2
        # assert a have ~`percent`% of c's data
        assert abs(percent - (len(a) / len(c))) <= bound

        # assert has ~(1 - `percent`)% (the remainder) of c's data
        assert abs((1 - percent) - (len(b) / len(c))) <= bound

        # assert the number of elements in a and b equals c
        assert (len(a) + len(b)) == len(c)

        # show a & b are both in c
        assert c.merge(a).equals(a)
        assert c.merge(b).equals(b)

        # assert a and b have no overlap
        assert a.merge(b).empty

    def test_random_split_even(self, get_mltable):
        mltable = get_mltable
        self.check_random_split(mltable, .5)

    def test_random_split_uneven(self, get_mltable):
        mltable = get_mltable
        self.check_random_split(mltable, .7)

    def test_get_partition_count(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        exp_path_1 = os.path.normpath(
            os.path.join(cwd, 'data/crime-spring.csv'))
        paths = [{'file': exp_path_1}]
        mltable = from_delimited_files(paths)
        assert mltable.get_partition_count() == 1

        mltable = mltable._with_partition_size(200)
        assert mltable.get_partition_count() == 11

        # with partition_size unit
        mltable = mltable._with_partition_size(500, 'kb')
        assert mltable.get_partition_count() == 1

    def test_update_partition_size_with_parquet(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/crime.parquet'}]
        mltable = from_parquet_files(paths)
        exp_err_msg = 'transformation step read_delimited or read_json_lines is required to update partition_size'
        with pytest.raises(UserErrorException) as e:
            mltable._with_partition_size(partition_size=200)
            assert exp_err_msg in e.message

    def test_mltable_from_delimited_files_is_tabular(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        exp_path_1 = os.path.normpath(
            os.path.join(cwd, 'data/crime-spring.csv'))
        paths = [{'file': exp_path_1}]
        mltable = from_delimited_files(paths)
        assert mltable._is_tabular is True

    def test_mltable_from_parquet_is_tabular(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/crime.parquet'}]
        mltable = from_parquet_files(paths)
        assert mltable._is_tabular is True

    def test_mltable_from_json_files_is_tabular(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        os.chdir(cwd)
        paths = [{'file': 'data/order.jsonl'}]
        mltable = from_json_lines_files(paths)
        assert mltable._is_tabular is True

    def test_mltable_load_is_tabular(self, get_dir_folder_path):
        cwd = get_dir_folder_path
        test_mltable_dir = os.path.join(
            cwd, 'data/mltable/mltable_file')
        mltable = load(test_mltable_dir)
        assert mltable._is_tabular is False

    def test_save_relative_to_non_colocated_directory_then_load(self, get_data_folder_path):
        mltable_dirc_path = os.path.join(get_data_folder_path, 'mltable_paths')
        mltable = load(mltable_dirc_path)

        with tempfile.TemporaryDirectory() as td:
            mltable.save(td, colocated=False)
            new_mltable, new_mltable_yaml_dict, new_mltable_yaml_file_dict = get_mltable_and_dicts(td)
            abs_relative_save_path = os.path.join(mltable_dirc_path, os.path.join('subfolder', 'Titanic2.csv'))
            abs_save_path = os.path.splitdrive(get_data_folder_path)[0] + os.path.normpath('/this/is/a/fake/path.csv')

            # paths after saving but before loading
            # saved paths & loaded path attributes are the same
            list_of_dicts_equal([{'file': abs_save_path}, {'file': abs_relative_save_path}],
                                new_mltable_yaml_file_dict['paths'],
                                new_mltable.paths)

            # paths after being loaded to MLTable's Dataflow, only change is `file://` is prepended to each path
            list_of_dicts_equal([{k: 'file://' + v for k, v in path_dict.items()}
                                for path_dict in new_mltable_yaml_file_dict['paths']],
                                new_mltable_yaml_dict['paths'])

    def test_save_relative_to_colocated_directory_then_load(self):
        with tempfile.TemporaryDirectory() as td:
            a_dirc = os.path.join(td, 'a')
            os.mkdir(a_dirc)

            b_dirc = os.path.join(td, 'b')
            os.mkdir(b_dirc)

            dirc_mount = os.path.splitdrive(os.getcwd())[0]

            # enter the "relative path" as absolute
            abs_paths = [{'file': dirc_mount + os.path.normpath('/this/is/absolute/path.csv')},
                         {'file': os.path.normpath(os.path.join(a_dirc, 'this/is/relative/path.csv'))}]
            rel_paths = [{'file': dirc_mount + os.path.normpath('/this/is/absolute/path.csv')},
                         {'file': os.path.normpath('this/is/relative/path.csv')}]

            mltable = from_paths(abs_paths)

            # save & load initial MLTable
            mltable.save(a_dirc, colocated=False)
            loaded_mltable = load(a_dirc)
            loaded_mltable, loaded_mltable_yaml_dict, loaded_mltable_yaml_file_dict \
                = get_mltable_and_dicts(a_dirc)

            # paths in MLTable's Dataflow after loading
            loaded_paths = [{k : 'file://' + v for k, v in path_dict.items()} for path_dict in abs_paths]
            list_of_dicts_equal(loaded_paths, loaded_mltable_yaml_dict['paths'])

            # paths are same before & after loading
            list_of_dicts_equal(rel_paths, loaded_mltable.paths, loaded_mltable_yaml_file_dict['paths'])

            # save to adjacent directory & reload
            loaded_mltable.save(b_dirc, colocated=False)
            reloaded_mltable, reloaded_mltable_yaml_dict, reloaded_mltable_yaml_file_dict \
                = get_mltable_and_dicts(b_dirc)

            # after resaving & reloading absolute paths are same but relative paths are adjusted
            reloaded_mltable_paths = [{k: v if os.path.isabs(v) else os.path.relpath(os.path.join(a_dirc, v), b_dirc)
                                      for k, v in path_dict.items()} for path_dict in rel_paths]
            list_of_dicts_equal(reloaded_mltable.paths,
                                reloaded_mltable_paths,
                                reloaded_mltable_yaml_file_dict['paths'])

            # absolute paths are kept consistent across two sequentiual loads
            list_of_dicts_equal(loaded_mltable_yaml_dict['paths'], reloaded_mltable_yaml_dict['paths'])

    def test_save_load_dataframe(self, get_mltable_data_folder_path):
        with tempfile.TemporaryDirectory() as td:
            a_dirc = os.path.join(td, 'a')
            b_dirc = os.path.join(td, 'b')

            # copy MLTable file & data files
            shutil.copytree(get_mltable_data_folder_path, a_dirc)

            og_mltable = load(a_dirc)
            og_dataframe = og_mltable.to_pandas_dataframe()
            og_mltable.save(b_dirc, colocated=False)

            loaded_mltable, _, loaded_mltable_yaml_file_dict = get_mltable_and_dicts(b_dirc)

            # loaded paths are relative
            for path_dict in loaded_mltable_yaml_file_dict['paths']:
                assert all(not os.path.isabs(path) for _, path in path_dict.items())

            loaded_dataframe = loaded_mltable.to_pandas_dataframe()

            assert og_dataframe is not None
            assert not og_dataframe.empty
            assert og_dataframe.equals(loaded_dataframe)


@pytest.mark.mltable_sdk_unit_test_windows
class TestMLTableSaveAndLoadWindowsOnly:
    def test_load_save_diff_drive(self, get_data_folder_path):
        # all files on loaded MLTable are on on D drive / mount, save to C drive / mount (temp directory)
        mltable_dirc_path = get_data_folder_path
        mltable_path = os.path.join(mltable_dirc_path, 'mltable_windows')
        og_mltable = load(mltable_path)

        with tempfile.TemporaryDirectory() as td:
            og_mltable.save(td, colocated=False)
            new_mltable, new_mltable_yaml_dict, new_mltable_yaml_file_dict = get_mltable_and_dicts(td)
            relative_file_save_path = os.path.join(mltable_path, 'relative\\path\\file.csv')

            # explit check for paths after saving but before loading
            # paths are same before & after loading
            list_of_dicts_equal([{'file': 'D:\\absolute\\path\\file.csv'}, {'file': relative_file_save_path}],
                                new_mltable_yaml_file_dict['paths'],
                                new_mltable.paths)

            # explicit check for paths after loading
            list_of_dicts_equal([{'file': 'file://D:\\absolute\\path\\file.csv'},
                                 {'file': 'file://' + relative_file_save_path}],
                                new_mltable_yaml_dict['paths'])

    def test_load_save_same_drive(self, get_data_folder_path):
        # absolute file in loaded MLTable is on C drive / mount, save to C drive / mount (temp directory)
        mltable_dirc_path = get_data_folder_path
        mltable_path = os.path.join(mltable_dirc_path, 'mltable_windows_c_drive')
        og_mltable = load(mltable_path)

        with tempfile.TemporaryDirectory() as td:
            og_mltable.save(td, colocated=False)
            new_mltable, new_mltable_yaml_dict, new_mltable_yaml_file_dict = get_mltable_and_dicts(td)
            relative_file_save_path = os.path.join(mltable_path, 'relative\\path\\file.csv')
            absolute_file_save_path = os.path.relpath('C:\\absolute\\path\\file.csv', td)

            # explicit ceheck for paths after saving but before loading
            # paths are same before & after loading
            list_of_dicts_equal([{'file': absolute_file_save_path}, {'file': relative_file_save_path}],
                                new_mltable_yaml_file_dict['paths'],
                                new_mltable.paths)

            # explicit check for paths after reloading
            list_of_dicts_equal([{'file': 'file://C:\\absolute\\path\\file.csv'},
                                 {'file': 'file://' + relative_file_save_path}],
                                new_mltable_yaml_dict['paths'])
