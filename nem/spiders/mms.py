# import logging
from datetime import datetime
from io import BytesIO
from typing import Dict, Generator
from zipfile import ZipFile
import re

import scrapy
from dateutil.rrule import MONTHLY
from nem.utils.handlers import _handle_zip, chain_streams
from nem.utils.mime import mime_from_content, mime_from_url, decode_bytes
from nem.utils.dates import date_iso_str, date_series
from nem.pipelines import ExtractCSV

# logger = logging.getLogger('mms_dispatch')

MMS_URL = 'http://nemweb.com.au/Data_Archive/Wholesale_Electricity/MMSDM/{year}/MMSDM_{year}_{month}/MMSDM_Historical_Data_SQLLoader/DATA/PUBLIC_DVD_{table}_{year}{month}010000.zip'

class MMSArchiveBulkSpider(scrapy.Spider):

    name = 'mms_dispatch'
    table = 'DISPATCH_UNIT_SCADA'

    # interactive shell of spider parse response
    # https://docs.scrapy.org/en/latest/topics/shell.html#invoking-the-shell-from-spiders-to-inspect-responses
    # Let shell_obj_response = True to enable
    shell_obj_response = False
    
    pipelines = set([ExtractCSV])

    def start_requests(self):
        start_date = datetime(2021, 4, 1)
        end_date = datetime(2021, 6, 1)
        for date in date_series(start_date, end_date, _freq=MONTHLY):
            url_params = {
                'year': date.strftime('%Y'),
                'month': date.strftime('%m'),
                'table': self.table,
            }


            req_url = MMS_URL.format(**url_params)
            
            yield scrapy.Request(req_url, callback=self.parse)


    def parse(self, response) -> Generator[Dict, None, None]:

        self.logger.info("running mms_spider parse")

        if self.shell_obj_response:
            from scrapy.shell import inspect_response
            inspect_response(response, self)

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
        # item["log_name"] = re.findall('DATA/(.*).zip', response.url)[0]

        yield item

class MMSArchivePriceSpider(MMSArchiveBulkSpider):
    # price_dispatch
    name = "au.mms.archive.dispatch_price"

    pipelines = set(
        [
            ExtractCSV,
            # NemwebUnitScadaOpenNEMStorePipeline,
        ]
    )

    tables = ["DISPATCHPRICE"]