# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ContractorItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    address = scrapy.Field()
    zipCode = scrapy.Field()
    jobCostMin = scrapy.Field()
    jobCostMax = scrapy.Field()
    contactName = scrapy.Field()
    contactPhone = scrapy.Field()
    website = scrapy.Field()

    licenseNumber = scrapy.Field()

    averageRating = scrapy.Field()
    profileUrl = scrapy.Field()
    followers = scrapy.Field()
    following = scrapy.Field()
    badgeCount = scrapy.Field()
    projectCount = scrapy.Field()
    reviewCount = scrapy.Field()
    commentCount = scrapy.Field()
    pass

class GameListing(scrapy.Item):
    name = scrapy.Field()
    year_published = scrapy.Field()
    mfg_suggested_players = scrapy.Field()
    user_suggested_players = scrapy.Field()
    mfg_suggested_ages = scrapy.Field()
    playing_time = scrapy.Field()
    user_suggested_ages = scrapy.Field()
    languages = scrapy.Field()
    honors = scrapy.Field()
    subdomains = scrapy.Field()
    categories = scrapy.Field()
    mechanics = scrapy.Field()
    expansions = scrapy.Field()
    rank = scrapy.Field()
    count_ratings = scrapy.Field()
    avg_ratings = scrapy.Field()
    std_deviation = scrapy.Field()
    count_views = scrapy.Field()
    pass
