from typing import Dict

import pandas as pd

from fiddler.utils.decorators import compat_warning


@compat_warning
def dataset_id_compat(dataset_id: str, dataset_name: str) -> str:
    """
    Check duplicate dataset related params for compatibility.

    :param dataset_id:   The dataset name of which you need the details
    :param dataset_name: The dataset name of which you need the details
    """

    if dataset_id is None and dataset_name is None:
        raise ValueError('Pass either dataset_id or dataset_name')
    if dataset_id is not None and dataset_name is not None:
        raise ValueError('Pass either dataset_id or dataset_name, not both')

    return dataset_id or dataset_name


@compat_warning
def model_id_compat(model_id: str, model_name: str) -> str:
    """
    Check duplicate model related params for compatibility.

    :param model_id:   The model name of which you need the details
    :param model_name: The model name of which you need the details
    """
    if model_id is None and model_name is None:
        raise ValueError('Pass either model_id or model_name')
    if model_id is not None and model_name is not None:
        raise ValueError('Pass either model_id or model_name, not both')
    return model_id or model_name


@compat_warning
def project_id_compat(project_id: str, project_name: str) -> str:
    """
    Check duplicate project related params for compatibility.

    :param project_id:   The project to which the dataset belongs to
    :param project_name: The project to which the dataset belongs to
    """
    if project_id is None and project_name is None:
        raise ValueError('Pass either project_id or project_name')
    if project_id is not None and project_name is not None:
        raise ValueError('Pass either project_id or project_name, not both')
    return project_id or project_name


@compat_warning
def update_event_compat(update_event: bool, is_update: bool) -> bool:
    """
    Check duplicate project related params for compatibility.

    :param update_event: If publish event is of type update
    :param is_update:    If publish event is of type update
    """
    if update_event is not None and is_update is not None:
        raise ValueError('Pass either update_event or is_update, not both')
    return update_event or is_update


@compat_warning
def baseline_id_compat(baseline_id: str, baseline_name: str) -> str:
    """
    Check duplicate baseline related params for compatibility.

    :param baseline_id:    unique identifier for the baseline
    :param baseline_name:  unique identifier for the baseline
    """
    if baseline_id is None and baseline_name is None:
        raise ValueError('Pass either baseline_id or baseline_name')
    if baseline_id is not None and baseline_name is not None:
        raise ValueError('Pass either baseline_id or baseline_name, not both')
    return baseline_id or baseline_name
