

# def process_unit_scada(table: Dict[str, Any], spider: Spider) -> Dict:
#     if "records" not in table:
#         raise Exception("Invalid table no records")

#     records = table["records"]
#     item: Dict[str, Any] = dict()

#     item["table_schema"] = FacilityScada
#     item["update_fields"] = ["generated"]
#     item["records"] = unit_scada_generate_facility_scada(
#         records,
#         spider,
#         power_field="SCADAVALUE",
#         network=NetworkNEM,
#         date_format="%Y/%m/%d %H:%M:%S",
#     )
#     item["content"] = ""

#     return item