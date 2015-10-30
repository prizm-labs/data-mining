import pymongo
from pymongo import MongoClient
import re
import operator
import csv

client = MongoClient('mongodb://127.0.0.1:3005')
db = client['meteor']

#via a simple regex:
def parseInt(sin):
  m = re.search(r'^(\d+)[.,]?\d*?', str(sin))
  return int(m.groups()[-1]) if m and not callable(sin) else None

def cleanRank():
    for listing in db.updatedListings.find():
        if parseInt(listing[u'rank'])!=None:
            rank = int(listing[u'rank'])
            #print listing[u'name']
            #print listing[u'_id']
            #print rank

            result = db.updatedListings.update_one({'_id': listing[u'_id']}, {'$set': {'rank': rank}})
            #print result.matched_count
            #print result.modified_count


def averageSuggestedPlayers():
    captureTotal = 0.0
    total = 0.0
    for listing in db.updatedListings.find():
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
    for listing in db.updatedListings.find():
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
    for listing in db.updatedListings.find():
        entry = listing[u'avg_ratings']
        try:
            if float(listing[u'avg_ratings']) >= minimumRating:
                total += 1
        except Exception:
            pass #print "listing had an empty 'avg_ratings' field"
    return total
    
    
#returns number of games associated with a certain mechanic
def numberGameMechanics(minimumRating, maximumRating, minPopularity):
    print "Assessing games mechanics with a min rating of: " + str(minimumRating) + " and a max rating of: " + str(maximumRating) + ", and a minimum popularity of: " + str(minPopularity) + " votes"
    minimumGameHasMechanic = 10
    newMechanicsDict = {}
    mechanicsDict = {}
    sortedMechanicList = []
    for listing in db.updatedListings.find():
        entry = listing[u'mechanics']
        try:
            if float(listing[u'avg_ratings']) >= minimumRating and float(listing[u'avg_ratings']) <= maximumRating and int(listing[u'count_ratings']) > minPopularity:
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
		    print str(item[1]) + ", " + str(item[0])
        
#returns number of games associated with an amount of mechanics
def numberQuantityGameMechanics(minimumRating, maximumRating, minPopularity):
    print "Assessing games quantity of mechanics with a min rating of: " + str(minimumRating) + " and a max rating of: " + str(maximumRating) + ", and a minimum popularity of: " + str(minPopularity) + " votes"
    minimumGameHasMechanic = 10
    newMechanicsDict = {}
    mechanicsDict = {}
    sortedMechanicList = []
    for listing in db.updatedListings.find():
        entry = listing[u'mechanics']
        try:
            if float(listing[u'avg_ratings']) >= minimumRating and float(listing[u'avg_ratings']) <= maximumRating and int(listing[u'count_ratings']) > minPopularity:
               listMechanics = entry.split(", ")
               quantityMech = len(listMechanics)
               if quantityMech not in mechanicsDict:
                   mechanicsDict[quantityMech] = 1
               else:
                   mechanicsDict[quantityMech] += 1
        except Exception:
            pass
            #print "listing had an empty 'avg_ratings' field"
    print "Printing all quantities of mechanics that more than " + str(minimumGameHasMechanic) + " games have"
    for key in mechanicsDict:
        if int(mechanicsDict[key]) > minimumGameHasMechanic:
			newMechanicsDict[key] = mechanicsDict[key]
    sortedMechanicList = sorted(newMechanicsDict.items(), key=operator.itemgetter(1), reverse = True)
    for item in sortedMechanicList:
		if item[0]:
		    print str(item[1]) + " games have the the quantity of mechanics of: " + str(item[0])

