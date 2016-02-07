# data-mining

cd python
source venv/bin/activate

main scraping process
in spiders/dmoz_spider.py

## importing items into a mongoDB database

### start server and database
cd meteor
meteor --port 3004 // server connection URL defined in pipelines.py
// client = MeteorClient('ws://127.0.0.1:3004/websocket', auto_reconnect=True, auto_reconnect_timeout=1)

---
### inspect database and export items to csv
cd meteor
meteor mongo -U // get mongodb URL

collections: "listings", "updatedListings" // in games.js


## SETUP NEW CRAWLER

in dmoz_spider.py:

class DmozSpider(scrapy.Spider):
    name = "houzz"
    allowed_domains = ["www.houzz.com/"]
    start_urls = [
        #"https://boardgamegeek.com/boardgame/27833/steam"
        "http://www.houzz.com/professionals/general-contractor/los-angeles"
    ]
