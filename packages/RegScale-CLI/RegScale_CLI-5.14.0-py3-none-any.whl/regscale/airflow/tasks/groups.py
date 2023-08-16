"""Define pre-made TaskGroups for usage across DAGs."""
from uuid import uuid4

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

from regscale.airflow.tasks.init import get_shared_keys, set_shared_config_values


def setup_task_group(
    dag: DAG,
    setup_tag: str = None,
) -> TaskGroup:
    """Create a TaskGroup for setting up the init.yaml and initialization of the DAG
    :param DAG dag: an Airflow DAG
    :param str setup_tag: a unique identifier for the task
    :returns: a setup TaskGroup
    :rtype TaskGroup:
    """
    if not setup_tag:
        setup_tag = str(uuid4())[
            :8
        ]  # give the task setup group a unique name for tracking
    with TaskGroup(f"setup-{setup_tag}", dag=dag) as setup:
        # initialize the init yaml FIXME - want to have this back in
        # init_yaml = PythonOperator(
        #     task_id=f"initialize_init_yaml-{setup_tag}",
        #     task_group=setup,
        #     python_callable=execute_click_command,
        #     op_kwargs={
        #         "command": OPERATORS["init"]["command"],
        #         "skip_prompts": "",
        #     },
        #     provide_context=True,
        #     dag=dag,
        # )
        # find keys shared between the dag_run.config object and init.yaml
        shared_keys_task = PythonOperator(
            task_id=f"get_shared_keys-{setup_tag}",
            task_group=setup,
            python_callable=get_shared_keys,
            provide_context=True,
            dag=dag,
        )
        # apply the values of those found keys
        config_task = PythonOperator(
            task_id=f"set_config-{setup_tag}",
            task_group=setup,
            python_callable=set_shared_config_values,
            provide_context=True,
            dag=dag,
        )
        # set the order in which to run the tasks
        # init_yaml >> shared_keys_task >> config_task  # FIXME - reimplement when regscale init is fixed
        shared_keys_task >> config_task
        return setup