#returns number of games associated with a certain subdomain
def numberGameSubdomains(minimumRating, maximumRating, minPopularity):
    print "Assessing games subdomains with a min rating of: " + str(minimumRating) + " and a max rating of: " + str(maximumRating) + ", and a minimum popularity of: " + str(minPopularity) + " votes"
    minimumGameInSubdomain = 10
    newSubdomainsDict = {}
    subdomainsDict = {}
    sortedSubdomainList = []
    for listing in db.updatedListings.find():
        entry = listing[u'subdomains']
        try:
            if float(listing[u'avg_ratings']) >= minimumRating and float(listing[u'avg_ratings']) <= maximumRating and int(listing[u'count_ratings']) > minPopularity:
               listSubdomains = entry.split(", ")
               for sub in listSubdomains:
				   #print mech
				   if sub not in subdomainsDict:
					   subdomainsDict[sub] = 1
				   else:
					   subdomainsDict[sub] += 1
        except Exception as e:
            print e
            pass
            #print "listing had an empty 'avg_ratings' field"
    print "Printing all subdomains that more than " + str(minimumGameInSubdomain) + " games are in"
    for key in subdomainsDict:
        if int(subdomainsDict[key]) > minimumGameInSubdomain:
			newSubdomainsDict[key] = subdomainsDict[key]
    sortedSubdomainList = sorted(newSubdomainsDict.items(), key=operator.itemgetter(1), reverse = True)
    for item in sortedSubdomainList:
		if item[0]:
		    print str(item[1]) + ", " + str(item[0])
            
            
#returns number of games associated with a certain mechanic
def numberGameMechanicsAndCategory(minimumRating, maximumRating, minPopularity):
    print "Assessing games mechanics/categories with a min rating of: " + str(minimumRating) + " and a max rating of: " + str(maximumRating) + ", and a minimum popularity of: " + str(minPopularity) + " votes"
    minimumGameHasMechanic = 10
    newMechanicsDict = {}
    mechanicsDict = {}
    sortedMechanicList = []
    for listing in db.updatedListings.find():
        entry = listing[u'mechanics'] + ", " + listing[u'categories']
        try:
            if float(listing[u'avg_ratings']) >= minimumRating and float(listing[u'avg_ratings']) <= maximumRating and int(listing[u'count_ratings']) > minPopularity:
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
    print "Printing all mechanics/categories that more than " + str(minimumGameHasMechanic) + " games have"
    for key in mechanicsDict:
        if int(mechanicsDict[key]) > minimumGameHasMechanic:
			newMechanicsDict[key] = mechanicsDict[key]
    sortedMechanicList = sorted(newMechanicsDict.items(), key=operator.itemgetter(1), reverse = True)
    for item in sortedMechanicList:
		if item[0]:
		    print str(item[1]) + ", " + str(item[0])
            

#returns number of games associated with a certain complexity
def numberGameComplexity(minimumRating, maximumRating, minPopularity):
    print "Assessing games complexity with a min rating of: " + str(minimumRating) + " and a max rating of: " + str(maximumRating) + ", and a minimum popularity of: " + str(minPopularity) + " votes"
    languagesDict = {}
    
    languagesDict["N"] = 0  #No necessary in-game text
    languagesDict["S"] = 0  #Some necessary text
    languagesDict["M"] = 0  #Moderate use of text
    languagesDict["E"] = 0  #Extensive use of text
    languagesDict["U"] = 0  #Unplayable
    
    
    for listing in db.updatedListings.find():
        entry = listing[u'languages']
        try:
            if float(listing[u'avg_ratings']) >= minimumRating and float(listing[u'avg_ratings']) <= maximumRating and int(listing[u'count_ratings']) > minPopularity:
                ex = re.search(r'(\w).*', str(entry))
                if ex.group(1) == "N":
                   languagesDict["N"] += 1
                if ex.group(1) == "S":
                   languagesDict["S"] += 1
                if ex.group(1) == "M":
                   languagesDict["M"] += 1
                if ex.group(1) == "E":
                   languagesDict["E"] += 1
                if ex.group(1) == "U":
                   languagesDict["U"] += 1
        except Exception:
            pass
            #print "listing had an empty 'avg_ratings' field"
    for key in languagesDict:
        if key == "N":
            print "number of simple games, " + str(languagesDict[key])
        elif key == "S":
            print "number of slightly complex games, " + str(languagesDict[key])
        elif key == "M":
            print "number of moderately complex games, " + str(languagesDict[key])
        elif key == "E":
            print "number of extensively complex games, " + str(languagesDict[key])
        elif key == "U":
            print "number of unplayably complex games, " + str(languagesDict[key])
        else:
            print "should not reach here"

