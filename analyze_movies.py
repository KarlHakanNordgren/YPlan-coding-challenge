
################################################
################################################
############# 

#!/usr/bin/python

################################################
################################################
############# modules

import sys # for CLI arguments
from itertools import groupby # for group averages
from operator import itemgetter # for group averages

################################################
################################################
############# repeat CLI arguments back to user

varName = sys.argv[1]
numCat = sys.argv[2]

print('################################################')
print('################################################')
print('\n')
print('You have requested the names of the top %s movies grouped by %s.' %(numCat, varName))
print('\n')
print('################################################')
print('################################################')

################################################
################################################
############# check that CLI arguments are valid

# check first argument which should be 'age' or 'gender'
if (varName.lower() not in ['age', 'gender']):
	sentenceOne = 'You have to group the data either by age or gender.'
	sentenceTwo = '%s is not a valid grouping option.' %varName
	print(sentenceOne + ' ' + sentenceTwo[0].upper() + sentenceTwo[1:])
	sys.exit(0)

# check second argument which should be an integer
try:
	numCat = int(numCat)
except ValueError:
	sentenceOne = 'You have to specify an integer number of categories.'
	sentenceTwo = '%s is not an integer.' %numCat
	print(sentenceOne + ' ' + sentenceTwo[0].upper() + sentenceTwo[1:])
	sys.exit(0)
	
################################################
################################################
############# load datasets

def loadData(fileName, maxRow = -1):
	"""This functions takes the filename of a dataset and returns the dataset array. 
	There is an optional argument of how many rows to return for debugging purposes. If maxRow = -1
	then the functions returns the whole dataset"""
	dataset = []
	with open(fileName,'r') as f:
		numRows = len(list(enumerate(f)))
	with open(fileName,'r') as f:
		if maxRow == -1:
			maxRow = numRows - 1
		for i, line in enumerate(f):
			if i <= maxRow:
				lineString = line.split('::')
				lineNoEOL = [s.replace('\n', '') for s in lineString]
				dataset.append(lineNoEOL)
	return dataset;

# ratings: The input file is in format UserID::MovieID::Rating::Timestamp
ratingsFileName = u'C:\\work\\coding challenge\\data\\ml-1m\\ratings.dat'
ratings = loadData(ratingsFileName, maxRow = -1)

# users: The input file is in format UserID::Gender::Age::Occupation::Zip-code
usersFileName = u'C:\\work\\coding challenge\\data\\ml-1m\\users.dat'
users = loadData(usersFileName, maxRow = -1)

# movies: The input file is in format MovieID::Title::Genres
moviesFileName = u'C:\\work\\coding challenge\\data\\ml-1m\\movies.dat'
movies = loadData(moviesFileName, maxRow = -1)

'''
users = [
    ['M01', 'F', '23', 1, 1],
    ['M02', 'F', '4', 1, 1],
    ['M03', 'M', '45', 1, 1],
	['M04', 'M', '3', 1, 1],
]
ratings = [['M01', 'A', 2, 3], ['M01', 'B', 3, 3], ['M03', 'C', 5, 3], ['M02', 'A', 4, 3]]
movies = [['A', 'Hook', 3], ['B', 'Shrek', 3], ['C', 'Regardless', 3]]
'''

################################################
################################################
############# join datasets

# inner join users and ratings

# UserID is id
usersDict = dict([(user[0], user[1:]) for user in users])

# userRatings will have columns UserID::MovieID::Rating::Timestamp::Gender::Age::Occupation::Zip-code
userRatings = []
for rating in ratings:
	if rating[0] in usersDict:
		userRating = list(rating) + list(usersDict.get(rating[0]))
		userRatings.append(userRating)
		
################################################
################################################
############# 

if varName.lower() == 'gender':
	varIndex = 4
if varName.lower() == 'age':
	varIndex = 5
	
# MovieID has index 1
# Rating has index 2
# the grouping variable has index varIndex
idColumns = itemgetter(1, varIndex)
valColumn = 2

userRatingsSorted = sorted(userRatings, key = idColumns)
#groupMeans will have columns MovieID::grouping variable::mean rating
groupMeans = []
for k, g in groupby(userRatingsSorted, idColumns):
	groupRatings = [int(item[valColumn]) for item in g]
	numInGroup = len(groupRatings)
	if numInGroup == 0:
		continue
	groupMean = sum(groupRatings)/numInGroup
	row = [item for item in k]
	row.append(groupMean)
	row.append(numInGroup)
	groupMeans.append(row)


groupMeansSorted = sorted(groupMeans, key = itemgetter(1, 2, 3), reverse = True)

movieDict = dict([(movie[0], movie[1:]) for movie in movies])

for k, g in groupby(groupMeansSorted, itemgetter(1)):
	##for item in g:
	##	print(item)

	###groupMeansOrder = sorted(groupMeans, key = itemgetter(2, 3), reverse = True)
	topItemsInGroup = []
	for i, item in enumerate(g):
		if i < numCat:
			topItemsInGroup.append(item)
	topMovies = []
	# topMovies has columns MovieID::grouping variable::mean rating::num ratings::Title::Genres
	for item in topItemsInGroup:
		if item[0] in movieDict:
			topMovie = list(item) + list(movieDict.get(item[0]))
			topMovies.append(topMovie)
	print('\n')
	print('The top %s movies for %s = %s are:' %(numCat, varName, k))
	print('\n')
	for i, movie in enumerate(topMovies):
		print('Movie %d: "%s"; score: %s; number of ratings: %d' %(i+1, movie[4], movie[2], movie[3]))
	print('\n')
	
	
	
