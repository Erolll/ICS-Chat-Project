import http.cookiejar
import urllib.request
import requests
import bs4

def grab_financial_news():
    url = "https://finance.yahoo.com/news/"
    
    #Unpackaging and Surfing the Web
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)

    data = requests.get(url, cookies = cj)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')

    dataDict = {
        "Article Name":[],
        "Article Description":[],
        "Link":[]
        }
    for ultag in soup.find_all('ul', {'class': 'Mb(0) Ov(h) P(0) Wow(bw)'}):
        for litag in ultag.find_all('li'):
            for h3 in litag.find_all('h3'):
                dataDict["Article Name"].append(h3.getText())
                for p in litag.find_all('p'):
                    dataDict["Article Description"].append(p.getText())
                    for a in litag.find_all('a', href=True):
                        dataDict["Link"].append("https://finance.yahoo.com" + a['href'])


    return dataDict

def grab_financial_currencies():
    url = "https://finance.yahoo.com/cryptocurrencies"
    
    #Unpackaging and Surfing the Web
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)

    data = requests.get(url, cookies = cj)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    #print(data)
    
    theData = soup.findChildren('table', attrs={'class':'W(100%)'})
    moreKids = theData[0]
    rows = moreKids.findChildren(['th', 'tr'])

    dataDict = {
        "Name":[],
        "Price":[],
        "Change":[],
        "%Change":[],
        "Volume":[],
        "Market Cap":[],
        "Circulating Supply":[]
        }
    
    count = 0
    for row in rows:
        if count == 5:
            break
        cells = row.findChildren('td')
        try:
            dataDict["Name"].append(cells[1].getText())
            dataDict["Price"].append(cells[2].getText())
            dataDict["Change"].append(cells[3].getText())
            dataDict["%Change"].append(cells[4].getText())
            dataDict["Volume"].append(cells[5].getText())
            dataDict["Market Cap"].append(cells[6].getText())
            dataDict["Circulating Supply"].append(cells[7].getText())
            count += 1
        except:
            pass

    return dataDict

    
def grab_financial_commodities():
    url = "https://finance.yahoo.com/commodities"
    
    #Unpackaging and Surfing the Web
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)

    data = requests.get(url, cookies = cj)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    #print(data)
    
    theData = soup.findChildren('table', attrs={'class':'yfinlist-table W(100%) BdB Bdc($tableBorderGray)'})
    moreKids = theData[0]
    rows = moreKids.findChildren(['th', 'tr'])

    dataDict = {
        "Name":[],
        "Last Price":[],
        "Market Time":[],
        "Change":[],
        "%Change":[],
        "Volume":[]
        }
    
    count = 0
    for row in rows:
        if count == 5:
            break
        cells = row.findChildren('td')
        try:
            dataDict["Name"].append(cells[1].getText())
            dataDict["Last Price"].append(cells[2].getText())
            dataDict["Market Time"].append(cells[3].getText())
            dataDict["Change"].append(cells[4].getText())
            dataDict["%Change"].append(cells[5].getText())
            dataDict["Volume"].append(cells[6].getText())
            count += 1
        except:
            pass
    return dataDict
    
def grab_financial_full():
    url = "https://finance.yahoo.com/world-indices"

    #Unpackaging and Surfing the Web
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    urllib.request.install_opener(opener)

    data = requests.get(url, cookies = cj)
    soup = bs4.BeautifulSoup(data.text, 'html.parser')
    #print(data)
    
    theData = soup.findChildren('table', attrs={'class':'yfinlist-table W(100%) BdB Bdc($tableBorderGray)'})
    moreKids = theData[0]
    rows = moreKids.findChildren(['th', 'tr'])

    dataDict = {
        "Name":[],
        "Last Price":[],
        "Change":[],
        "%Change":[],
        "Volume":[]
        }

    count = 0
    for row in rows:
        if count == 5:
            break
        cells = row.findChildren('td')
        try:
            dataDict["Name"].append(cells[1].getText())
            dataDict["Last Price"].append(cells[2].getText())
            dataDict["Change"].append(cells[3].getText())
            dataDict["%Change"].append(cells[4].getText())
            dataDict["Volume"].append(cells[5].getText())
            count += 1
        except:
            pass
    return dataDict
        
    
    
def grab_financial_data(name):
    #URL
    url = "https://finance.yahoo.com/quote/"
    url += name
    
    financeData = {}
    #Unpackaging and Surfing the Web
    try:
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        urllib.request.install_opener(opener)

        data = requests.get(url, cookies = cj)
        soup = bs4.BeautifulSoup(data.text, 'html.parser')


        #Grabs Name
        nameData = soup.find('div', attrs={'class': 'D(ib)', 'data-reactid':'6'})
        financeData["Name"] = nameData.getText()

        #Grabs Price and Change
        priceChangeData = soup.findChildren('div', attrs={'class':'My(6px) Pos(r) smartphone_Mt(6px)'})
        newPriceChangeData = priceChangeData[0]
        thePrice = newPriceChangeData.findChildren(['span'])
        
        financeData["Current Price"] = thePrice[0].getText()
        financeData["Change"] = thePrice[1].getText()

        #Grabs Table With Most Info
        allTables = soup.findChildren('table')
        my_table = allTables[0]
        rows = my_table.findChildren(['th', 'tr'])
        
        for row in rows:
            cells = row.findChildren('td')
            financeData[cells[0].getText()] = cells[1].getText()
    

    except:
        pass
    return financeData

#grab_financial_data("TSLA")
#print('==='*20)
#grab_financial_data("UBER")
#print('==='*20)
#grab_financial_data("AAPL")
