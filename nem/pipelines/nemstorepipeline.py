import logging
import logging.config
from typing import Any, Dict, List, Optional

from nem.settings import config_dict
from nem.settings.logconfig import LoggingDict
from nem.utils.pipelines import check_spider_pipeline

# logging.config.fileConfig("~/repos/nem/nem/settings/logconfig.yaml")
LoggingDict().readyaml()
logger = logging.getLogger(__name__)


def process_unit_scada(table: Dict[str, Any], spider: Spider) -> Dict:
    if "records" not in table:
        raise Exception("Invalid table no records")

    records = table["records"]
    item: Dict[str, Any] = dict()

    item["table_schema"] = FacilityScada
    item["update_fields"] = ["generated"]
    item["records"] = unit_scada_generate_facility_scada(
        records,
        spider,
        power_field="SCADAVALUE",
        network=NetworkNEM,
        date_format="%Y/%m/%d %H:%M:%S",
    )
    item["content"] = ""

    return item


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
            logger.error("No item in pipeline: {}".format(msg))
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
