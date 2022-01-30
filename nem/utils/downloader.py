import logging
import re
from html.parser import HTMLParser
from io import BytesIO
from zipfile import ZipFile

# from utils.http import http
import requests

from utils.handlers import _handle_zip, chain_streams
from utils.mime import mime_from_content, mime_from_url

logger = logging.getLogger("opennem.downloader")


def url_downloader(url: str) -> bytes:
    """Downloads a URL and returns content, handling embedded zips and other MIME's"""

    logger.debug("Downloading: {}".format(url))

    # r = http.get(url, verify=False)
    r = requests.get(url, verify=False)

    if not r.ok:
        raise Exception("Bad link returned {}: {}".format(r.status_code, url))

    content = BytesIO(r.content)

    file_mime = mime_from_content(content)

    if not file_mime:
        file_mime = mime_from_url(url)

    if file_mime == "application/zip":
        with ZipFile(content) as zf:
            if len(zf.namelist()) == 1:
                return zf.open(zf.namelist()[0]).read()

            c = []
            stream_count = 0

            for filename in zf.namelist():
                if filename.endswith(".zip"):
                    c.append(_handle_zip(zf.open(filename), "r"))
                    stream_count += 1
                else:
                    c.append(zf.open(filename))

            return chain_streams(c).read()

    return content.getvalue()


class NemwebHTMLParser(HTMLParser):
    """Parse html str and keep list of zipfiles, dates and item number
    """

    def __init__(self):
        HTMLParser.__init__(self)
        self.zipdate = []
        self.ziplist = []
        self.zipitem = []
        self.WEEKDAY = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def handle_data(self, data: str) -> list:
        # if day string exists, must be date and item number
        if any(day in data for day in self.WEEKDAY):
            # strip left and right trailing wrhitespace
            data = data.lstrip().rstrip()
            # trim inner padded spaces to 1
            data = re.sub(r"\s{2,}", " ", data)
            # reverse split trailing item number from date
            data = data.rsplit(' ', 1)
            self.zipdate.append(data[0])
            self.zipitem.append(data[1])

        # some header links begin with www.nemweb or \r\n\n\r. get rid of those
        elif data.startswith("PUBLIC"):
            self.ziplist.append(data)

    def to_dict(self) -> dict:
        return {
            'zipfile': self.ziplist,
            'zipdate': self.zipdate,
            'zipitem': self.zipitem,
        }
