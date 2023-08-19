import argparse
import sys
from ngdataenginterface.analytical import Analytical
from ngdataenginterface.spark_manager import SparkManager
from ngdataenginterface.aws_interface import AWSInterface
from ngdataenginterface.table import *
from ngdataenginterface.utils import *
from ngdataenginterface.process import *
import logging

# import pyspark packages
from pyspark.sql.types import *

from pyspark.sql import functions as F


def raw_to_trusted(
    spark: SparkManager,
    aws_interface: AWSInterface,
    env: str,
    current_step_params,
    execution_date: datetime,
    overwrite: bool,
    kwargs: dict,
):
    print(f"Raw to Trusted - Execution Date: {execution_date} \n")
    table_params = current_step_params
    merge_params = table_params["merge"]

    read_path = handle_input_api(env, table_params["read"])
    write_path = handle_input_api(env, table_params["write"])

    read_params = PathParams.from_dict(read_path)
    write_params = PathParams.from_dict(write_path)
    meta = MetaParams(date=execution_date, overwrite=overwrite)

    read_table = Table(
        path=read_params, meta=meta, aws_interface=aws_interface, spark_manager=spark
    )

    write_table = Table(
        path=write_params, meta=meta, aws_interface=aws_interface, spark_manager=spark
    )

    process = Process(
        read=read_table,
        write=write_table,
        merge=merge_params,
    )

    if process.read.check_for_new_data():
        if kwargs.get("merge"):
            # if there is new data, we merge it with the previous partition
            df = process.merge_previous_partition()
        else:
            # if there is new data, we just read the new data
            df = process.read.read_table()
    else:
        # if there is no new data, we just read the previous partition table
        # and write it to the new partition
        df = process.read_previous_partition_table()

    # write the table to the new partition writting path
    process.write.write_table(df=df)
    return
