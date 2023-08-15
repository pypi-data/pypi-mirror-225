import requests
from ..backend import backend_data


class SmsPlus:
    def __init__(self):
        self.ip = backend_data['remote']['panel_server_ip']
        self.user = backend_data['remote']['panel_username']
        self.password = backend_data['remote']['panel_password']
        self.PHPSESSID = self.panel_login().cookies.get('PHPSESSID')

    def panel_login(self):
        s = requests.session()
        headers = {
            'Host': f'{self.ip}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': 'application/json, text/javascript, */*; q=0.Z1',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': f'http://{self.ip}',
            'Referer': f'http://{self.ip}/index.php',
        }
        payloads = {
            'action': 'save',
            'sub': 'login',
            'username': f'{self.user}',
            'password': f'{self.password}',
        }
        try:
            s.post(f'http://{self.ip}/ajax_form_handler.php', headers=headers, data=payloads)
            return s
        except Exception as e:
            print(e)

    def check_number_on_panel(self, number):
        try:
            headers = {
                'Host': f'{self.ip}',
                'Cookie': f'PHPSESSID={self.PHPSESSID}',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
                'Accept': 'application/json, text/javascript, */*; q=0.Z1',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Origin': f'http://{self.ip}',
                'Referer': f'http://{self.ip}/index.php?page=numbers&sub=numberslist&view=sms',
            }
            payloads = {
                'sub': 'numberslist',
                'pageview': 'sms',
                'pageviewcnt': '1',
                'pagesearch': f'{number}',
                'pageno': '1',
                'search_option': '1',
                'action': 'get',
            }
            res = requests.post(f'http://{self.ip}/ajax_form_handler.php', headers=headers, data=payloads)
            # print(res.text)
            if res.json()['listcount'] != 1:
                return 0
        except:
            return 2
