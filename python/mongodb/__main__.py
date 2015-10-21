import pymongo
from pymongo import MongoClient
import re
import operator
import csv

client = MongoClient('mongodb://127.0.0.1:3001')
db = client['meteor']

#via a simple regex:
def parseInt(sin):
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


def averageSuggestedPlayers():
    captureTotal = 0.0
    total = 0.0
    for listing in db.listings.find():
        tempString = listing[u'user_suggested_players']
        m = re.search(r'Best with (\d)\D*(\d)*', str(tempString))
        if m:
			if m.group(2):
				#print m.group(1) + ", " + m.group(2)
				total += (float(m.group(1)) + float(m.group(2))) / 2.0
				#print "average: " + str((float(m.group(1)) + float(m.group(2))) / 2.0)
				captureTotal += 1.0
			else:
				#print m.group(1)
				total += float(m.group(1))
				captureTotal += 1.0
    return total / captureTotal

def bestAverageSuggestedPlayers(minimumRating):
    captureTotal = 0
    total = 0
    for listing in db.listings.find():
        entry = listing[u'avg_ratings']
        try:
            if float(listing[u'avg_ratings']) >= minimumRating:
                #print "avg_rating: " + listing[u"avg_ratings"]
                tempString = listing[u'user_suggested_players']
                m = re.search(r'Best with (\d)\D*(\d)*', str(tempString))
                if m:
                    if m.group(2):
                        #print m.group(1) + ", " + m.group(2)
                        total += (float(m.group(1)) + float(m.group(2))) / 2.0
                        #print "average: " + str((float(m.group(1)) + float(m.group(2))) / 2.0)
                        captureTotal += 1.0
                    else:
                        #print m.group(1)
                        total += float(m.group(1))
                        captureTotal += 1.0
        except Exception:
			pass #print "listing had an empty 'avg_ratings' field"
	
    return total / captureTotal
    
def numGamesRating(minimumRating):
    total = 0
    for listing in db.listings.find():
        entry = listing[u'avg_ratings']
        try:
            if float(listing[u'avg_ratings']) >= minimumRating:
                total += 1
        except Exception:
            pass #print "listing had an empty 'avg_ratings' field"
    return total
    
def numberGameMechanics(minimumRating):
    print "Assessing games mechanics with a min rating of: " + str(minimumRating)
    minimumGameHasMechanic = 50
    newMechanicsDict = {}
    mechanicsDict = {}
    sortedMechanicList = []
    for listing in db.listings.find():
        entry = listing[u'mechanics']
        try:
            if float(listing[u'avg_ratings']) >= minimumRating:
               listMechanics = entry.split(", ")
               for mech in listMechanics:
				   #print mech
				   if mech not in mechanicsDict:
					   mechanicsDict[mech] = 1
				   else:
					   mechanicsDict[mech] += 1
        except Exception:
            pass
            #print "listing had an empty 'avg_ratings' field"
    print "Printing all mechanics that more than " + str(minimumGameHasMechanic) + " games have"
    for key in mechanicsDict:
        if int(mechanicsDict[key]) > minimumGameHasMechanic:
			newMechanicsDict[key] = mechanicsDict[key]
    sortedMechanicList = sorted(newMechanicsDict.items(), key=operator.itemgetter(1), reverse = True)
    for item in sortedMechanicList:
		if item[0]:
		    print str(item[1]) + " games have the mechanic of: " + str(item[0])

def numberGameCategories(minimumRating):
    print "Assessing only games categories with a min rating of: " + str(minimumRating)
    minimumGamesContain = 50
    categoriesDict = {}
    newCategoriesDict = {}
    for listing in db.listings.find():
        entry = listing[u'categories']
        try:
            if float(listing[u'avg_ratings']) >= minimumRating:
               listCategories = entry.split(", ")
               for cat in listCategories:
				   #print cat
				   if cat not in categoriesDict:
					   categoriesDict[cat] = 1
				   else:
					   categoriesDict[cat] += 1
        except Exception:
            pass
            #print "listing had an empty 'avg_ratings' field"
    print "Printing all categories that more than " + str(minimumGamesContain) + " games have"
    for key in categoriesDict:
        #print str(categoriesDict[key]) + " games are in the category: " + str(key) 
        if int(categoriesDict[key]) > minimumGamesContain:
		    newCategoriesDict[key] = categoriesDict[key]
    sortedCategoriesList = sorted(newCategoriesDict.items(), key=operator.itemgetter(1), reverse =True)
    for item in sortedCategoriesList:
		if item[0]:
			print str(item[1]) + " games are in the category of: " + str(item[0])

def numberGameExpansions(minimumRating):
    print "Assessing only games expansions with a min rating of: " + str(minimumRating)
    minimumGamesContain = 50
    totalExpansions = 0
    totalGames = 0
    for listing in db.listings.find():
        entry = listing[u'expansions']
        #print "new listing: " + str(listing[u'name'])
        if entry:    
            try:
                if float(listing[u'avg_ratings']) >= minimumRating:
                    totalGames+=1
                    gameExpansions = entry.split(", ")
                    totalExpansions += len(gameExpansions)
            except Exception:
                pass
    print str(totalExpansions) + " total expansions"
    print "average expansion per game: " + str(float(totalExpansions) / float(totalGames))
    return totalGames
            #print "listing had an empty 'avg_ratings' field"
    #return totalExpansions / totalGames


def writeToCSV():
	rank_limit = 9001

	myquery = db.listings.find({'rank':{'$lt':rank_limit}}).sort([
			('rank', pymongo.ASCENDING)]) # I am getting everything !

	#cleanRank()

	output = csv.writer(open('top-'+str(rank_limit)+'.csv', 'wt')) # writng in this file

	column_headers = [u'name',u'rank',u'year_published',u'mechanics',u'categories',u'subdomains',
	u'playing_time',u'mfg_suggested_ages',u'user_suggested_ages',u'expansions',u'languages',u'honors',
	u'mfg_suggested_players',u'user_suggested_players',u'count_ratings',u'avg_ratings',u'std_deviation',u'count_views',
	]

	output.writerow(column_headers)
	print "writing row"

	for listing in myquery:
		tt = list()

		for k in column_headers:
			tt.append(listing[k])

		# for k,v in listing.items():
		#     tt.append(v) #encoding
		#     # tt.append(v.encode('ascii', 'ignore')) #encoding


		output.writerow(tt)


print str(numGamesRating(7.0)) + " games are rated " + str(7.0) + " or above out of 80032 total games"
print "\n\n"
print "average board game is best with: " + str(averageSuggestedPlayers()) + " players"
print "\n\n"
print "for board games that are rated 7.5 or above, average suggested players is: " + str(bestAverageSuggestedPlayers(7.5)) + " players"
print "\n\n"
numberGameMechanics(7.0)
print "\n\n"
numberGameCategories(7.0)
print "\n\n"
print str(numberGameExpansions(7.0)) + " games have expansions"
print "\n\n"


