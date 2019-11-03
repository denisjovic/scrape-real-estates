import requests
from bs4 import BeautifulSoup
import pandas


mylist = []

base_url = "http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/#t=0&s="
for page in range(0,30,10):
    url = base_url + str(page) + '.html'
    r = requests.get(url,  headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c = r.content
    soup = BeautifulSoup(c, 'html.parser')


    containers = soup.find_all('div', {'class':'propertyRow'})
    #price = containers.find_all('h4',{'class':'propPrice'}).text.strip()


    for item in containers:
        d={}
        d['Address'] = item.find_all('span', {'class':'propAddressCollapse'})[0].text
        d['Location'] = item.find_all('span', {'class':'propAddressCollapse'})[1].text
        d['Price'] = item.find('h4',{'class':'propPrice'}).text.strip()

        try:
            #print(item.find('span', {'class':'infoBed'}).text)
            d['Beds'] = item.find('span', {'class':'infoBed'}).find('b').text

        except:
            d['Beds'] = None
            
        try:
            # print(item.find('span', {'class':'infoValueFullBath'}).text)
            d['Bathrooms'] = item.find('span', {'class':'infoValueFullBath'}).find('b').text

        except:
            d['Bathrooms'] = None

        try:
            d['Area'] = item.find('span', {'class':'infoSqFt'}).text
            #print(item.find('span', {'class':'infoSqFt'}).find('b').text)

        except:
            d['Area'] = None

        for col_grp in item.find_all('div', {'class':'columnGroup'}):
            for ftr_grp, ftr_name in zip(col_grp.find_all('span', {'class':'featureGroup'}), col_grp.find_all('span', {'class':'featureName'})):
                if 'Lot Size' in ftr_grp.text:
                    d['Lot size'] = ftr_name.text.replace(',','')               

        mylist.append(d)

    # add list to pandas dataframe
    df = pandas.DataFrame(mylist)

    # send data to csv file
    df.to_csv('realestate.csv')
