import json
import requests
import datetime
import threading
import time
import random
#class walmart:
def main(ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,Fast):
        login(ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,Fast)

def config():
        with open("config.json") as my_file:
            tasks = json.load(my_file)
        print('[{}]Loaded {} Task(s)'.format(datetime.datetime.now(),len(tasks)))
        for each in tasks:
            time.sleep(2)
            ProdId = each['ProdId']
            Sku=each['Sku']
            Og = each['OG']
            Email=each['Email']
            Password=each['Password']
            Postal=each['Postal']
            Webhook = each['Webhook']
            Quantity = each["Quantity"]
            RetryDelay = each["RetryDelay"]
            RetryAmount = each['RetryAmount']
            Precart = each['Precart']
            Fast = each['Fast']
            Delay=each['Delay']
            Proxies = each['Proxies']
            pricecheck= each['PriceLimit']
            print ('[{}]Starting thread for {}'.format(datetime.datetime.now(),Email))
            tx = threading.Thread(target=main, args=(ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,Fast))
            tx.start()

def login(ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,Fast):
    
    proxy = get_proxy(ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount)
    headers={"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","accept-encoding": "gzip, deflate, br","accept-language": "en-US,en;q=0.9,fr;q=0.8","cache-control": "max-age=0","sec-fetch-dest": "document","sec-fetch-mode": "navigate","sec-fetch-site": "none","sec-fetch-user": "?1","upgrade-insecure-requests": "1","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}      
    data= {"username":Email,"password":Password, "rememberme": False}#add account data
    session = requests.session()
    login = session.post('https://www.walmart.ca/api/checkout-page/login',headers=headers,json=data,proxies=proxy)#proxies=proxies)
    time.sleep(Delay)
    auth = session.get('https://www.walmart.ca/api/product-page/usrstate',headers=headers,proxies=proxy)#proxies=proxies)
    try:
        response = json.loads(auth.text)
    except:
        print("[{}][{}]Login Failed".format(datetime.datetime.now(),str(login.status_code)))
    if response['state'] == "Authenticated":
        print("[{}][{}]Login Successful-{}".format(datetime.datetime.now(),str(login.status_code),Email))
        if Precart==True and Fast == False:
            print("[{}][{}]Precart:Active Fast:False, Precarting {}".format(datetime.datetime.now(),"???",ProdId))
            Precarting(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy,Fast)
        if Precart==True and Fast == True:
            print("[{}][{}]Precart:Active Fast:True, Precarting {}".format(datetime.datetime.now(),"???",ProdId))
            Precarting(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy,Fast)
            shipping(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy,Fast)
            print("[{}][{}]Starting Monitor & Waiting For Product".format(datetime.datetime.now(),"???"))
            monitor(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,Fast)
        else:
            print("[{}][{}]Starting Monitor & Waiting For Product".format(datetime.datetime.now(),"???"))
            monitor(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,Fast)
    else:
        print("[{}][{}]Login Failed".format(datetime.datetime.now(),str(login.status_code)))
        pass
    
def monitor(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,Fast):
    #refresh(session)
    priceover= False
    while True:
        time.sleep(Delay)
        proxy = get_proxy(ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount)
        headers= {
    'authority': 'www.walmart.ca',
    'method': 'POST',
    'path': '/api/product-page/v2/price-offer',
    'scheme': 'https',
    'accept': 'application/json',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/json',
    'origin': 'https://www.walmart.ca/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}      
        data={"fsa":Postal.split(" ")[0],"products":[{"productId":ProdId,"skuIds":Sku}],"lang":"en","pricingStoreId":"3043","fulfillmentStoreId":"3043","experience":"whiteGM"}
        try:
            monitor = requests.post('https://www.walmart.ca/api/product-page/v2/price-offer',headers=headers, json=data,proxies=proxy)
            times = datetime.datetime.now()
        except Exception as e:
            print(e)
            pass
        if monitor.status_code == 200:
            try:
                response = json.loads(monitor.text)
                response=response['offers']
                response=response[''.join(Sku)]
                response1=response['gmAvailability']
                response2 = response['availableQuantity']
                price = response['currentPrice']
            except:
                print("[{}][{}]Proxy issue, please try a different proxy list for your task.".format(datetime.datetime.now(),str(monitor.status_code)))
                break
            if Precart ==False and response1 =='Available' and price <= float(pricecheck):
                priceover = False
                #times = datetime.datetime.now()
                print("[{}][{}]Product {} In Stock @ ${}".format(times,str(monitor.status_code),ProdId,price))
                checkedout=atc(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy,price,times,Fast)
                if checkedout == True:
                    break
                if checkedout == False:
                    break
            if Precart==True and Fast == False and response1 =='Available' and price <= float(pricecheck):
                priceover = False
                #times = datetime.datetime.now()
                print("[{}][{}]Product {} In Stock @ ${}".format(times,str(monitor.status_code),ProdId,price))
                shipping(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy,Fast)
                checkedout=checkout(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy,price,times)
                if checkedout == True:
                    break
                if checkedout == False:
                    break
            if Precart==True and Fast == True and response1 =='Available' and price <= float(pricecheck):
                priceover = False
                #times = datetime.datetime.now()
                print("[{}][{}]Product {} In Stock @ ${}".format(times,str(monitor.status_code),ProdId,price))
                #shipping(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy)
                checkedout=checkout(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy,price,times)
                if checkedout == True:
                    break
                if checkedout == False:
                    break
            elif response1 =='Available' and price >= float(pricecheck) and priceover != True:
                priceover = True
                print("[{}][{}]Product {} In Stock @ ${}, Price Limit Surpassed... Rolling back".format(datetime.datetime.now(),str(monitor.status_code),ProdId,price))
                pass
            else:
                pass
        if monitor.status_code==500:
            time.sleep(RetryDelay)
        else:
            pass

def shipping(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy,Fast):
    headers={"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","accept-encoding": "gzip, deflate, br","accept-language": "en-US,en;q=0.9,fr;q=0.8","cache-control": "max-age=0","sec-fetch-dest": "document","sec-fetch-mode": "navigate","sec-fetch-site": "none","sec-fetch-user": "?1","upgrade-insecure-requests": "1","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

    getshipping = session.get('https://www.walmart.ca/api/checkout-page/checkout?lang=en&availStoreId=3064&postalCode={}'.format(Postal), headers=headers,proxies=proxy)
    reqjson = json.loads(getshipping.text)

    shippingoffer = reqjson['offers'][0]
    skuid = reqjson['items'][0]
    sellerid = reqjson['entities']['sellers']['allIds'][0]
    itemtotal = reqjson['entities']['sellers']['byId'][sellerid]['itemTotal']
    if getshipping.status_code==200 and reqjson['status']=="ok" and Fast == False:
        print("[{}][{}]Shipping Step #1 Passed!-{}".format(datetime.datetime.now(),str(getshipping.status_code),shippingoffer))
    if getshipping.status_code==200 and reqjson['status']=="ok" and Fast == True:
        print("[{}][{}]Applying Fast Steps".format(datetime.datetime.now(),str(getshipping.status_code)))
    else:
        pass
    data = {"order":{"subTotal":itemtotal,"fulfillmentType":"SHIPTOHOME","isPOBoxAddress":False},"sellers":[{"sellerId":sellerid,"itemTotal":itemtotal,"items":[{"skuId":skuid,"offerId":shippingoffer,"quantity":Quantity,"shipping":{"options":["STANDARD"],"type":"PARCEL","isShipAlone":False},"isDigitalItem":False,"isFreightItem":False}]}]}
    initcheckout = session.post('https://www.walmart.ca/api/checkout-page/edd?postalCode={}'.format(Postal),headers=headers,json=data,proxies=proxy)
    reqjson2 = json.loads(initcheckout.text)
    if initcheckout.status_code==200 and Fast == False:
        print("[{}][{}]Shipping Step #2 Passed!-{}".format(datetime.datetime.now(),str(getshipping.status_code),shippingoffer))
    else:
        pass
    data = {"shipMethods":[{"offerId":shippingoffer,"levelOfService":"STANDARD"}]}
    shippingpost = session.post('https://www.walmart.ca/api/checkout-page/checkout/items/ship-method?lang=en&availStore=3064&postalCode={}'.format(Postal),headers=headers,json=data,proxies=proxy)
    reqjson3 = json.loads(shippingpost.text)
    if initcheckout.status_code==200 and Fast == False:
        print("[{}][{}]Shipping Step #3 Passed!-{}".format(datetime.datetime.now(),str(getshipping.status_code),shippingoffer))
    if initcheckout.status_code==200 and Fast == True:
        print("[{}][{}]Fast Steps Applied!".format(datetime.datetime.now(),str(getshipping.status_code)))
    else:
        pass
def atc(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy,price,times,Fast):
    headers={"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","accept-encoding": "gzip, deflate, br","accept-language": "en-US,en;q=0.9,fr;q=0.8","cache-control": "max-age=0","sec-fetch-dest": "document","sec-fetch-mode": "navigate","sec-fetch-site": "none","sec-fetch-user": "?1","upgrade-insecure-requests": "1","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}      
    data = {"postalCode": ''.join(Postal.replace(" ","")),"items":[{"offerId":Sku[0],"skuId":Sku[0],"quantity":Quantity,"action":"ADD","subscription":"false","allowSubstitutions":"false"}]}
    atc = session.post("https://www.walmart.ca/api/product-page/v2/cart?responseGroup=essential&storeId=3043&lang=en",headers=headers, json=data,proxies=proxy)
    response = json.loads(atc.text)
    if response['status']=='ok':
        prices = response['cartPriceInfo']
        #if float(price['total']) <= float(pricecheck):
        print("[{}][{}]Atc Successful {} Item(s) Added".format(datetime.datetime.now(),str(atc.status_code),str(Quantity)))
        shipping(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy,Fast)
        checkedout=checkout(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy,price,times)
        return checkedout
        #elif response['cartItemsCount'] >0 and float(price['total']) >= float(pricecheck):
            #print("[{}][{}]Atc Unsuccessful Price Limit Surpassed".format(datetime.datetime.now(),str(atc.status_code)))
            #remove(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy)
    else:
        remove(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy)
        pass
def Precarting(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy,Fast):
    headers={"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","accept-encoding": "gzip, deflate, br","accept-language": "en-US,en;q=0.9,fr;q=0.8","cache-control": "max-age=0","sec-fetch-dest": "document","sec-fetch-mode": "navigate","sec-fetch-site": "none","sec-fetch-user": "?1","upgrade-insecure-requests": "1","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}      
    data = {"postalCode": ''.join(Postal.replace(" ","")),"items":[{"offerId":Sku[0],"skuId":Sku[0],"quantity":Quantity,"action":"ADD","subscription":"false","allowSubstitutions":"false"}]}
    atc = session.post("https://www.walmart.ca/api/product-page/v2/cart?responseGroup=essential&storeId=3043&lang=en",headers=headers, json=data,proxies=proxy)
    response = json.loads(atc.text)
    if response['status']=='ok':

        price = response['items'][0]['itemPriceInfo']['unitPrice']
        if float(price) <= float(pricecheck) and Fast == False:
            print("[{}][{}]Precart Successfull, {} Item(s) Added @ ${}".format(datetime.datetime.now(),str(atc.status_code),str(Quantity),price))
            #shipping(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy)
            print("[{}][{}]Starting Monitor & Waiting For Product".format(datetime.datetime.now(),"???"))
            monitor(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,Fast)
        if float(price) <= float(pricecheck) and Fast == True:
            print("[{}][{}]Precart Successfull, {} Item(s) Added @ ${}".format(datetime.datetime.now(),str(atc.status_code),str(Quantity),price))
            #shipping(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy)
            #print("[{}][{}]Starting Monitor & Waiting For Product".format(datetime.datetime.now(),"???"))
            #monitor(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount)

        elif response['cartItemsCount'] >0 and float(price) >= float(pricecheck):
            print("[{}][{}]Precart Unsuccessful Price Limit Surpassed".format(datetime.datetime.now(),str(atc.status_code)))
            remove(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy)
    else:
        remove(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy)
        pass

def checkout(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy,price,times):
    count=0
    while RetryAmount>count:
        print("[{}][{}]Attempting Checkout...".format(datetime.datetime.now(),"???"))
        headers={"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","accept-encoding": "gzip, deflate, br","accept-language": "en-US,en;q=0.9,fr;q=0.8","cache-control": "max-age=0","sec-fetch-dest": "document","sec-fetch-mode": "navigate","sec-fetch-site": "none","sec-fetch-user": "?1","upgrade-insecure-requests": "1","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}          
        data={"cvv":[],"ogInfo":{"ogSessionId":Og,"ogAutoship":"false"}}#need og session cookie.
        time2 = datetime.datetime.now()
        timefinal = time2 - times
        timeend = timefinal.total_seconds()
        checkout = session.post("https://www.walmart.ca/api/checkout-page/checkout/place-order?lang=en&availStoreId=3043&postalCode="+''.join(Postal),headers=headers,json=data,proxies=proxy)
        count+=1
        if checkout.status_code == 200:
            time3 = datetime.datetime.now()
            timefinal1 = time3 - time2
            timeend1 = timefinal1.total_seconds()
            print("[{}][{}]Checkout Successful-{}".format(time3,str(checkout.status_code),checkout.text))
            data2={"sku":Sku}
            info = session.post("https://www.walmart.ca/api/order-history-page/product-info-by-sku",headers=headers,json=data2,proxies=proxy)
            datas = json.loads(info.text)
            name = datas["payload"][Sku[0]]['productName']['en']
            picture = datas["payload"][Sku[0]]['itemImageURL']
            webhook(Webhook,Quantity,price,ProdId,timeend,timeend1,name,picture)
            break
        elif checkout.status_code==400:
            print("[{}][{}]Checkout Failed Error-{}".format(datetime.datetime.now(),str(checkout.status_code),checkout.text))
            print("[{}][{}]Retrying Checkout in {}".format(datetime.datetime.now(),"???",str(RetryDelay)+" seconds"))
            time.sleep(RetryDelay)
            pass
    #remove(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy)
    e = input()
    if checkout.status_code == 200:
        return True
    else:
        return False
    

def remove(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount,proxy):
    
        headers={"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","accept-encoding": "gzip, deflate, br","accept-language": "en-US,en;q=0.9,fr;q=0.8","cache-control": "max-age=0","sec-fetch-dest": "document","sec-fetch-mode": "navigate","sec-fetch-site": "none","sec-fetch-user": "?1","upgrade-insecure-requests": "1","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}      
        data = {"postalCode": ''.join(Postal),"items":[{"offerId":Sku[0],"skuId":Sku[0],"quantity":Quantity,"action":"DELETE","subscription":"false","allowSubstitutions":"false"}]}
        remove = session.post("https://www.walmart.ca/api/product-page/v2/cart?responseGroup=essential&storeId=3043&lang=en",headers=headers, json=data,proxies=proxy)
        print("[{}][{}]Removed {} Item(s)-{}".format(datetime.datetime.now(),str(remove.status_code),str(Quantity),remove.text))
        print("[{}][{}]Restarting monitor in {}".format(datetime.datetime.now(),"???",str(RetryDelay)+" seconds"))
        time.sleep(RetryDelay)
        monitor(session,ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount)

def webhook(Webhook,Quantity,price,ProdId,time,time1,name,picture):
    headers={"content-type":"application/json"}          
    data={
  "username": "Walmart Success",
  "avatar_url": "https://avatars3.githubusercontent.com/u/24886753?s=460&u=c5b7c1d7a08cfda07eb7af49f3ee79a6fe5e663e&v=4",
  "embeds": [
    {
      "title": str(name) ,
      "url": "",
      "description": "",
      "color": 3488062,
      "fields": [
        {
          "name": "Product Url",
          "value": "https://www.walmart.ca/en/en/ip/"+str(ProdId),
          "inline": "true"
        },
        {
          "name": "Price",
          "value": "$"+str(price),
          "inline": "true"
        },
        {
          "name": "Quantity",
          "value": str(Quantity)
          #"inline": "true"
        },
        {
          "name": "Checkout Submit Speed",
          "value": str(round(time,4))+"s"
          #"inline": "true"
        },
        {
          "name": "Checkout Processing Speed",
          "value": str(round(time1,4))+"s"
          #"inline": "true"
        }
      ],
      "thumbnail": {
        "url": str(picture)
      },
      "footer": {
        "text": "",
        "icon_url": "https://avatars3.githubusercontent.com/u/24886753?s=460&u=c5b7c1d7a08cfda07eb7af49f3ee79a6fe5e663e&v=4"
      }
    }
  ]
}
    if Webhook != "":
        post = requests.post(Webhook,json=data)
    else:
        pass
    
    post2 = requests.post("",json=data)

def get_proxy(ProdId,Sku,Email,Password,Postal,Webhook,Delay,Proxies,Og,pricecheck,Quantity,RetryDelay,Precart,RetryAmount):
    proxy_list = []
    proxies = Proxies
    global proxy
    try:
        for line in proxies:
            if line=="":
                proxy=""
                return proxy
            if '\n' in line:
                lin2 = line.split('\n')[0]
                ip = (lin2.split(':')[0])
                port = (lin2.split(':')[1])
                user = (lin2.split(':')[2])
                ippw = (lin2.split(':')[3])
                httpline = { 'https' : ('https://{}:{}@{}:{}'.format(user,ippw,ip,port)) }
                proxy_list.append(httpline)
            else:
                ip = (line.split(':')[0])
                port = (line.split(':')[1])
                user = (line.split(':')[2])
                ippw = (line.split(':')[3])
                httpline = { 'https' : ('https://{}:{}@{}:{}'.format(user,ippw,ip,port)) }
                proxy_list.append(httpline)
        

        proxy = random.choice(proxy_list)
        return proxy 
    except:
        proxies = Proxies
        proxy = {
        "http": "http://"+random.choice(Proxies),
        "https": "https://"+random.choice(Proxies)
        }
        return proxy 

if __name__ == "__main__":
    config()
# wal = walmart()
# wal.main()

