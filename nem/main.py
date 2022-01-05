from utils.downloader import NemwebHTMLParser, url_downloader
from pprint import pprint

u = url_downloader("http://www.nemweb.com.au/Reports/CURRENT/ROOFTOP_PV/ACTUAL/")
udec = u.decode("utf-8")

parser = NemwebHTMLParser()
parser.feed(udec)
z = parser.ziplist
d = parser.to_dict()

print(d)

isequallength = len(d["zipfile"]) == len(d["zipdate"]) == len(d["zipdate"])
print(f"List lengths are equal: {isequallength}")