import requests
import pprint
import time


proxies = {'http' : 'http://127.0.0.1:9000/',
            'https' : 'http://127.0.0.1:9000/' }

param = {'somekey': 'somevalue'}# data for post requests


r = requests.post('http://manganelo.com/', proxies=proxies, data = param)
#r = requests.get('http://manganelo.com/', proxies=proxies)

pprint.pprint(dict(r.headers))
print("\n\n")
with  open("site.html","w") as wr:
    wr.write(str(r.text.encode(encoding='UTF-8',errors='strict')))
#print(r.text)


#    https://www.w3schools.com/python/demopage.php



count =1

""" while count<1:
    print("\n\n"+str(count)+"\n\n")
    r = requests.get('https://manganelo.com/', proxies=proxies)
    pprint.pprint(dict(r.headers))
    print("\n\n")
    time.sleep(.5)
    count=count+1 """