# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml.dataprep import UserErrorException
from azureml.dataprep.api.mltable._validation_and_error_handler import _RSLEX_USER_ERROR_VALUES


def _validate_downloads(download_records, ignore_not_found, logger):
    if not download_records:
        return []

    from azureml.dataprep.native import StreamInfo, DataPrepError
    downloaded_files = []
    errors = []
    for record in download_records:
        value = record['DestinationFile']
        if isinstance(value, StreamInfo):
            downloaded_files.append(value.resource_identifier)
        elif isinstance(value, DataPrepError):
            resource_identifier = value.originalValue
            error_code = value.errorCode
            if ignore_not_found and error_code == 'Microsoft.DPrep.ErrorValues.SourceFileNotFound':
                logger.warning(f"'{resource_identifier}' hasn't been downloaded as it was not present at the source. \
                               Download is proceeding.")
            else:
                errors.append((resource_identifier, error_code))
        else:
            raise RuntimeError(f'Unexpected error during file download: {value}')

    if errors:
        _download_error_handler(errors)
    return downloaded_files


def _download_error_handler(errors):  # TODO call from azureml.dataprep
    non_user_errors = list(filter(lambda x: x[1] not in _RSLEX_USER_ERROR_VALUES, errors))
    if non_user_errors:
        raise RuntimeError(f'System errors occured during downloading: {non_user_errors}')
    errors = '\n'.join(map(str, errors))
    raise UserErrorException(f'Some files have failed to download: {errors}')
