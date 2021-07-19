'''
This module is not called anywhere within nem source code.
'''

from datetime import datetime
from io import BytesIO
from typing import Dict, Generator
from zipfile import ZipFile
import csv

import scrapy
from dateutil.rrule import MONTHLY
from scrapy import shell
from nem.utils.handlers import _handle_zip, chain_streams
from nem.utils.mime import mime_from_content, mime_from_url, decode_bytes
from nem.utils.dates import date_iso_str, date_series
from nem.pipelines import ExtractCSV


MMS_URL = 'http://nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/{year}/MMSDM_{year}_{month}/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_{table}_{year}{month}010000.zip'


name = 'mms_dispatch'
table = 'DISPATCH_UNIT_SCADA'

# interactive shell of spider parse response
# https://docs.scrapy.org/en/latest/topics/shell.html#invoking-the-shell-from-spiders-to-inspect-responses
# Let shell_obj_response = True to enable
shell_obj_response = True

# pipelines = set([ExtractCSV])

def start_requests(self):
    start_date = datetime(2021, 6, 1)
    end_date = datetime(2021, 7, 1)
    for date in date_series(start_date, end_date, _freq=MONTHLY):
        url_params = {
            'year': date.strftime('%Y'),
            'month': date.strftime('%m'),
            'table': table,
        }

        req_url = MMS_URL.format(**url_params)
        
        yield scrapy.Request(req_url, callback=parse)


def parse(response) -> Generator[Dict, None, None]:

    content = None

    file_mime = mime_from_content(response.body)

    if not file_mime:
        file_mime = mime_from_url(response.url)

    if file_mime == "application/zip":
        with ZipFile(BytesIO(response.body)) as zf:
            if len(zf.namelist()) == 1:
                content = zf.open(zf.namelist()[0]).read()

            c = []
            stream_count = 0

            for filename in zf.namelist():
                if filename.endswith(".zip"):
                    c.append(_handle_zip(zf.open(filename), "r"))
                    stream_count += 1
                else:
                    c.append(zf.open(filename))

            content = chain_streams(c).read()
    else:
        content = response.body.getvalue()

    if not content:
        # logger.info("No content from scrapy request")
        print("No content from scrapy request")
        return None

    content_decoded: str = decode_bytes(content)

    item = {}
    item["content"] = content_decoded
    item["extension"] = ".csv"
    item["mime_type"] = file_mime

    return item

import csv
import logging
import zipfile

from nem.utils.pipelines import check_spider_pipeline

logger = logging.getLogger(__name__)

def process_item(item):
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

# item = parse(response)
# csv_item = process_item(item)
