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


# Setup
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

# =======================================================================================================================
# 第二部分 - 抓取帖子内容
def get_new_ip():
    print('Getting new IP!')
    order = "d9688431f712b21b42c2f103dca284d4"
    apiUrl = "http://api.ip.data5u.com/dynamic/get.html?order=" + order;
    return {'https': requests.get(apiUrl).content.decode().strip()}

access_count = 0
proxy = get_new_ip()
def get_soup(url, user_agent):
    '''URL -> return soup object'''
    # print('Getting soup..')
    global proxy
    global access_count
    access_count += 1
    if access_count > 35:
        proxy = get_new_ip()
        access_count = 0
 
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

def find_last_comment(soup, postUrl):
    '''Soup object -> Last comment time'''
    if soup.find('div', attrs = {'class': 'paginator'}):
        tmp_lst = list(soup.find('div', attrs = {'class': 'paginator'}).find_all('a'))
        new_url = tmp_lst[-2]['href']

        # Setup
        idx = np.random.choice(len(user_agent_list))
        user_agent = user_agent_list[idx]
        tmp_soup = get_soup(new_url, user_agent)
        try: 
            result = (tmp_soup.find_all('span', attrs = {'class': 'pubtime'})[-1].text)
        except:
            result = 'Failed to get info'
        return result
    else:
        try: 
            result = (soup.find_all('span', attrs = {'class': 'pubtime'})[-1].text)
            
        except:
            result = 'Failed to get info'
        return result
    
def find_post_like_n_comment_num(soup):
    '''Soup object -> number of like, number of comment'''
    # print('hi')
    tmp_str = soup.find('script', attrs = {'type': 'application/ld+json'})
    if tmp_str:
        tmp_str = tmp_str.text
        tmp_str = tmp_str.replace('\t', '').replace('\n', '').replace('\\', '')
        try:
            tmp_json = json.loads(str(tmp_str))
        except:
            return 0, 0
        like_num = tmp_json['interactionStatistic']['userInteractionCount']
        comment_num = tmp_json['commentCount']
        # print('hiiii')
        return int(like_num), int(comment_num)
    else:
        # print('hiiii')
        return 0, 0

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

def handle_single_post(soup, postUrl, peopleUrl):
    '''
    Soup object, post url -> Group info dictionary
    给定一个帖子页面，返回这个帖子的内容信息
    '''
    postContent = soup.find("div", attrs={"class":"topic-content clearfix"})
    postComment = soup.find("ul", attrs={"id":"comments", "class":"topic-reply"})

    # [3项]作者姓名、ID、签名、个人地址
    # [5项]内容、图片张数、图片地址列表字符串、作者评论、作者评论个数
    postDetailInfoDict = {}

    # Part.1 帖子基本信息 - 帖子链接、标题、ID、创建时间、最后回复时间、回复个数、喜欢人数
    postDetailInfoDict['postID'] = postUrl.split('/')[-2]
    postDetailInfoDict['postUrl'] = postUrl

    # 帖子标题
    # postTitle
    try: # 查找是否存在长标题的标签并匹配
        postDetailInfoDict['postTitle'] = re.findall('<strong>标题：</strong>(.*)</td><td class="tablerc"></td></tr>', str(postContent))[0]
    except:
        try:
            postDetailInfoDict['postTitle'] = soup.title.text.strip()
        except:
            proxy = get_new_ip()
            idx = np.random.choice(len(user_agent_list))
            user_agent = user_agent_list[idx]
            soup = get_soup(postUrl, user_agent)
            try:
                postDetailInfoDict['postTitle'] = soup.title.text.strip()
            except:
                postDetailInfoDict['postTitle'] = ''
    
    try:
        postDetailInfoDict['postCreateDate'] = str(soup.find("span", attrs={"class":"color-green"}).string).strip()
    except:
        proxy = get_new_ip()
        idx = np.random.choice(len(user_agent_list))
        user_agent = user_agent_list[idx]
        soup = get_soup(postUrl, user_agent)
        try:
            postDetailInfoDict['postCreateDate'] = str(soup.find("span", attrs={"class":"color-green"}).string).strip()
        except:
            postDetailInfoDict['postCreateDate'] = ''
    # print(postDetailInfoDict['postCreateDate'])
    print('Title:', postDetailInfoDict['postTitle'])
    
    # 赞数 & 评论数
    like_num, comment_num = find_post_like_n_comment_num(soup)
    postDetailInfoDict["postLikeNum"] = like_num
    postDetailInfoDict['postCommentNum'] = comment_num

    # # postLastCommentDate
    # if postDetailInfoDict['postCommentNum'] > 0:
    #     postDetailInfoDict['postLastCommentDate'] = find_last_comment(soup, postUrl)
    # else:
    #     postDetailInfoDict['postLastCommentDate'] = postDetailInfoDict['postCreateDate']

    # Part.2
    # 作者姓名、ID、签名、个人地址
    try:
        postDetailInfoDict['postAuthorName'] = re.findall('alt="(.*)" class="pil"', str(postContent))[0]
        postDetailInfoDict['postAuthorUrl'] = re.findall('(https://www\.douban\.com/people/.*/)"><img', str(postContent))[0]
        postDetailInfoDict['postAuthorId'] = re.findall('https://www\.douban\.com/people/(.*)/"><img', str(postContent))[0]
    except:
        proxy = get_new_ip()
        idx = np.random.choice(len(user_agent_list))
        user_agent = user_agent_list[idx]
        tmp_soup = get_soup(postUrl, user_agent)
        try:
            postDetailInfoDict['postAuthorName'] = re.findall('alt="(.*)" class="pil"', str(postContent))[0]
            postDetailInfoDict['postAuthorUrl'] = re.findall('(https://www\.douban\.com/people/.*/)"><img', str(postContent))[0]
            postDetailInfoDict['postAuthorId'] = re.findall('https://www\.douban\.com/people/(.*)/"><img', str(postContent))[0]
        except:
            postDetailInfoDict['postAuthorName'] = ''
            postDetailInfoDict['postAuthorUrl'] = ''
            postDetailInfoDict['postAuthorId'] = ''
    # Part.3 帖子内容
    # 帖子内容、所有评论、评论个数
    postDetailInfoDict['postContent'] = soup.find("div", attrs={"class":"topic-content"}).text.replace("\r", "").replace("\n", "").replace(" ", "")
    
    # print('---Before accessing the author info---')
    # # Setup
    # idx = np.random.choice(len(user_agent_list_mobile))
    # user_agent = user_agent_list_mobile[idx]
    # gender, location = get_author_info(get_soup(peopleUrl, user_agent))
    # postDetailInfoDict['postAuthorGender'] = gender
    # postDetailInfoDict['postAuthorLocation'] = location
    # print('after=====')
    return postDetailInfoDict


