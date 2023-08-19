from datetime import datetime
from ngdataenginterface.table import Table, PathParams, MetaParams
from ngdataenginterface.aws_interface import AWSInterface
from ngdataenginterface.spark_manager import SparkManager
from typing import Optional
import logging

class Analytical:
    """
    Class Analytical encapsulates the functionality for table read and write operations,
    along with the execution of a specified aggregation function.
    """

    def __init__(
        self,
        read_params: dict,
        write_params: dict,
        aggregation_function,
        date: datetime,
        aws_interface: AWSInterface,
        spark_manager: SparkManager,
        overwrite: bool = False,
        log_level: int = logging.INFO,
        opt_dict: Optional[dict] = None
    ) -> None:
        """
        Instantiates an Analytical object.
        """
        self.read = self._init_tables(
            read_params, date, aws_interface, spark_manager, overwrite, opt_dict
        )
        self.write = self._init_tables(
            write_params, date, aws_interface, spark_manager, overwrite, opt_dict
        )
        self.aggregation_function = aggregation_function
        self.meta = {
            "spark": spark_manager.spark,
            "aws_interface": aws_interface,
            "date": date,
            "session_name": "analytical_tables",
        }
        # Set up logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)  # Set the log level

    @staticmethod
    def _init_tables(
        params: dict,
        date: datetime,
        aws_interface: AWSInterface,
        spark_manager: SparkManager,
        overwrite: bool,
        opt_dict: Optional[dict] = None
    ) -> dict:
        """
        Initialize the tables for data read and write operations.
        """
        tables = {}
        print("\nparams: ", params, "\n")
        for table_name, table_params in params.items():
            path = PathParams.from_dict(table_params)
            meta = MetaParams(date=date, overwrite=overwrite)
            file_system = opt_dict.get("file_system") if opt_dict else 's3'
            tables[table_name] = Table(
                path=path,
                meta=meta,
                aws_interface=aws_interface,
                spark_manager=spark_manager,
                file_system=file_system
            )

        return tables

    def prepare_inputs(self) -> None:
        """
        Prepare the inputs by reading data from the tables.
        """
        self.logger.info("Preparing inputs...")
        try:
            self.inputs = {}
            for table_name, table in self.read.items(): 
                self.inputs[table_name] = {"df": table.read_table()}
            self.logger.debug(f"Prepared inputs: {self.inputs}")
        except Exception as e:
            self.logger.error(f"Failed to prepare inputs: {e}")
            raise e
        self.logger.info("Inputs prepared successfully.")

    def run(self) -> None:
        """
        Run the aggregation function and write the output back to the tables.
        """
        self.logger.info("Running the aggregation function...")
        try:
            self.prepare_inputs()
        except Exception as e:
            return False
        
        try:
            # print("\ninputs: ", self.inputs, "\n")
            # print("\nagg:", self.aggregation_function, "\n")
            self.output = self.aggregation_function(inputs=self.inputs, meta=self.meta)
            self.logger.debug(f"Aggregation output: {self.output}")
            # print("\noutput2: ", self.output, "\n")
            for table_name, table in self.write.items():
                # print("\noutput: ", self.output[table_name], "\n")
                table.write_table(self.output[table_name])
            self.logger.info(
                "Successfully ran the aggregation function and wrote output to tables."
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to run the aggregation function: {e}")
            raise e
