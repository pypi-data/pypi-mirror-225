import os
from . import userdata, Lists
import random
import requests
import requests
import zipfile
# import undetected_chromedriver as uc

class Requests:
    proxy_list = Lists.proxy
    def proxy_session(self):
        # print(self.settings_active_proxy)
        s = requests.Session()
        if userdata['Proxy.active']:
            proxy = self.proxy_list[random.randrange(len(self.proxy_list))].strip()
            # print(proxy)
            s.proxies = {
                'http': f'{userdata["Proxy.type"]}://{proxy}',
                'https': f'{userdata["Proxy.type"]}://{proxy}',
            }
            return s
        else:
            return s

# class Selenium:
#     NOPECHA_KEY = userdata['Captcha.nopecha']
#     with open('chrome.zip', 'wb') as f:
#         f.write(requests.get('https://nopecha.com/f/chrome.zip').content)
#     with zipfile.ZipFile('chrome.zip', 'r') as zip_ref:
#         zip_ref.extractall('nopecha')
#     def undetected_chromedriver(self):
#         options = uc.ChromeOptions()
#         # options.add_argument('--no-sandbox')
#         # options.add_argument('--disable-infobars')
#         # options.add_argument('--disable-dev-shm-usage')
#         # options.add_argument('--')
#         # options.add_argument('--disable-blink-features=AutomationControlled')
#         # options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
#         # options.add_argument(f"--load-extension={os.getcwd()}/nopecha")
#         driver = uc.Chrome(options=options)
#         # driver.get(f"https://nopecha.com/setup#{self.NOPECHA_KEY}")
#         return driver