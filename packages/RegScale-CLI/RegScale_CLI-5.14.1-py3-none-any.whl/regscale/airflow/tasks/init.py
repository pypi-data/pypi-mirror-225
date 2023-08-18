"""Initialize init.yaml"""
from typing import Optional, Union
import yaml
from pathlib import Path
import logging

from regscale.airflow.tasks.click import execute_click_command
from regscale.airflow.hierarchy import AIRFLOW_CLICK_OPERATORS as OPERATORS


def get_shared_keys(
    yaml_file_path: Optional[Union[str, Path]] = Path("init.yaml"),
    **context,
) -> list:
    """Get shared keys between init.yaml and a dag_run_conf obj
    :param yaml_file_path: the Path to where the yaml file is expected.
    :param context: context from Airflow DAG
    :returns: a list of shared keys
    :rtype: list
    """
    if "dag_run" not in context:
        logging.error(f"context contains {list(context.keys())}")
    if isinstance(yaml_file_path, str):
        yaml_file_path = Path(yaml_file_path)
    yaml_keys = list(yaml.safe_load(yaml_file_path.open("r")).keys())
    dag_run_conf = context["dag_run"].conf
    shared_keys = set(list(dag_run_conf.keys())).intersection(set(yaml_keys))
    return list(shared_keys)


def set_shared_config_values(**context):
    """Get the shared keys and set them as a variable"""
    dag_run_conf = context["dag_run"].conf
    logging.info(f"{dag_run_conf=}")
    # pull the value of the get_shared_keys task
    shared_keys = context["ti"].xcom_pull(task_ids="get_shared_keys")
    logging.info(f"{shared_keys=}")
    if shared_keys:
        for key in shared_keys:
            value = dag_run_conf[key]
            temp_context = context | {"param": key, "val": value}
            execute_click_command(
                command=OPERATORS["config"]["command"], **temp_context
            )
    else:
        logging.warning(f"No shared keys found: {shared_keys=}")
