import logging
import logging.config
from typing import Any, Dict, List, Optional
from scrapy import Spider
from nem.db.models.nemstore import FacilityScada
from nem.utils.pipelines import check_spider_pipeline

# logging.config.fileConfig("~/repos/nem/nem/settings/logconfig.yaml")
logger = logging.getLogger(__name__)

def unit_scada_generate_facility_scada(
    records,
    spider=None,
    network: NetworkSchema = NetworkNEM,
    interval_field: str = "SETTLEMENTDATE",
    facility_code_field: str = "DUID",
    date_format: Optional[str] = None,
    power_field: Optional[str] = None,
    energy_field: Optional[str] = None,
    is_forecast: bool = False,
    primary_key_track: bool = False,
    groupby_filter: bool = True,
    created_by: str = None,
    limit: int = 0,
    duid: str = None,
) -> List[Dict]:
    created_at = datetime.now()
    primary_keys = []
    return_records = []

    created_by = ""

    if spider and hasattr(spider, "name"):
        created_by = spider.name

    for row in records:

        trading_interval = parse_date(
            row[interval_field],
            network=network,
            dayfirst=False,
            date_format=date_format,
        )

        # if facility_code_field not in row:
        # logger.error("Invalid row no facility_code")
        # continue

        facility_code = normalize_duid(row[facility_code_field])

        if duid and facility_code != duid:
            continue

        if primary_key_track:
            pkey = (trading_interval, facility_code)

            if pkey in primary_keys:
                continue

            primary_keys.append(pkey)

        generated = None

        if power_field and power_field in row:
            generated = clean_float(row[power_field])

            if generated:
                generated = float_to_str(generated)

        energy = None

        if network == NetworkWEM and power_field and not energy_field:
            _generated = clean_float(row[power_field])

            if _generated:
                energy = str(_generated / 2)

        if energy_field and energy_field in row:
            _energy = clean_float(row[energy_field])

            if _energy:
                energy = float_to_str(_energy)

        __rec = {
            "created_by": created_by,
            "created_at": created_at,
            "updated_at": None,
            "network_id": network.code,
            "trading_interval": trading_interval,
            "facility_code": facility_code,
            "generated": generated,
            "eoi_quantity": energy,
            "is_forecast": is_forecast,
            "energy_quality_flag": 0,
        }

        return_records.append(__rec)

        if limit > 0 and len(return_records) >= limit:
            break

    if not groupby_filter:
        return return_records

    return_records_grouped = {}

    for pk_values, rec_value in groupby(
        return_records,
        key=lambda r: (
            r.get("network_id"),
            r.get("trading_interval"),
            r.get("facility_code"),
        ),
    ):
        if pk_values not in return_records_grouped:
            return_records_grouped[pk_values] = list(rec_value).pop()

    return_records = list(return_records_grouped.values())

    return return_records


def generate_balancing_summary(
    records: List[Dict],
    spider: Spider,
    interval_field: str = "SETTLEMENTDATE",
    network_region_field: str = "REGIONID",
    price_field: Optional[str] = None,
    network: NetworkSchema = NetworkNEM,
    limit: int = 0,
) -> List[Dict]:
    created_at = datetime.now()
    # primary_keys = []
    return_records = []

    created_by = ""

    if spider and hasattr(spider, "name"):
        created_by = spider.name

    for row in records:

        trading_interval = parse_date(row[interval_field], network=network, dayfirst=False)

        network_region = None

        if network_region_field and network_region_field in row:
            network_region = row[network_region_field]

        price = None

        if price_field and price_field in row:
            price = clean_float(row[price_field])

            if price:
                price = float_to_str(price)

        __rec = {
            "created_by": created_by,
            "created_at": created_at,
            "updated_at": None,
            "network_id": network.code,
            "network_region": network_region,
            "trading_interval": trading_interval,
            "price": price,
        }

        return_records.append(__rec)

        if limit > 0 and len(return_records) >= limit:
            break

    return return_records


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

if __name__ == "__main__":
    logger.debug("test")
