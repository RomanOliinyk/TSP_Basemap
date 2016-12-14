# -*- coding: utf-8 -*-
'''
Creating script to parse every possible city to city destination possible using
Google Distance Matrix API module. Importing results to JSON file, creating
clean json version of results file with info needed just for working with and
creating Excel Workbook with clean results just for looks.
'''
import googlemaps # importing googlemaps module
import json     # importing json module
from xlwt import Workbook # importing Excel writing module
import os       # importing os module to work with directories

def distanceQueryFunction(googleAPIKey, cityList, jsonName, excelName):

    # Google API Key ( has to be enabled in Google Developer Console)
    gmaps = googlemaps.Client(key = googleAPIKey)

    # Sorting citiesList to get all results in aphabetical order
    cityList.sort()

    # List of all results from distance_matrix request
    resultsTotal = []

    # List of all items needed for resultsTotalClean
    # resultsTotalClean = [cleanCitiesDict, distancesTotal list]
    resultsTotalClean = []
    # List of Google fixed city Names
    cleanCitiesList = []
    # {"Cities": [List of Cities Google fixed Names]}
    cleanCitiesDict = {"Cities": cleanCitiesList}
    #  list of {"City's Google Name": [distanceList to other cities]}
    distancesTotal = []

    # Opening excel Workbook to work with and fill it on the go
    book = Workbook(encoding='utf-8')
    sheet1 = book.add_sheet('Sheet 1', cell_overwrite_ok=True)
    # "row" and "col" starting coordinates of Excel Workbook
    row = 0 # Data row
    col = 1 # Data column

    # Going through every item in cityList, to create every possible combination
    # of 'origin_addresses' to 'destination_addresses'
    for item in cityList:
        print ('Starting ' + item + ' scan.') # Current City scanned

        # Calling Google Distance Matrix Module and saving to temporary
        # distanceMatrix dictionary to perform actions on
        distanceMatrix = gmaps.distance_matrix(item, cityList)

        # Google Geocode data
        geocode = gmaps.geocode(item)
        # latitude
        lat = geocode[0]["geometry"]["location"]["lat"]
        # Longitude
        lng = geocode[0]["geometry"]["location"]["lng"]

        # Current city in distanceMatrix
        currentCity = distanceMatrix["origin_addresses"][0]

        # Appending currentCity to cleanCitiesList
        cleanCitiesList.append(currentCity)

        # Temp empty list to fill with current city distances
        distancesTemp = []
        # Teml dict {"currentCity": distancesTemp}
        cityDictTemp = {}

        # Checking Status Code if "OK" perform action, else type fail message
        if distanceMatrix["status"] == "OK":

            # getting every distance, except when it cannot be done
            # then error message and appending 'error' to the list
            for element in distanceMatrix["rows"][0]["elements"]:
                distanceValue = element["distance"]["value"]
                try:
                    distancesTemp.append(distanceValue)
                    # Filling in Excel Workbook column by column
                    sheet1.write(row, col+2, int(distanceValue))
                    row += 1
                except KeyError:
                    print ('Error with ' + currentCity)
                    distancesTemp.append('error')

            print (distancesTemp) # show distances for currentCity
            # filling and appending cityDictTemp to cleanCitiesList
            cityDictTemp[currentCity] = [distancesTemp]
            distancesTotal.append(cityDictTemp)
        else:
            print ('Destination results failed for ' + currentCity)

        # adding Cities and coordinates to Excel Workbook
        sheet1.write(col-1, 0, str(currentCity))
        sheet1.write(col-1, 1, lng)
        sheet1.write(col-1, 2, lat)
        # reseting "m" value and adding +1 to "n"
        row = 0
        col += 1

        # Appending unformated distanceMatrix to resultsTotal
        resultsTotal.append(distanceMatrix)

        print ('Finished scanning ' + item) # Finishing scan

    # Appending cleanCitiesDict and cleanCitiesList to resultsTotalClean
    resultsTotalClean.append(cleanCitiesDict)
    d = {"distance_result": distancesTotal}
    resultsTotalClean.append(d)

    # Creating 'Results' directory and changing working location to save files
    os.makedirs('Results', exist_ok=True)
    os.chdir('Results')


    # Saving Excel Workbook
    excelName = '{}.xls'.format(excelName)
    book.save(excelName)

    # Creating JSON files for both resultsTotal and resultsTotalClean
    jsonCleanName = 'clean{}.json'.format(jsonName)
    jsonName = '{}.json'.format(jsonName)
    with open(jsonCleanName, 'w') as outfileClean:
        json.dump(resultsTotalClean, outfileClean, indent=4, skipkeys=True,
            sort_keys=True)
    with open(jsonName, 'w') as outfile:
        json.dump(resultsTotal, outfile, indent=4, skipkeys=True,
            sort_keys=True)


# Open and Start TSP_Source.dat
def openAndStart(filename):
    # creating cityList
    cityList = []
    with open(filename) as inFile:
        firstLine = inFile.readline()
        key = str(firstLine[0:-1])
        print (key)
        for line in inFile:
            city = line[0:-1]
            cityList.append(city)
    print (cityList)

    jsonName = 'queryResult'
    excelName = 'queryTable'
    # running distanceQueryFunction
    distanceQueryFunction(key, cityList, jsonName, excelName)


openAndStart('TSP_Source.dat')

'''
    LIST OF CITIES
	'Vienna, Austria', 'Minsk, Belarus', 'Sofia, Bulgaria', 'Zagreb, Croatia',
	'Prague, Czech Republic', 'Paris, France', 'Marseille, France',
	'Berlin, Germany', 'Hamburg, Germany', 'Munich, Germany',
	'Cologne, Germany', 'Athens, Greece', 'Salonika, Greece',
	'Budapest, Hungary', 'Rome, Italy', 'Milan, Italy', 'Naples, Italy',
	'Turin, Italy', 'Palermo, Italy', 'Riga, Latvia', 'Amsterdam, Netherlands',
	'Warsaw, Poland', 'Lodz, Poland', 'Krakow, Poland', 'Belgrade, Serbia',
	'Madrid, Spain', 'Barcelona, Spain', 'Valencia, Spain', 'Sevilla, Spain',
	'Stockholm, Sweden', 'London, UK', 'Birmingham, UK', 'Leeds, UK',
	'Kyiv, Ukraine', 'Kharkiv, Ukraine', 'Dnipro, Ukraine', 'Donetsk, Ukraine',
	'Odessa, Ukraine', 'Zaporozhya, Ukraine', 'Lviv, Ukraine',
	'Kryvy Rig, Ukraine', 'Kishinev, Moldova', 'Genova, Italy',
	'Frankfurt am Main, Germany', 'Wroclaw, Poland', 'Glasgow, UK',
	'Zaragoza, Spain', 'Essen, Germany', 'Rotterdam, Netherlands',
	'Dortmund, Germany'

'''
