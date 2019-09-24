import requests
import pandas
import bs4
import re
import time
import json
import pandas as pd
import time
import sys
import numpy as np

user_agent_list = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]
user_agent_list_mobile = [\
    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1',
    'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 7.0; SM-A310F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36 OPR/42.7.2246.114996',
    'Opera/9.80 (Android 4.1.2; Linux; Opera Mobi/ADR-1305251841) Presto/2.11.355 Version/12.10',
    'Opera/9.80 (J2ME/MIDP; Opera Mini/5.1.21214/28.2725; U; ru) Presto/2.8.119 Version/11.10',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) OPiOS/10.2.0.93022 Mobile/11D257 Safari/9537.53',
    'Mozilla/5.0 (Android 7.0; Mobile; rv:54.0) Gecko/54.0 Firefox/54.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) FxiOS/7.5b3349 Mobile/14F89 Safari/603.2.4',
    'Mozilla/5.0 (Linux; U; Android 7.0; en-US; SM-G935F Build/NRD90M) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/11.3.8.976 U3/0.8.0 Mobile Safari/534.30"',
    'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 5.1.1; SM-N750K Build/LMY47X; ko-kr) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Puffin/6.0.8.15804AP',
    'Mozilla/5.0 (Linux; Android 5.1.1; SM-N750K Build/LMY47X; ko-kr) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Puffin/6.0.8.15804AP',
    'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G955U Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 6.0; Lenovo K50a40 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.137 YaBrowser/17.4.1.352.00 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; U; Android 7.0; en-us; MI 5 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.0.3',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows Phone 8.0; Trident/6.0; IEMobile/10.0; ARM; Touch; Microsoft; Lumia 950)',
    'Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.14977',
    'Mozilla/5.0 (BB10; Kbd) AppleWebKit/537.35+ (KHTML, like Gecko) Version/10.3.3.2205 Mobile Safari/537.35+'
]


def get_new_ip():
    print('Getting new IP!')
    order = "d9688431f712b21b42c2f103dca284d4"
    apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + order;
    return {'https': requests.get(apiUrl).content.decode().strip()}

proxy = get_new_ip()
def get_soup(url, user_agent):
    '''URL -> return soup object'''
    global proxy
 
    headers = {
        'User-Agent': user_agent,
    }

    while True:
        try:
            response = requests.get(url, headers = headers, proxies = proxy, timeout = (5, 20))
            response.encoding = 'utf-8'
            soup = bs4.BeautifulSoup(response.text, "lxml")
            if soup.find('p') and 'IP' in soup.find('p').text:
                continue
            else:
                break
        except Exception as e:
            print(e)
            proxy = get_new_ip()
            continue
    return soup

def get_author_info(soup):
    try:
        gender = (soup.find('span', attrs = {'class': 'gender'})['class'])[1]
    except:
        gender = ''
    
    try:
        location = soup.find('div', attrs = {'class': 'loc'}).text
    except:
        location = ''
    
    return gender, location



page = int(sys.argv[1])
all_user = {}
current_url = 'https://www.douban.com/group/345244/discussion?start=' + str((page - 1) * 25)
print(current_url)
start = time.time()

while True:
    # Setup
    idx = np.random.choice(len(user_agent_list))
    user_agent = user_agent_list[idx]
    
    soup = get_soup(current_url, user_agent)
    print('===================')
    print('Getting page:', page)
    
    # Get the replies and post info
    table = soup.find('table', attrs = {'class': 'olt'})
    ##########【可调整参数】#########
    post_num = 1
    while not table:
        idx = np.random.choice(len(user_agent_list))
        user_agent = user_agent_list[idx]
        soup = get_soup(current_url, user_agent)
        table = soup.find('table', attrs = {'class': 'olt'})

    for post in table.children:
        if post == '\n':
            continue
        urls = post.find_all('a')

        print('Getting people:', post_num)
        post_num += 1

        if len(urls) > 0:
            if urls[1].text == '[已注销]':
                continue

            peopleUrl = urls[1]['href']
            if peopleUrl in all_user.keys():
                continue
            idx = np.random.choice(len(user_agent_list_mobile))
            user_agent = user_agent_list_mobile[idx]
            all_user[peopleUrl] = get_author_info(get_soup(peopleUrl, user_agent))
    
    # Check if it's the last page
    if page < 2849:
    	current_url = 'https://www.douban.com/group/345244/discussion?start=' + str(page * 25)
    else:
        result = {'Gender': list(map(lambda x: all_user[x][0], all_user)), 
                 'Location': list(map(lambda x: all_user[x][1], all_user))}
        tmp_df = pd.DataFrame(result)
        tmp_df = tmp_df.loc[tmp_df.apply(lambda s: s['Gender'] != '' and s['Location'] != '', axis = 1)]
        tmp_df.to_csv('data/user_info_' + str(page) + '.csv')
        all_user = {}
        print('========Done!========')
        break
    if page % 100 == 0:
        result = {'Gender': list(map(lambda x: all_user[x][0], all_user)), 
                 'Location': list(map(lambda x: all_user[x][1], all_user))}
        tmp_df = pd.DataFrame(result)
        tmp_df = tmp_df.loc[tmp_df.apply(lambda s: s['Gender'] != '' and s['Location'] != '', axis = 1)]
        tmp_df.to_csv('data/user_info_' + str(page) + '.csv')
        all_user = {}
    
    page += 1
end = time.time()
print(end - start)
print('========Done!========')