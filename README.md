<h1>Traveling Salesman Problem 2-opt Solution and Basemap visualization</h1>

<h3>distanceQuery.py uses TSP_Source.dat to get Google Maps API Key and list of cities to work with. It returns the raw Google Distance Matrix response in json, cleaned up json to work with and a .xls table with list of cities their latitudes, longitudes and list of distances.</h3>

<h3>calc.py takes .xls table from created 'Results' directory, parses it for cities, their coords and distances. Script calculates solution using greedy algorithm and 2-opt optimization, and returns 2 png files with visualized solution of both algorithms.</h3>

<h3>All results of both scripts are saved into 'Results' directory.</h3>

<h3>All actions were computed on Python 3.5 on Anaconda platform.</h3>

<h3>Packages used:</h3> 
<ul>
<li>googlemaps</li> 
<li>matplotlib</li> 
<li>matplotlib.basemap</li> 
<li>xlwt</li> 
<li>xlrd</li>
<li>json</li>
</ul>

<h2>To run the scripts you will have to get Google Maps API Key and replace first line in TSP_Source.dat with it.</h2>

