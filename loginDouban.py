import requests

# 生成Session对象，用于保存Cookie
s = requests.Session()


def login_douban(name: str, password: str) -> int:
    """
    login douban
    :return:
    """

    login_url = 'https://accounts.douban.com/j/mobile/login/basic'

    headers = {'user-agent': 'Mozilla/5.0',
               'Referer': 'https://accounts.douban.com/passport/login?source=main'}

    data = {'name': name,
            'password': password,
            'remember': 'false'}
    try:
        r = s.post(login_url, headers=headers, data=data)
        r.raise_for_status()
    except Exception as e:
        print('login in error', e)
        return -1

    print(r.text)
    return 1



if __name__ == '__main__':
    login_douban("username", "password")

