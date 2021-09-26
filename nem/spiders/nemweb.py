"""
NEM Base Nemweb Spider is the base nemweb spider that all the other spiders inherit from. It
simply sets up the allowed domain and the default pipelines applied.


"""

# from nem.pipelines.files import LinkExtract
from typing import Dict, Generator
from nem.pipelines import ExtractCSV
from nem.spiders.dirlisting import DirlistingSpider


class NemwebSpider(DirlistingSpider):
    """Base Nemweb spider - sets the allowed domains and the default
    pipelines to apply using the custom pipelines extension"""

    allowed_domains = ["nemweb.com.au"]
    pipelines = set([ExtractCSV])

class NemwebLatestDispatchScada(NemwebSpider):
    name = "au.nem.latest.dispatch_scada"
    start_url = "http://www.nemweb.com.au/Reports/CURRENT/Dispatch_SCADA/"
    limit = 3

        

    # pipelines_extra = set(
    #     [
    #         NemwebUnitScadaOpenNEMStorePipeline,
    #         BulkInsertPipeline,
    #         RecordsToCSVPipeline,
    #     ]
    # )

