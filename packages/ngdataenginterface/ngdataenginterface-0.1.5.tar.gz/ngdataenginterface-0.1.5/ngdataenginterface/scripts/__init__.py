from ngdataenginterface.scripts.landing_to_raw import landing_to_raw
from ngdataenginterface.scripts.raw_to_trusted import raw_to_trusted
from ngdataenginterface.scripts.trusted_to_analytics import trusted_to_analytics
from ngdataenginterface.scripts.create_analytical_tables import create_analytical_table

PROCESSING_FUNCTIONS = {
    "landing_to_raw": landing_to_raw,
    "raw_to_trusted": raw_to_trusted,
    "trusted_to_analytics": trusted_to_analytics,
    "create_analytical_table": create_analytical_table,
}
