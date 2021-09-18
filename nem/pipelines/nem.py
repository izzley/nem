import logging
from typing import Any, Dict, List, Optional
from nem.utils.pipelines import check_spider_pipeline

logger = logging.getLogger(__name__)

TABLE_PROCESSOR_MAP = {
    "DISPATCH_CASE_SOLUTION": "process_case_solutions",
    "DISPATCH_INTERCONNECTORRES": "process_dispatch_interconnectorres",
    "DISPATCH_PRICE": "process_trading_price",
    "DISPATCH_REGIONSUM": "process_dispatch_regionsum",
    "DISPATCH_UNIT_SCADA": "process_unit_scada",
    "DISPATCH_UNIT_SOLUTION": "process_unit_solution",
    "METER_DATA_GEN_DUID": "process_meter_data_gen_duid",
    "ROOFTOP_ACTUAL": "process_rooftop_actual",
    "ROOFTOP_FORECAST": "process_rooftop_forecast",
    "TRADING_PRICE": "process_trading_price",
    "TRADING_REGIONSUM": "process_trading_regionsum",
}

class NemwebUnitScadaOpenNEMStorePipeline(object):
    @check_spider_pipeline
    def process_item(self, item: Dict[str, Any], spider=None) -> List:
        if not item:
            msg = "NemwebUnitScadaOpenNEMStorePipeline"
            if spider and hasattr(spider, "name"):
                msg = spider.name
            Logger.error("No item in pipeline: {}".format(msg))
            return {}

        if "tables" not in item:
            print(item)
            raise Exception("Invalid item - no tables located")

        if not isinstance(item["tables"], dict):
            raise Exception("Invalid item - no tables located")

        tables = item["tables"]

        ret = []

        for table in tables.values():
            if "name" not in table:
                logger.info("Invalid table found")
                continue

            table_name = table["name"]

            if table_name not in TABLE_PROCESSOR_MAP:
                logger.info("No processor for table %s", table_name)
                continue

            process_meth = TABLE_PROCESSOR_MAP[table_name]

            if process_meth not in globals():
                logger.info("Invalid processing function %s", process_meth)
                continue

            logger.info("processing table {}".format(table_name))

            record_item = None

            record_item = globals()[process_meth](table, spider=spider)

            if record_item:
                ret.append(record_item)

        return ret