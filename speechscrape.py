
# coding: utf-8

## Iterates across the S public remarks from 2014

# and returns a dict called 'remarks_dict' where each key is a month string from '01' to '12' and each value is a list of remarks from that month.
# 
# For example, access January's remarks by calling:
# remarks_dict['01']

#### Imports and Functions

# In[1]:

from bs4 import BeautifulSoup
import urllib2


# Here I set up the *months* variable for iterating across the state.gov pages. Note that I convert each *month* to a string.

# In[39]:

months = []
for month in range(1,13):
    if month < 10:
        month_i = "0" + str(month)
    else:
        month_i = str(month)
    months.append(month_i)

print months


# This defines a function to grab the html of the site. Pass variable *month* which is plugged into the url within the request

# In[3]:

def get_soup(month):
    request = urllib2.Request("http://www.state.gov/secretary/remarks/2014/" + month + "/index.htm")
    response = urllib2.urlopen(request)
    global soup
    soup = BeautifulSoup(response)
    return soup


# This defines a function that grabs all the links within the #tier3-landing-content-wide div of the site. These are the links to the remarks.

# In[4]:

def get_links(soup):
    global links
    links = []
    for div in soup.findAll('div', {'id': 'tier3-landing-content-wide'}):
        for a in div.findAll('a'):
            links.append(a['href'])
    print str(len(links)) + " links were found"
    return links


# This defines a function that grabs the remarks from the #centerblock div of the remarks page.

# In[5]:

def get_remarks(links):
    global remarks
    remarks = []

    for link in links:
        request = urllib2.Request(link)
        response = urllib2.urlopen(request)
        soup = BeautifulSoup(response)

        remark = str()
        for div in soup.findAll('div', {'id': 'centerblock'}):
            for p in div.findAll('p'):
                remark += p.text

        remarks.append(remark)
    print str(len(remarks)) + " remarks were found"
    return remarks


#### Putting it all together

# Here a dict called *remarks_dict* is built by iterating through each month in *months*. The dict contains the remarks for each month returned as a comma separated list.

# In[6]:

remarks_dict = {}

for month in months:
    get_soup(month)

    get_links(soup)
    get_remarks(links)
    
    remarks_dict[month] = remarks


# Let's take a look at the 3rd remark from June. Note that the "first" remark is at the 0 index, so to get the third remark ask for the remark at index 2.

# In[43]:

remarks_dict['06'][2]