#returns gross popularity of game mechanics
def popularityGameMechanics(minimumRating, maximumRating):
    print "Assessing games mechanics with a min rating of: " + str(minimumRating) + " and a max rating of: " + str(maximumRating)
    minimumPopularity = 1000
    clampedMechanicsDict = {}
    mechanicsDict = {}
    sortedMechanicList = []
    for listing in db.updatedListings.find():
        entry = listing[u'mechanics']
        try:
            if float(listing[u'avg_ratings']) >= minimumRating and float(listing[u'avg_ratings']) <= maximumRating:
               listMechanics = entry.split(", ")
               for mech in listMechanics:
				   #print mech
				   if mech not in mechanicsDict:
					   mechanicsDict[mech] = int(listing[u'count_ratings'])
				   else:
					   mechanicsDict[mech] += int(listing[u'count_ratings'])
        except Exception:
            pass
            #print "listing had an empty 'avg_ratings' field"
    print "Printing popularity of game mechanics: (only mechanics with 1000+) are counted"
    for key in mechanicsDict:
        if int(mechanicsDict[key]) > minimumPopularity:
			clampedMechanicsDict[key] = mechanicsDict[key]
    sortedMechanicList = sorted(clampedMechanicsDict.items(), key=operator.itemgetter(1), reverse = True)   #sorts dictionary by popularity
    for item in sortedMechanicList:
		if item[0]: #if dictionary key exists
		    print str(item[0]) + ", " + str(item[1])
           
            
#returns gross popularity of game mechanics
def popularityGameSubdomains(minimumRating, maximumRating):
    print "Assessing games subdomains with a min rating of: " + str(minimumRating) + " and a max rating of: " + str(maximumRating)
    minimumPopularity = 1000
    clampedSubdomainDict = {}
    subdomainsDict = {}
    sortedSubdomainList = []
    for listing in db.updatedListings.find():
        entry = listing[u'subdomains']
        try:
            if float(listing[u'avg_ratings']) >= minimumRating and float(listing[u'avg_ratings']) <= maximumRating:
               listSubdomains = entry.split(", ")
               for sub in listSubdomains:
				   #print mech
				   if sub not in subdomainsDict:
					   subdomainsDict[sub] = int(listing[u'count_ratings'])
				   else:
					   subdomainsDict[sub] += int(listing[u'count_ratings'])
        except Exception as e:
            pass
            #print "listing had an empty 'avg_ratings' field"
    print "Printing popularity of game subdomains: (only subdomains with 1000+) are counted"
    for key in subdomainsDict:
        if int(subdomainsDict[key]) > minimumPopularity:
			clampedSubdomainDict[key] = subdomainsDict[key]
    sortedSubdomainList = sorted(clampedSubdomainDict.items(), key=operator.itemgetter(1), reverse = True)   #sorts dictionary by popularity
    for item in sortedSubdomainList:
		if item[0]: #if dictionary key exists
		    print str(item[0]) + ", " + str(item[1])


#returns gross popularity of game mechanics and game categories combined
def popularityGameMechanicsAndCategory(minimumRating, maximumRating, minimumPopularity):
    print "Assessing games mechanics/categories with a min rating of: " + str(minimumRating) + " and a max rating of: " + str(maximumRating) + "and a minimum popularity of: " + str(minimumPopularity)
    clampedMechanicsDict = {}
    mechanicsDict = {}
    sortedMechanicList = []
    for listing in db.updatedListings.find():
        entry = listing[u'mechanics'] + ", " + listing[u'categories']
        try:
            if float(listing[u'avg_ratings']) >= minimumRating and float(listing[u'avg_ratings']) <= maximumRating:
               listMechanics = entry.split(", ")
               for mech in listMechanics:
				   #print mech
				   if mech not in mechanicsDict:
					   mechanicsDict[mech] = int(listing[u'count_ratings'])
				   else:
					   mechanicsDict[mech] += int(listing[u'count_ratings'])
        except Exception:
            pass
            #print "listing had an empty 'avg_ratings' field"
    print "Printing popularity of game mechanics/categories: "
    for key in mechanicsDict:
        if int(mechanicsDict[key]) > minimumPopularity:
			clampedMechanicsDict[key] = mechanicsDict[key]
    sortedMechanicList = sorted(clampedMechanicsDict.items(), key=operator.itemgetter(1), reverse = True)   #sorts dictionary by popularity
    for item in sortedMechanicList:
		if item[0]: #if dictionary key exists
		    print str(item[0]) + ", " + str(item[1])
            
            
