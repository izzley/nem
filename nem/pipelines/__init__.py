import csv
import logging
import zipfile

from nem.utils.pipelines import check_spider_pipeline

logger = logging.getLogger(__name__)

class ExtractCSV(object):
    @check_spider_pipeline
    def process_item(self, item, spider):
        if not item:
            logger.error("No item to parse")
            return None

        if "content" not in item:
            logger.error("No content in item to parse")
            return item

        content = item["content"]
        del item["content"]

        item["tables"] = {}
        table = {"name": None}

        content_split = content.splitlines()

        datacsv = csv.reader(content_split)

        for row in datacsv:
            if not row or type(row) is not list or len(row) < 1:
                continue

            record_type = row[0]

            if record_type == "C":
                # @TODO csv meta stored in table
                if table["name"] is not None:
                    table_name = table["name"]

                    if table_name in item["tables"]:
                        item["tables"][table_name]["records"] += table[
                            "records"
                        ]
                    else:
                        item["tables"][table_name] = table

            elif record_type == "I":
                if table["name"] is not None:
                    table_name = table["name"]

                    if table_name in item["tables"]:
                        item["tables"][table_name]["records"] += table[
                            "records"
                        ]
                    else:
                        item["tables"][table_name] = table

                table = {}
                table["name"] = "{}_{}".format(row[1], row[2])
                table["fields"] = fields = row[4:]
                table["records"] = []

            elif record_type == "D":
                values = row[4:]
                record = dict(zip(table["fields"], values))

                table["records"].append(record)

        return item