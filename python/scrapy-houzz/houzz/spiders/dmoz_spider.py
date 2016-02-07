import scrapy
from houzz.items import ContractorItem

import csv
import sys
import re

def extract_text(response,css_selector,extract_with_links):
    xpath = response.css(css_selector)

    if (len(xpath) == 0):
        return False;

    if extract_with_links:
        return extract_wrapped_links(xpath)
    else:
        return clean_text(xpath.xpath("text()").extract())

# def extract_link(response,css_selector):
#     xpath = response.css(css_selector)
#
#     if extract_with_links:
#         return extract_wrapped_links(xpath)
#     else:
#         return clean_text(xpath.xpath("text()").extract())

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
    name = "houzz"
    allowed_domains = ["www.houzz.com"]
    start_urls = [
        #"https://boardgamegeek.com/boardgame/27833/steam"
        "http://www.houzz.com/professionals/general-contractor/los-angeles"
    ]

    statistics_access_index = 0
    child = 2

    # entry point for all scraping
    def parse(self, response):
        hxs = scrapy.Selector(response)
        next_page = hxs.css("ul#paginationBar > li:last-child > a")

        if next_page:
            link = next_page.xpath("@href").extract()
            print "found next page to crawl",link
            url = link[0].encode('ascii','ignore')
            yield scrapy.Request(url, callback=self.parse)

        titles = hxs.xpath("//div[@class='name-info']")
        print "detail pages found:",len(titles)

        for titles in titles:
            title = titles.xpath("a/text()").extract()
            link = titles.xpath("a/@href").extract()
            url = link[0].encode('ascii','ignore')

            # check URL targeted
            print "page title",title, "page URL",url

            # if ( len(re.search( r'(javascript)', url, re.M|re.I).group())!=0 ):
            #     print "found url for profile page"
            # else:
            #     print "invalid page url"

            # yield scrapy.Request(url, callback=self.parse_contractor_detail_page)

        # HAS "Typical Job Costs"
        # url = "http://www.houzz.com/pro/socalcontractor/socal-contractor"

        # HAS "License Number"
        # url = "http://www.houzz.com/pro/tnoroian/tnt-simmon"

        # HAS NO ADDITONAL INFO
        # url = "http://www.houzz.com/pro/chelseaconstruction/chelsea-construction-corporation"
        # yield scrapy.Request(url, callback=self.parse_contractor_detail_page)


    def parse_contractor_detail_page(self,response):
    # ex. http://www.houzz.com/pro/socalcontractor/socal-contractor

        print 'entered detail page',response.url

        listing = ContractorItem()

        #Game Name
        #listing["name"] = extract_text(response,"h1.geekitem_title > a > span",False)

        # response.css("").xpath("text()").extract()
        # test in: scrapy shell "PAGE_URL"
        # CSS_SELECTOR = "div.info-list-text:nth-child(2)"
        # response.css(CSS_SELECTOR).xpath("text()").extract()

        # name = scrapy.Field()
        # response.css("a.profile-full-name").xpath("text()").extract()
        name = extract_text(response,"a.profile-full-name",False)
        listing["name"] = name

        # profileUrl = scrapy.Field()
        # response.css("a.profile-full-name").xpath("@href").extract()[0].encode('ascii','ignore')
        profileUrl = response.css("a.profile-full-name").xpath("@href").extract()[0].encode('ascii','ignore')
        listing["profileUrl"] = profileUrl

        # website = scrapy.Field()
        # response.css("a.profile-full-name").xpath("@href").extract()[0].encode('ascii','ignore')
        # website = response.css("div.pro-contact-methods.one-line > a").xpath("@href").extract()[0].encode('ascii','ignore')
        # compid="Profile_Website"
        website = response.css("a[compid='Profile_Website']").xpath("@href").extract()[0].encode('ascii','ignore')
        listing["website"] = website

        # address = scrapy.Field()
        # response.css("div.info-list-label:nth-child(3) > div.info-list-text > span[itemprop='streetAddress']").xpath("text()").extract()
        address = extract_text(response,"div.info-list-label:nth-child(3) > div.info-list-text > span[itemprop='streetAddress']",False)
        listing["address"] = address

        # zipCode = scrapy.Field()
        # response.css("div.info-list-label:nth-child(3) > div.info-list-text > span[itemprop='postalCode']").xpath("text()").extract()
        zipCode = extract_text(response,"div.info-list-label:nth-child(3) > div.info-list-text > span[itemprop='postalCode']",False)
        listing["zipCode"] = zipCode


        # contactName = scrapy.Field()
        contactName = extract_text(response,"div.info-list-label:nth-child(2) > div.info-list-text",False)
        # ex. ': Roy Yerushalmi'
        contactName = contactName.replace(": ","");
        listing["contactName"] = contactName

        # contactPhone = scrapy.Field()
        # response.css("div.pro-contact-methods.one-line > span.pro-contact-text").xpath("text()").extract()
        contactPhone = extract_text(response,"div.pro-contact-methods.one-line > span.pro-contact-text",False)
        listing["contactPhone"] = contactPhone


        # averageRating = scrapy.Field()
        # <meta itemprop="ratingValue" content="4.9">
        # float(response.css("meta[itemprop='ratingValue']").xpath("@content").extract()[0].encode('ascii','ignore'))
        averageRating = response.css("meta[itemprop='ratingValue']").xpath("@content").extract()[0].encode('ascii','ignore')
        listing["averageRating"] = float(averageRating)


        # badgeCount = scrapy.Field()
        # response.css("a.following.follow-box > span.follow-count").xpath("text()").extract()
        badgeCount = extract_text(response,"div.profile-sidebar-section > .header-6.top > a",False)
        badgeCount = re.search( r'(\d+)', badgeCount, re.M|re.I).group(1)
        listing["badgeCount"] = int(badgeCount.replace(",",""))

        # projectCount = scrapy.Field()
        # response.css("div.project-section > .header-6.top > a").xpath("text()").extract()
        projectCount = extract_text(response,"div.project-section > .header-6.top > a",False)
        projectCount = re.search( r'(\d+)', projectCount, re.M|re.I).group(1)
        listing["projectCount"] = int(projectCount.replace(",",""))

        # reviewCount = scrapy.Field()
        # response.css("div.review-section > .header-6.top > a").xpath("text()").extract()
        reviewCount = extract_text(response,"div.review-section > .header-6.top > a",False)
        reviewCount = re.search( r'(\d+)', reviewCount, re.M|re.I).group(1)
        listing["reviewCount"] = int(reviewCount.replace(",",""))

        # commentCount = scrapy.Field()
        # response.css("div.question-section > .header-6.top > a").xpath("text()").extract()
        commentCount = extract_text(response,"div.question-section > .header-6.top > a",False)
        commentCount = re.search( r'(\d+)', commentCount, re.M|re.I).group(1)
        listing["commentCount"] = int(commentCount)


        # OPTIONAL ELEMENTS
        #==================

        # MAY HAVE FOLlWERS

        # followers = scrapy.Field()
        # response.css("a.followers.follow-box > span.follow-count").xpath("text()").extract()
        followers = extract_text(response,"a.followers.follow-box > span.follow-count",False)

        if (followers):
            listing["followers"] = int(followers.replace(",",""))


        # MAY HAVE FOLLOWING

        # following = scrapy.Field()
        # response.css("a.following.follow-box > span.follow-count").xpath("text()").extract()
        following = extract_text(response,"a.following.follow-box > span.follow-count",False)

        if (following):
            listing["following"] = int(following.replace(",",""))

        # MAY HAVE "License Number" at 4th element in right sidebar
        # EX. http://www.houzz.com/pro/tnoroian/tnt-simmonds
        # OR
        # MAY HAVE "Typical Job Cost" at 4th element in right sidebar
        # EX. http://www.houzz.com/pro/socalcontractor/socal-contractor

        # OR NO ADDITIONAL INFO
        # EX. http://www.houzz.com/pro/chelseaconstruction/chelsea-construction-corporation

        # CHECK TYPE OF THIS ELEMENT
        # response.css("div.info-list-label:nth-child(4) > div.info-list-text > b").xpath("text()").extract()

        info_element = response.css("div.info-list-label:nth-child(4) > div.info-list-text").xpath("text()").extract()

        if ( len(info_element) > 0):

            element_type = response.css("div.info-list-label:nth-child(4) > div.info-list-text > b").xpath("text()").extract()[0].encode('ascii','ignore')
            itemStr = extract_text(response,"div.info-list-label:nth-child(4) > div.info-list-text",False)

            print "HAS ADDITIONAL INFO", element_type, itemStr

            if (element_type == "Typical Job Costs"):
                # ex. ':   $50000 - 15,000,000'
                jobCostStr = itemStr

                jobCostNumbers = re.search( r'\$(.*) \- (.*)', jobCostStr, re.M|re.I)

                # jobCostMin = scrapy.Field()
                # response.css("div.info-list-label:nth-child(4) > div.info-list-text").xpath("text()").extract()
                jobCostMin = jobCostNumbers.group(1).replace(",","");
                listing["jobCostMin"] = int(jobCostMin)

                # jobCostMax = scrapy.Field()
                jobCostMax = jobCostNumbers.group(2).replace(",","");
                listing["jobCostMax"] = int(jobCostMax)


            if (element_type == "License Number"):

                licenseNumber = itemStr.replace(": ","");
                listing["licenseNumber"] = licenseNumber


        print "extracted listing:",listing

        yield listing



    def general_parse_helper(self, response, regex_key, extract_text_bool):
        for i in range(20):
            entry_name = extract_text(response,"table.geekitem_infotable > tr:nth-child(%d) > td:nth-child(1) > b" % i,False)
            #print "Entry name is: " + entry_name + " from n-th child: " + str(i)
            try:
                if (re.search(r'.*(%s)' % regex_key, entry_name).group(1)):  #if we hit the right entry
                    return extract_text(response,"table.geekitem_infotable > tr:nth-child(%d) > td:nth-child(2) > div" % i,extract_text_bool)
            except:
                pass



    def statistics_parse_helper(self, response):
        #the table row that we are accessing is called self.child
        base_string = "table.innermoduletable > tr > td:nth-child(1) > table > tr:nth-child(%d) > td:nth-child(2)" % self.child
        #print "child: " + str(self.child)
        #find out what section we are looking at (i.e. Num Ratings, Family Game Rank, Standard Dev, etc)
        category_name = extract_text(response, "table.innermoduletable > tr > td:nth-child(1) > table > tr:nth-child(%d) > td:nth-child(1) > b" % self.child, False)
	#print "category_name: " + category_name

        try:
            if (re.search(r'.*(Rank:)', category_name).group(1)):  #if we we on something that is a rank, we don't want it, recurse for the next one
                self.child += 1
                #print "Rank caught, child: " + str(self.child) + extract_text(response,base_string,False)
                return self.statistics_parse_helper(response)
        except:
            pass
        try:
            if (re.search(r'.*(Ratings:)', category_name).group(1)):    #if we caught Num Ratings, append hyperlink tag
                self.child += 1
                #print "Num ratings caught, child: " + str(self.child) + extract_text(response,base_string + " > a",False)
                return (base_string + " > a")
        except:
            pass
        try:
            if (re.search(r'.*(Views:)', category_name).group(1)):    #if we are on Num Views, reset child count (all we need)
                self.child = 1
                #print "num views caught, child: " + str(self.child) + extract_text(response,base_string,False)
                return base_string
        except:
            pass
        try:  #if we are on any other statistic, prepare for the next one and return default string
            self.child += 1
            #print "none caught, child: " + str(self.child) + extract_text(response,base_string,False)
            return base_string
        except:
            print "catastrophic failure!!!"
