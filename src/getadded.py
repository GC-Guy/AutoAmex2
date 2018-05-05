#!/usr/bin/env python

from datetime import datetime
import sys
from helper import *

def getAddedOffers(username, password, lastfive, nickname, outputlog = True, browser = "Chrome"):
    if username == [] or password == [] or len(username) != len(password):
        print("username array does not have the same length as password array...")
    driver = getDriver(browser)
    majorOfferDollarMap = dict()
    majorOfferDescMap = dict()
    majorOfferDateMap = dict()
    majorDateOfferPair = set()
    userOffersList = []

    for idx in range(len(username)):
        sys.stdout.write('\r                                            \rRunning ' + username[idx])
        sys.stdout.flush()
        try:
            driver.get(amexWebsite)
        except:
            print("website is not available...")
            return
        # fill and submit login form
        try:
            amexLogIn(driver, username[idx], password[idx])
        #   print username[idx]
        except:
            print("username/password combination is incorrect...")
    #      print username[idx]
            continue
        time.sleep(2)
        # main program
        driver.get(added_page)
        # Wait for page to load
        time.sleep(4)
        # Find all offers
        offers = driver.find_elements_by_xpath('//*[@id="offers"]/div/section[2]/section/div')
        # Remove line with filters
        offers.pop(0)
        # Extract text of each offer
        offerstext = [offer.text.encode('utf-8') for offer in offers]
        offersplit = [text.split('\n') for text in offerstext]
        offerDollarMap = dict()
        offerDescMap = dict()
        offerDateMap = dict()
        dateOfferPair = set()
        offersSet = set()
        # discard expired offers
        for sp in offersplit:
            if sp[2] == 'EXPIRES':
                expiration = sp[3]
            else:
                expiration = sp[2]
            offerDollarMap[sp[0] + sp[1]] = sp[0]
            offerDescMap[sp[0] + sp[1]] = sp[1]
            offerDateMap[sp[0] + sp[1]] = expiration
            dateOfferPair.add((expiration, sp[0] + sp[1]))
            offersSet.add(sp[0] + sp[1])
        majorOfferDollarMap.update(offerDollarMap)
        majorOfferDescMap.update(offerDescMap)
        majorOfferDateMap.update(offerDateMap)
        majorDateOfferPair.update(dateOfferPair)

        # accomodate new AMEX GUI
        if len(offers) == 0:
            offers = driver.find_elements_by_xpath("//*[contains(text(), 'Spend ') or contains(text(), 'Get ')]")
            offerstext = [n.text.encode('utf-8') for n in offers]
            offers = [offers[i] for i in range(len(offers)) if offerstext[i] != '']
            offerstext = filter(None, offerstext)
            offers = [e.find_element_by_xpath('..') for e in offers]
            offerstext = [n.text.encode('utf-8') for n in offers]
            offerstext = filter(None, offerstext)
            tmpnames = [n.split('\n')[1] for n in offerstext]
            offerDescMap = {n.split('\n')[1]: n.split('\n')[0] for n in offerstext}
            for n in tmpnames:
                offersSet.add(n)
            majorOfferDescMap.update(offerDescMap)
        userOffersList.append(offersSet)

        time.sleep(1)
        # logout
        try:
            amexLogOut(driver)
        except:
            pass

        time.sleep(5)


    majorDateOfferList = list(majorDateOfferPair)
    majorDateOfferList.sort(key=lambda tup:tup[0])
    orig_stdout = sys.stdout
    if outputlog:
        logfilename = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        logfilename = "offers " + logfilename.replace(':', '_') + ".csv"
        logfile = open('../tmp/' + logfilename, 'w+')
        sys.stdout = logfile

    printoffer = 'Username,Last5,Nickname'
    for dateOffer in majorDateOfferList:
        offer = majorOfferDollarMap[dateOffer[1]].replace(',', ' and')
        printoffer = printoffer + "," + offer
    # write 2nd line
    printdesc = ',,'
    for dateOffer in majorDateOfferList:
        desc = majorOfferDescMap[dateOffer[1]].replace(',', ' and')
        printdesc = printdesc + "," + desc
    # write 3rd line
    printdate = ',,'
    for dateOffer in majorDateOfferList:
        date = majorOfferDateMap[dateOffer[1]]
        printdate = printdate + "," + date

    # Print to csv file
    print(printoffer)
    print(printdesc)
    print(printdate)
    for i in range(len(username)):
        myline = str(username[i]) + "," + str(lastfive[i]) + "," +  str(nickname[i])
        for dateOffer in majorDateOfferList:
            if dateOffer[1] in userOffersList[i]:
                myline = myline + ",+"
            else:
                myline = myline + ","
        print(myline)

    # Close csv file
    if outputlog:
        sys.stdout = orig_stdout
        logfile.close()

def main():
    username, password, lastfive, nickname = loadConfig("../conf/config.csv")
    getAddedOffers(username, password, lastfive, nickname, outputlog = True)

if __name__ == '__main__':
    main()