#returns gross popularity of game category
def popularityGameCategory(minimumRating, maximumRating):
    print "Assessing games categories with a min rating of: " + str(minimumRating) + " and a max rating of: " + str(maximumRating)
    minimumPopularity = 1000
    clampedCategoriesDict = {}
    categoriesDict = {}
    sortedCategoryList = []
    for listing in db.updatedListings.find():
        entry = listing[u'categories']
        try:
            if float(listing[u'avg_ratings']) >= minimumRating and float(listing[u'avg_ratings']) <= maximumRating:
               listCategories = entry.split(", ")
               for cat in listCategories:
				   #print cat
				   if cat not in categoriesDict:
					   categoriesDict[cat] = int(listing[u'count_ratings'])
				   else:
					   categoriesDict[cat] += int(listing[u'count_ratings'])
        except Exception:
            pass
            #print "listing had an empty 'avg_ratings' field"
    print "Printing popularity of game categories: (only categories with 1000+) are counted"
    for key in categoriesDict:
        if int(categoriesDict[key]) > minimumPopularity:
			clampedCategoriesDict[key] = categoriesDict[key]
    sortedCategoryList = sorted(clampedCategoriesDict.items(), key=operator.itemgetter(1), reverse = True)   #sorts dictionary by popularity
    for item in sortedCategoryList:
		if item[0]: #if dictionary key exists
		    print str(item[0]) + ", " + str(item[1])
            


#returns gross popularity of game's playing time
def popularityPlayingTime(minimumRating, maximumRating, minimumPopularity):
    print "Assessing games playing times with a min rating of: " + str(minimumRating) + " and a max rating of: " + str(maximumRating) + " and a min popularity of: " + str(minimumPopularity)
    avgPlaytimeList = []
    sortedPlaytimeList = []
    games_counted = 0
    games_tried = 0
    for listing in db.updatedListings.find():
        entry = listing[u'categories']
        try:
            games_tried +=1
            if float(listing[u'avg_ratings']) >= minimumRating and float(listing[u'avg_ratings']) <= maximumRating and int(listing[u'count_ratings']) >= minimumPopularity:
                #need to further parse game playing time
                ex = re.search(r'([123456789]+0?)(\d*).*', str(listing[u'playing_time']))
                #calculate average
                #throw out if average is too high
                try:
                    #print "found regex: " + str(ex.group(0))
                    first_time = ex.group(1)
                    
                    try:
                        #print "second number: " + str(ex.group(2))
                        second_time = ex.group(2)
                    except Exception:
                        #print "no second playtime to average"
                        pass
                        
                except Exception:
                    pass
                    
                #print "first num:"+first_time + ",secondnum:"+second_time
                try:
                    #print "average: " + str((float(first_time) + float(second_time)) / 2.0)
                    average_playtime = (float(first_time) + float(second_time)) / 2.0
                except Exception as e:
                    #print "average: " + str(first_time)
                    average_playtime = float(first_time)
                    #print e
                    #print "don't worry, thing is set"
                
                if average_playtime < 250.0:    #only count the data if it's not an outlier
                    avgPlaytimeList.append(average_playtime)
                    games_counted += 1
                else:
                    print "average playtime out of bounds! time is: " + average_playtime
        except Exception as e:
            #print e
            #print "main exception handled, item not added to list"
            pass
            #print "listing had an empty 'avg_ratings' field"
    print "Printing average playtimes of popular games:"
    sortedPlaytimeList = sorted(avgPlaytimeList)   #sorts dictionary by popularity
    total_time_played = 0
    for item in sortedPlaytimeList:
        print str(item)
        #total_time_played += item
    print "list length is: " + str(len(sortedPlaytimeList))
            
            
