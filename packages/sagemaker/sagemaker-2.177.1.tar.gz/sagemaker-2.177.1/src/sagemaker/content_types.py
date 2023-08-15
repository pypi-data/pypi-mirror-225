# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
"""This module is for SageMaker content types."""
from __future__ import absolute_import
from typing import List, Optional

from sagemaker.jumpstart import artifacts, utils as jumpstart_utils


def retrieve_options(
    region: Optional[str] = None,
    model_id: Optional[str] = None,
    model_version: Optional[str] = None,
    tolerate_vulnerable_model: bool = False,
    tolerate_deprecated_model: bool = False,
) -> List[str]:
    """Retrieves the supported content types for the model matching the given arguments.

    Args:
        region (str): The AWS Region for which to retrieve the supported content types.
            Defaults to ``None``.
        model_id (str): The model ID of the model for which to
            retrieve the supported content types. (Default: None).
        model_version (str): The version of the model for which to retrieve the
            supported content types. (Default: None).
        tolerate_vulnerable_model (bool): True if vulnerable versions of model
            specifications should be tolerated (exception not raised). If False, raises an
            exception if the script used by this version of the model has dependencies with known
            security vulnerabilities. (Default: False).
        tolerate_deprecated_model (bool): True if deprecated models should be tolerated
            (exception not raised). False if these models should raise an exception.
            (Default: False).
    Returns:
        list: The supported content types to use for the model.

    Raises:
        ValueError: If the combination of arguments specified is not supported.
    """
    if not jumpstart_utils.is_jumpstart_model_input(model_id, model_version):
        raise ValueError(
            "Must specify JumpStart `model_id` and `model_version` when retrieving content types."
        )

    return artifacts._retrieve_supported_content_types(
        model_id,
        model_version,
        region,
        tolerate_vulnerable_model,
        tolerate_deprecated_model,
    )


def retrieve_default(
    region: Optional[str] = None,
    model_id: Optional[str] = None,
    model_version: Optional[str] = None,
    tolerate_vulnerable_model: bool = False,
    tolerate_deprecated_model: bool = False,
) -> str:
    """Retrieves the default content type for the model matching the given arguments.

    Args:
        region (str): The AWS Region for which to retrieve the default content type.
            Defaults to ``None``.
        model_id (str): The model ID of the model for which to
            retrieve the default content type. (Default: None).
        model_version (str): The version of the model for which to retrieve the
            default content type. (Default: None).
        tolerate_vulnerable_model (bool): True if vulnerable versions of model
            specifications should be tolerated (exception not raised). If False, raises an
            exception if the script used by this version of the model has dependencies with known
            security vulnerabilities. (Default: False).
        tolerate_deprecated_model (bool): True if deprecated models should be tolerated
            (exception not raised). False if these models should raise an exception.
            (Default: False).
    Returns:
        str: The default content type to use for the model.

    Raises:
        ValueError: If the combination of arguments specified is not supported.
    """
    if not jumpstart_utils.is_jumpstart_model_input(model_id, model_version):
        raise ValueError(
            "Must specify JumpStart `model_id` and `model_version` when retrieving content types."
        )

    return artifacts._retrieve_default_content_type(
        model_id,
        model_version,
        region,
        tolerate_vulnerable_model,
        tolerate_deprecated_model,
    )


CONTENT_TYPE_JSON = "application/json"
CONTENT_TYPE_CSV = "text/csv"
CONTENT_TYPE_OCTET_STREAM = "application/octet-stream"
CONTENT_TYPE_NPY = "application/x-npy"
