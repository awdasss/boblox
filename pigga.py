import requests
from bs4 import BeautifulSoup
import time
import random_proxies
import random
import urllib3
import threading
import ctypes
urllib3.disable_warnings()
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'
        }

used=0
used2=10
duplicates = []
val = 0
dupli = 0
invalid = 0
err = 0
key = input('Enter the main word: ')



proxy = open('proxy.txt').read().split('\n')

def stat():
    ctypes.windll.kernel32.SetConsoleTitleW(f"Invalid:{invalid} | Valid:{val} | Duplicates:{dupli} | Errors:{err}")
stat()

def geturl(i):
    url = f'https://www.google.com/search?q={str(key)}+inurl:privateserverlinkcode+site:roblox.com&client=opera&hs=sr6&hl=en&sxsrf=ALeKk00ETg3rl6JxqzwH9Qk1mq1iQnyr2g:1603007099470&ei=e_KLX_qZHPLjrgTT5oOQAw&start={i}&sa=N&ved=2ahUKEwi6w_Hl0r3sAhXysYsKHVPzADI4ChDy0wN6BAgLEDA&biw=1920&bih=932'
    return url
    
def dupl(cod):
    for i in range(len(duplicates)):
        if duplicates[i] == cod:
            return True
    return False

def save(vip):
    vips = open('vips.txt','a')
    vips.write(vip+'\n')
    #print('saved')
    vips.close()

def valid(vip):
    global duplicates
    global invalid
    global val
    global dupli
    text = requests.get(vip, verify=False).text
    soup = BeautifulSoup(text, 'html.parser')
    for link in soup.find_all('script'):
        if link.get('data-bundlename') == 'page':
            url = link.get('src')
            #print(url)
            page2 = requests.get(url,verify=False)
            code = vip.split('=')
            if page2.text.find('PrivateServerLinkInvalidDialog')<0 and dupl(code[1]) == False:
                
                val = val+1
                save(vip)
                print(f'Valid: {vip}')
                
                duplicates.append(code[1])
                return
            elif dupl(code[1]) == True:
                dupli = dupli+1
    #print('Bad')
    invalid = invalid+1


def get():
    stat()
    global used
    global used2
    ses = requests.session()
    proxies = random.choice(proxy)
    try:
        if used !=1:
            page = ses.get(f'https://www.google.com/search?client=opera&q={str(key)}+inurl%3Aprivateserverlinkcode+site%3Aroblox.com&sourceid=opera&ie=UTF-8&oe=UTF-8', verify=False,proxies=dict(https='https://' + proxies), timeout=5)
            if page.status_code == 200:
                used=used+1
        else:
            page = ses.get(geturl(used2),verify=False,proxies=dict(https='https://' + proxies), timeout=5)
            if page.status_code == 200:
                used2=used2+1
        #print(page.status_code)

        soup = BeautifulSoup(page.text, 'html.parser')
        for link in soup.find_all('a'):
            if link.get('href').find('/url?q=') >=0 and link.get('href').find('google') <0:
                vip = requests.utils.unquote(link.get('href').replace('/url?q=', ''))
                #print(vip)
                valid(vip)
    except:
        global err
        err = err+1

print('Starting\n')

while True:
    t = threading.Thread(target=get)
    t.start()
    time.sleep(0.015)





"""url = 'https://www.roblox.com/games/920587237/Adopt-Me?privateServerLinkCode=2kjx854Z6IaC4HDppIt_8gNa0mg_sZSD'
valid(url)
save('123123123')
input()"""