#correlates game's rank and popularity
def popularityVsGameRank(minimumPopularity):
    print "Assessing games ranks with a min popularity of: " + str(minimumPopularity)
    clampedRankDict = {}
    rankDict = {}
    sortedRankList = []
    for listing in db.updatedListings.find():
        gameRank = listing[u'rank']
        try:
           rankDict[int(listing[u'count_ratings'])] = gameRank
        except Exception:
            pass
            #print "listing had an empty 'count_ratings' field"
    for key in rankDict:
        if int(key) > minimumPopularity:
			clampedRankDict[key] = rankDict[key]
    sortedRankList = sorted(clampedRankDict.items(), key=operator.itemgetter(1), reverse = False)   #sorts dictionary by popularity
    for item in sortedRankList:
		if item[0]: #if dictionary key exists
		    print str(item[1]) + ", " + str(item[0])
            
            
            
def numberGameCategories(minimumRating, maximumRating, minPopularity):
    print "Assessing only games categories with a min rating of: " + str(minimumRating) + " and a max rating of: " + str(maximumRating) + ", and a minimum popularity of: " + str(minPopularity) + " votes"
    minimumGamesContain = 10
    categoriesDict = {}
    newCategoriesDict = {}
    for listing in db.updatedListings.find():
        entry = listing[u'categories']
        try:
            if float(listing[u'avg_ratings']) >= minimumRating and float(listing[u'avg_ratings']) <= maximumRating and int(listing[u'count_ratings']) > minPopularity:
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
			print str(item[1]) + ", " + str(item[0])

def numberGameExpansions(minimumRating):
    print "Assessing only games expansions with a min rating of: " + str(minimumRating)
    minimumGamesContain = 10
    totalExpansions = 0
    totalGames = 0
    for listing in db.updatedListings.find():
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
    rank_limit = 200

    myquery = db.updatedListings.find({'rank':{'$lt':rank_limit}}).sort([('rank', pymongo.ASCENDING)]) # I am getting everything !

    cleanRank()

    output = csv.writer(open('top-'+str(rank_limit)+'.csv', 'wt')) # writng in this file

    column_headers = [u'name',u'rank',u'year_published',u'mechanics',u'categories',u'subdomains',	u'playing_time',u'mfg_suggested_ages',u'user_suggested_ages',u'expansions',u'languages',u'honors',	u'mfg_suggested_players',u'user_suggested_players',u'count_ratings',u'avg_ratings',u'std_deviation',u'count_views',]

    output.writerow(column_headers)
    #print "writing row"

    for listing in myquery:
        tt = list()
        #print "writing another row"

        for k in column_headers:
            temp_row = str(listing[k]).replace(";", ",")
            print temp_row
            tt.append(temp_row)

		# for k,v in listing.items():
		#     tt.append(v) #encoding
		#     # tt.append(v.encode('ascii', 'ignore')) #encoding
	#print "in listing"
        output.writerow(tt)
    print "done writing"
    
def writeALLToCSV():
    myquery = db.updatedListings.find().sort([('rank', pymongo.ASCENDING)]) # I am getting everything !

    cleanRank()

    output = csv.writer(open('ALL_data.csv', 'wt')) # writng in this file

    column_headers = [u'name',u'rank',u'year_published',u'mechanics',u'categories',u'subdomains',	u'playing_time',u'mfg_suggested_ages',u'user_suggested_ages',u'expansions',u'languages',u'honors',	u'mfg_suggested_players',u'user_suggested_players',u'count_ratings',u'avg_ratings',u'std_deviation',u'count_views',]

    output.writerow(column_headers)
    #print "writing row"

    for listing in myquery:
        tt = list()
        #print "writing another row"

        for k in column_headers:
            temp_row = str(listing[k]).replace(";", ",")
            print temp_row
            tt.append(temp_row)

		# for k,v in listing.items():
		#     tt.append(v) #encoding
		#     # tt.append(v.encode('ascii', 'ignore')) #encoding
	#print "in listing"
        output.writerow(tt)
    print "done writing"
#writeToCSV()
writeALLToCSV()


#Completed, Useful Functions:

#POPULARITY VS. MECHANICS
#gross popularity of mechanics
#popularityGameMechanics(0.1, 7.0)   #worst rated
#popularityGameMechanics(7.0, 10.0)  #best rated
#popularityGameMechanics(0.1, 10.0)  #all-inclusive

