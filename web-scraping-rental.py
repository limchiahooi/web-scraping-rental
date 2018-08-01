import numpy as np
import pandas as pd
# import googlemaps
from urllib.request import urlopen
from bs4 import BeautifulSoup
# import requests
import csv
from datetime import datetime, timedelta

# You can change the State, StartPageRange and EndPageRange here
State = "Kuala-Lumpur"
StartPageRange = 1
EndPageRange = 2

datafile = "mudah1_"+ State.lower() + "_page" + str(StartPageRange) + "to" + str(EndPageRange - 1) + ".csv"

with open(datafile, 'a', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["PostedDate", "PropertyName", "CategoryType", "PropertyType", "City", "State", "Furnishing", "BuiltUpSize", "AgeofProperty", "RentalDeposit", "NoOfBedroom", "NoOfBathroom", "NoOfParking", "RentalPerMth", "Facilities", "OtherFacilities", "SourceUrl"])
    

all_links = []
for i in range(StartPageRange, EndPageRange):
    firsturl = "https://www.mudah.my/" + State + "/Properties-for-rent-2002?o=" + str(i) + "&q=&so=1&th=1"
    response = urlopen(firsturl)
    data = BeautifulSoup(response.read(),'lxml')
    
    prop_urls = data.find_all("h2", {"class":"list_title"})
    

    for links in prop_urls:
        links.find_all("a")
        for link in links:
            all_links.append(link.get("href"))

    if 'https://www.mudah.my/honeypot.html' in all_links:
        all_links.remove('https://www.mudah.my/honeypot.html')
    
    
    
for i in range(len(all_links)):
    ind_page_response = urlopen(all_links[i])
    data2 = BeautifulSoup(ind_page_response.read(),'lxml')
    
    SourceUrl = all_links[i]

    prop_name = data2.find("h2", {"class":"roboto"})
    PropertyName = prop_name.text.strip()

    for i in range(len(data2.select('.params dt'))):
        if data2.select('.params dt')[i].text == "Property Type":
            PropertyType = data2.select('.params dd')[i].text


    if data2.find("dd", {"class":"loc_dd"}) != None:
        City = data2.find("dd", {"class":"loc_dd"}).text.strip().split(" - ")[1]

    if data2.find("dd", {"class":"loc_dd"}) != None:
        State = data2.find("dd", {"class":"loc_dd"}).text.strip().split(" - ")[0]

    
    for i in range(len(data2.select('.params dt'))):
        if data2.select('.params dt')[i].text == "Size":
            BuiltUpSize = data2.select('.params dd')[i].text
            BuiltUpSize = float(BuiltUpSize.strip(' sq.ft.'))

    NoOfBedroom = ''
    for i in range(len(data2.select('.params dt'))):
        if data2.select('.params dt')[i].text == "Bedrooms":
            NoOfBedroom = data2.select('.params dd')[i].text
            NoOfBedroom = int(NoOfBedroom)

    NoOfBathroom = ''
    for i in range(len(data2.select('.params dt'))):
        if data2.select('.params dt')[i].text == "Bathroom":
            NoOfBathroom = data2.select('.params dd')[i].text
            NoOfBathroom = int(NoOfBathroom)

    NoOfParking = ''
    for i in range(len(data2.select('.params dt'))):
        if data2.select('.params dt')[i].text == "Carpark":
            NoOfParking = data2.select('.params dd')[i].text
            NoOfParking = int(NoOfParking)

    Furnishing = ''
    for i in range(len(data2.select('.params dt'))):
        if data2.select('.params dt')[i].text == "Furnished":
            Furnishing = data2.select('.params dd')[i].text
            
    Facilities = ''
    for i in range(len(data2.select('.params dt'))):
        if data2.select('.params dt')[i].text == "Facilities":
            Facilities = data2.select('.params dd')[i].text
            
    OtherFacilities = ''
    for i in range(len(data2.select('.params dt'))):
        if data2.select('.params dt')[i].text == "Other Facilities":
            OtherFacilities = data2.select('.params dd')[i].text
        
    AgeofProperty = ''
    for i in range(len(data2.select('.params dt'))):
        if data2.select('.params dt')[i].text == "Age of Property":
            AgeofProperty = data2.select('.params dd')[i].text
            AgeofProperty = int(AgeofProperty.strip(" Year(s)"))
            
    RentalDeposit = ''
    for i in range(len(data2.select('.params dt'))):
        if data2.select('.params dt')[i].text == "Rental Deposit":
            RentalDeposit = data2.select('.params dd')[i].text.strip("RM ")
            RentalDeposit = float(RentalDeposit)
            
    CategoryType = ''
    CategoryType = data2.select('.highlight-title-value')[0].text
            

    if data2.find("dd", {"class":"dd-price"}) != None:
        RentalPerMth = float(data2.find("dd", {"class":"dd-price"}).text.strip().strip("RM").strip("(per month)").replace(" ", ""))


    if data2.find("div", {"class":"list_time"}).text.strip().split(" ")[0] == "Today":
        PostedDate = datetime.today().date()
    elif data2.find("div", {"class":"list_time"}).text.strip().split(" ")[0] == "Yesterday":
        PostedDate = datetime.today().date() - timedelta(days=1)
    else:
        PostedDate = datetime.strptime(a[:6] + " " + str(datetime.today().year), '%d %b %Y').date()

    

    with open(datafile, 'a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([PostedDate, PropertyName, CategoryType, PropertyType, City, State, Furnishing, BuiltUpSize, AgeofProperty, RentalDeposit, NoOfBedroom, NoOfBathroom, NoOfParking, RentalPerMth, Facilities, OtherFacilities, SourceUrl])


