import scrapy
from tutorial.items import GameListing

import csv
import sys

def extract_text(response,css_selector,extract_with_links):
    xpath = response.css(css_selector)

    if extract_with_links:
        return extract_wrapped_links(xpath)
    else:
        return clean_text(xpath.xpath("text()").extract())

def extract_wrapped_links(xpath):
    text_in_nodes = []
    subitems = xpath.xpath("div")

    for item in subitems:
        text = item.xpath("a/text()").extract()
        if len(text)>0:
            text_in_nodes.append(clean_text(text))

    return ', '.join(text_in_nodes)

def clean_text(text):
    if len(text)>0:
        return text[0].encode('ascii','ignore').strip().replace("\n","").replace("\t","")
    else:
        return 'null';

class DmozSpider(scrapy.Spider):
    name = "bgg"
    allowed_domains = ["boardgamegeek.com"]
    start_urls = [
        #"https://boardgamegeek.com/boardgame/27833/steam"
        "https://boardgamegeek.com/browse/boardgame"
    ]

    def parse(self, response):
        hxs = scrapy.Selector(response)
        next_page = hxs.xpath("//p[@align='right']/a[@title='next page']")

        if next_page:
            link = next_page.xpath("@href").extract()
            print link
            url = response.urljoin(link[0])
            yield scrapy.Request(url, callback=self.parse)

        titles = hxs.xpath("//div[@style='z-index:1000;']")
        for titles in titles:
            title = titles.xpath("a/text()").extract()
            link = titles.xpath("a/@href").extract()
            url = response.urljoin(link[0])
            print title, url
            yield scrapy.Request(url, callback=self.parse_game_detail_page)


    def parse_game_detail_page(self,response):

        listing = GameListing()

        #Game Name
        listing["name"] = extract_text(response,"h1.geekitem_title > a > span",False)

        # Year Published
        listing["year_published"] = extract_text(response,"div#edit_yearpublished > div:nth-child(2)",False)

        # Number of Players
        listing["mfg_suggested_players"] = extract_text(response,"div#edit_players > div:nth-child(2)",False)

        # User Suggested # of Players
        listing["user_suggested_players"] = extract_text(response,"table.geekitem_infotable > tr:nth-child(6) > td:nth-child(2) > div",False)

        # Mfg Suggested Ages
        listing["mfg_suggested_ages"] = extract_text(response,"div#edit_minage > div:nth-child(2)",False)

        # Playing Time
        listing["playing_time"] = extract_text(response,"div#edit_playtime > div:nth-child(2)",False)

        # User Suggested Ages
        listing["user_suggested_ages"] = extract_text(response,"table.geekitem_infotable > tr:nth-child(9) > td:nth-child(2) > div",False)

        # Language Dependence
        listing["languages"] = extract_text(response,"table.geekitem_infotable > tr:nth-child(10) > td:nth-child(2) > div",False)

        # Honors
        listing["honors"] = extract_text(response,"table.geekitem_infotable > tr:nth-child(11) > td:nth-child(2) > div",True)

        # Sub-domain
        listing["subdomains"] = extract_text(response,"table.geekitem_infotable > tr:nth-child(12) > td:nth-child(2) > div",True)

        # Category
        listing["categories"] = extract_text(response,"table.geekitem_infotable > tr:nth-child(13) > td:nth-child(2) > div",True)

        # Mechanic
        listing["mechanics"] = extract_text(response,"table.geekitem_infotable > tr:nth-child(14) > td:nth-child(2) > div",True)

        # Expansions
        listing["expansions"] = extract_text(response,"table.geekitem_infotable > tr:nth-child(15) > td:nth-child(2) > div",True)

        # Statistics
        # ==========
        # Board Game Rank
        listing["rank"] = extract_text(response,"table.innermoduletable > tr > td:nth-child(1) > table > tr:nth-child(1) > td:nth-child(2) > a",False)

        # Num Ratings:
        listing["count_ratings"] = extract_text(response,"table.innermoduletable > tr > td:nth-child(1) > table > tr:nth-child(3) > td:nth-child(2) > a",False)

        # Average Rating:
        listing["avg_ratings"] = extract_text(response,"table.innermoduletable > tr > td:nth-child(1) > table > tr:nth-child(4) > td:nth-child(2)",False)

        # Standard Deviation:
        listing["std_deviation"] = extract_text(response,"table.innermoduletable > tr > td:nth-child(1) > table > tr:nth-child(5) > td:nth-child(2)",False)

        # Num Views:
        listing["count_views"] = extract_text(response,"table.innermoduletable > tr > td:nth-child(1) > table > tr:nth-child(6) > td:nth-child(2)",False)


        yield listing
