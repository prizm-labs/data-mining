import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://127.0.0.1:3334')
db = client['meteor']

#via a simple regex:
def parseInt(sin):
  import re
  m = re.search(r'^(\d+)[.,]?\d*?', str(sin))
  return int(m.groups()[-1]) if m and not callable(sin) else None

def cleanRank():
    for listing in db.listings.find():
        if parseInt(listing[u'rank'])!=None:
            rank = int(listing[u'rank'])
            print listing[u'name']
            print listing[u'_id']
            print rank

            result = db.listings.update_one({'_id': listing[u'_id']}, {'$set': {'rank': rank}})
            print result.matched_count
            print result.modified_count

import csv

rank_limit = 5000

myquery = db.listings.find({'rank':{'$lt':rank_limit}}).sort([
        ('rank', pymongo.ASCENDING)]) # I am getting everything !
output = csv.writer(open('top-'+str(rank_limit)+'.csv', 'wt')) # writng in this file

column_headers = [u'name',u'rank',u'year_published',u'mechanics',u'categories',u'subdomains',
u'playing_time',u'mfg_suggested_ages',u'user_suggested_ages',u'expansions',u'languages',u'honors',
u'mfg_suggested_players',u'user_suggested_players',u'count_ratings',u'avg_ratings',u'std_deviation',u'count_views',
]

output.writerow(column_headers)

for listing in myquery:
    tt = list()

    for k in column_headers:
        tt.append(listing[k])

    # for k,v in listing.items():
    #     tt.append(v) #encoding
    #     # tt.append(v.encode('ascii', 'ignore')) #encoding


    output.writerow(tt)
