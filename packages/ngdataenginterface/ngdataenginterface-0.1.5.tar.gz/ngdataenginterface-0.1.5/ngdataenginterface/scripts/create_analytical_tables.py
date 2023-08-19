import sys
from ngdataenginterface.analytical import Analytical
from ngdataenginterface.spark_manager import SparkManager
from ngdataenginterface.aws_interface import AWSInterface
from ngdataenginterface.utils import *
import logging

# import pyspark packages

from pyspark.sql import functions as F


def create_analytical_table(
    spark: SparkManager,
    aws_interface: AWSInterface,
    env: str,
    current_step_params,
    execution_date: datetime,
    overwrite: bool,
    kwargs: dict,
):
    """Script to aggregated tables from parent tables and save them in S3

    Parameters
    ----------
    spark
        Spark Session
    domain : str
        String refering to the data domain (finance, user_journey, customer_sucess)
    table : str
        String refering to the analytical table name
    env : str
        Environment (prd or dev)
    execution_date : datetime
        Datetime referenced to the airflow scheduler that is used to read and write
    partitioned tables.
    current_step : str
        String that defines the current step that is being executed.

    Returns
    -------
    DataFrame
        The resultant analytical DataFrame

    """

    print(f"Creating Analytical Tables - Execution Date: {execution_date} \n")
    analytical_params = current_step_params

    read_params = {}
    for table_name, table_params in analytical_params["read"].items():
        read_params[table_name] = handle_input_api(
            env, table_params, ng_prefix="ngcash"
        )

    write_params = {}
    for table_name, table_params in analytical_params["write"].items():
        write_params[table_name] = handle_input_api(
            env, table_params, ng_prefix="ngcash"
        )

    analytical_instance = Analytical(
        read_params=read_params,
        write_params=write_params,
        aggregation_function=analytical_params["aggregation_function"],
        date=execution_date,
        aws_interface=aws_interface,
        spark_manager=spark,
        overwrite=overwrite,
        log_level=logging.INFO,
    )

    success = analytical_instance.run()
    if not success:
        print(f"Failed to create Analytical Tables - Current Step Params: {current_step_params}\nExecution Date: {execution_date} \n")
    return
