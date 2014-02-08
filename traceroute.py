import sys
import mechanize
import os
import subprocess
import re
from BeautifulSoup import BeautifulSoup
from pygmaps import maps


print "hello world"
print sys.argv[1]
# Running Traceroute on your system
cmd = ['traceroute' , sys.argv[1] ]
output = subprocess.Popen(cmd,stdout=subprocess.PIPE).communicate()[0]
print "Done with Traceroute"


# Regex to search for ip addresses from the traceroute output . Incorrect regex but works because all ip's in the output are valid ip's .
ipregex = "([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})"
iplist = re.findall(ipregex,output)


# Finding Latitudes and Longitudes using a webservice which has access to ip-location database.
print "Retreiving Locations of ip's"
latitudes =[]
longitudes =[]
br = mechanize.Browser()
response = br.open("http://ipinfodb.com/index.php")
for i in br.forms():
	form = i

for i in iplist:
	response = br.open("http://ipinfodb.com/index.php")
	form["ip"] = i 
	request = form.click()
	response = br.open(request)
	html = response.read()

	soup = BeautifulSoup(html)
	lilist = soup.findAll('li')

	lat = float(lilist[len(lilist)-6].contents[0][11:])	#Latitude
	if lat!=0 :	
		latitudes.append(lat)

	lon = float(lilist[len(lilist)-5].contents[0][12:])	#Longitude
	if lon!=0 :
		longitudes.append(lon)


# Plotting the coordinates onto the map
print "Plotting the points on to the map"
points =[]
mymap = maps(37.438,-122.145,10)	# any starting point for the map and zoom level

for i in range(1,len(latitudes),2):
	mymap.addpoint(latitudes[i],longitudes[i],'#0000FF')
	temp = (latitudes[i],longitudes[i])
	if temp not in points:
		points.append(temp)

print points
mymap.addpath(points,"#00FF00")  
mymap.draw("traceroute.html")

 	