#how many popular games have certain mechanic
#numberGameMechanics(0.1, 7.0, 1000) #worst rated, at least 1000 poular
#numberGameMechanics(7.0, 10.0, 1000) #best rated, at least 1000 poular
#numberGameMechanics(0.1, 10.0, 1000) #all-inclusive, at least 1000 poular

#NOTE: average popularity per game mechanic is extrapolated by total popularity / number of popular games


#POPULARITY VS. CATEGORY
#gross popularity of categories
#popularityGameCategory(0.1, 7.0)
#popularityGameCategory(7.0, 10.0)
#popularityGameCategory(0.1, 10.0)

#how many popular games are in certain category
#numberGameCategories(0.1, 7.0, 1000) #worst rated, at least 1000 poular
#numberGameCategories(7.0, 10.0, 1000) #best rated, at least 1000 poular
#numberGameCategories(0.1, 10.0, 1000) #all-inclusive, at least 1000 poular

#NOTE: average popularity per game category is extrapolated by total popularity / number of popular games


#POPULARITY VS. RANK
#popularity vs. rank simple scatter plot
#(may want to revisit, may want to clamp to top 1000 ranked games)
#popularityVsGameRank(1000)  #associates game's rank with popularity, at least 1000 votes


#POPULARITY VS. PLAYING TIME
#how many games have a certain playing time
#popularityPlayingTime(0.1, 7.0, 1000) #worst rated, at least 1000 popular
#popularityPlayingTime(7.0, 10.0, 1000) #best rated, at least 1000 popular
#popularityPlayingTime(0.1, 10.0, 1000) #all-inclusive, at least 1000 popular


#POPULARITY VS. COMPLEXITY
#number of popular games in a certain complexity category
#numberGameComplexity(0.1, 7.0, 1000)    #worst rated, at least 1000 popular
#numberGameComplexity(7.0, 10.0, 1000)   #best rated, at least 1000 popular
#numberGameComplexity(0.1, 10.0, 1000)   #all-inclusive, at least 1000 popular


#POPULARITY VS. CAT/MECH
#gross popularity of certain CAT/MECHs
#popularityGameMechanicsAndCategory(0.1, 7.0, 1000)    #worst rated, at least 1000 popular
#popularityGameMechanicsAndCategory(7.0, 10.0, 1000)    #best rated, at least 1000 popular
#popularityGameMechanicsAndCategory(0.1, 10.0, 1000)    #all-inclusive, at least 1000 popular

#number of games with particular Cat/Mech
#numberGameMechanicsAndCategory(0.1, 7.0, 1000) #worst rated, at least 1000 popular
#numberGameMechanicsAndCategory(7.0, 10.0, 1000) #best rated, at least 1000 popular
#numberGameMechanicsAndCategory(0.1, 10.0, 1000) #all-inclusive, at least 1000 popular

#NOTE: average popularity per game Cat/Mech is extrapolated by total popularity / number of popular games


#POPULARITY VS. SUBDOMAINS
#gross popularity of certain subdomains
#popularityGameSubdomains(0.1, 7.0)  #worst rated, at least 1000 popular
#popularityGameSubdomains(7.0, 10.0) #best rated, at least 1000 popular
#popularityGameSubdomains(0.1, 10.0) #all-inclusive, at least 1000 popular

#number of games that are in certain subdomain
#numberGameSubdomains(0.1, 7.0, 1000) #worst rated, at least 1000 popular
#numberGameSubdomains(7.0, 10.0, 1000) #best rated, at least 1000 popular
#numberGameSubdomains(0.1, 10.0, 1000) #all-inclusive, at least 1000 popular

#NOTE: average popularity per game subdomain is extrapolated by total popularity / number of popular games

#POPULARITY VS. QUANTITY MECHANICS
#numberQuantityGameMechanics(0.1, 7.0, 200)  #worst rated, at least 200 popular
#numberQuantityGameMechanics(7.0, 10.0, 200) #best rated, at least 200 popular
#numberQuantityGameMechanics(0.1, 10.0, 200) #all-inclusive, at least 200 popular
