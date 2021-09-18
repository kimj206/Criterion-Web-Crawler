# Name: Johnny Kim
# Date: August 23, 2021
# Description: This program parses data from the
#              Criterion Collection website and 
#              displays each title next to its
#              respective Blu-Ray price if said
#              title is in stock.

from urllib.request import urlopen, Request # Import packages from urllib.request library to open and read website
from bs4 import BeautifulSoup # Import Beautiful Soup from bs4 to parse read in HTML data

titleURL = [] # Array for all film URLs to go into 
titles = [] # Array for all film titles to go into
prices = [] # Array for all film prices to go into 
inURL = "" # String to store URL which is appended to titleURL
newTitle = "" # String to store title and append to titles
newPrice = "" # String to store price and append to prices 

web_url = "https://www.criterion.com/shop/browse/list?sort=spine_number" # Website URL
headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html'} # Header to satisfy Request function 

dataReq = Request(url = web_url, headers = headers) # Request access to website
dataOp = urlopen(dataReq) # Open website
pageData = dataOp.read() # Read data from website
dataOp.close() # Close website 

pageP = BeautifulSoup(pageData, 'html.parser') # Parse read in website data for HTML scripts
parent_node = pageP.find("tbody", {"data-is-load-more-container": ""}) # Place encapsulating tag for film URLs in parent node variable

offspring = parent_node.findChildren("tr", recursive=False) # Find all child nodes of parent node with table row tag 

# For loop appends URLs to titleURL
for i in range(len(offspring)):
   temp = str(offspring[i]) # Store string cast of current index into temporary string 
   for j in range(len(temp))[32:]: 
      if temp[j] == '"': # Once end of URL has been reached at " symbol, break
         break
      inURL += temp[j] #Store each film URL in string and append to titleURL
   titleURL.append(inURL)
   inURL = '' # Reset inURL to empty string 

for i in range(13): # 13 chosen as limit to avoid for running too long (processing 1490 elements takes around 22 minutes)
   # Bottom code block opens up and reads in data from first 13 URLs
   newReq = Request(url = titleURL[i], headers = headers)
   newOp = urlopen(newReq)
   newData = newOp.read()
   newOp.close()

   # Bottom code block finds title from webpage and adds to array 
   newP = BeautifulSoup(newData, 'html.parser')
   newParent = newP.find("h1", class_ = "header__primarytitle") # Locate title from HTML
   temp = str(newParent)
   for j in range(len(temp))[49:]: # Start at first character of title 
      if temp[j] == '<': # Stop processing string at bracket
         break
      newTitle += temp[j] # Add character to newTitle string 
   titles.append(newTitle) # Once string is complete, append newTitle to titles
   newTitle = "" # Set newTitle to empty string

   # Bottom code block finds price from webpage and adds to array 
   newParent = newP.find("span", class_ = "item-price") # Locate price from HTML
   temp = str(newParent)
   for j in range(len(temp))[25:]: # Start at first character of price
      if temp[j] == '<': # Stop processing string at bracket
         break
      newPrice += temp[j]
   prices.append(newPrice)
   newPrice = ""

# Bottom for loop prints each title and its price 
for i in range(len(titles)):
   print(titles[i], prices[i])

print(len(titleURL)) # Print length of URL array to show 1490 titles have been obtained