def handle_post_replies(soup, postUrl):
    '''
    给定一个帖子，返回这个帖子的所有回复信息（一个dataframe）
    '''
    all_reply = []
    postID = postUrl.split('/')[-2]
    current_url = postUrl
    while True:
        if current_url != postUrl:
            # Setup
            idx = np.random.choice(len(user_agent_list))
            user_agent = user_agent_list[idx]
            soup = get_soup(current_url, user_agent)
        # Get all replies
        if len((soup.find_all('ul', attrs = {'class': 'topic-reply'}))) == 0:
            break
        reply_lst = (soup.find_all('ul', attrs = {'class': 'topic-reply'})[-1].children)
        for reply in reply_lst:
            if reply == '\n':
                continue
            single_reply = {}

            # Post ID
            single_reply['postID'] = postID
            
            # Reply content
            try:
                single_reply['content'] = reply.find('p', attrs = {'class': 'reply-content'}).text
            except:
                continue
            # print(single_reply['content'][:10])
            # Poster id
            single_reply['posterID'] = reply.find('div', attrs = {'class': 'operation_div'})['id']
            
            # Reply time
            single_reply['replyTime'] = reply.find('span', attrs = {'class': 'pubtime'}).text
            
            # Add to all the replies
            all_reply.append(single_reply)

        # Check if it's the last page
        if soup.find('span', attrs = {'class': 'next'}) and soup.find('span', attrs = {'class': 'next'}).a:
            current_url = soup.find('span', attrs = {'class': 'next'}).a.get('href')
        else:
            break
    return pd.DataFrame(all_reply, columns = ['postID', 'posterID', 'replyTime', 'content'])


# =======================================================================================================================
# 第三部分 - 整合所有内容，进行抓取

page = int(sys.argv[1])

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

    data_reply = []
    data_post = []
    
    # Get the replies and post info
    table = soup.find('table', attrs = {'class': 'olt'})
    ##########【可调整参数】#########
    post_num = 1
    if table:
        for post in table.children:
            if post == '\n':
                continue
            urls = post.find_all('a')
            
            if len(urls) > 0:
                postUrl = urls[0]['href']
                # Setup
                idx = np.random.choice(len(user_agent_list))
                user_agent = user_agent_list[idx]
                tmp_soup = get_soup(postUrl, user_agent)
                print('Getting the post:', post_num)
                data_reply.append(handle_post_replies(tmp_soup, postUrl))
                peopleUrl = urls[1]['href']
                data_post.append(handle_single_post(tmp_soup, postUrl, peopleUrl))
                post_num += 1

    # Check if it's the last page
    if soup.find('span', attrs = {'class': 'next'}) and soup.find('span', attrs = {'class': 'next'}).a:
        pd.concat(data_reply).to_csv('data/reply_' + str(page) + '.csv', index = False)
        pd.DataFrame(data_post).to_csv('data/post_' + str(page) + '.csv', index = False)
        current_url = soup.find('span', attrs = {'class': 'next'}).a['href']
        page += 1
    else:
        pd.concat(data_reply).to_csv('data/reply_' + str(page) + '.csv', index = False)
        pd.DataFrame(data_post).to_csv('data/post_' + str(page) + '.csv', index = False)
        print('========Done!========')
        break
    # break
    # if page == 2:
    #     break
end = time.time()
print(end - start)
print('========Done!========')
