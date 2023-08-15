import base64
import random
import re
import string
import uuid
import names
import phonenumbers
from phonenumbers import carrier, timezone
import pycountry
import requests
from phone_iso3166.country import phone_country
from urllib.parse import unquote
from . import Lists

class Options:
    user_agents = requests.get("https://pastebin.com/raw/hxqYvBtu").text.split("\n")

    # print("User_Agents")
    @staticmethod
    def phone_number(phone_number_) -> dir():
        phone_number_ = f"+{phone_number_.replace('+', '')}"
        try:
            pn = phonenumbers.parse(phone_number_)
            number_without_prefix = pn.national_number
            # country_code_name = region_code_for_country_code(pn.country_code)
            country_code_prefix = pn.country_code
            country = pycountry.countries.get(alpha_2=phone_country(phone_number_))
            alpha_2 = phone_country(phone_number_)
            national_f = phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            number_with_zero = phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.NATIONAL)
            ro_number = phonenumbers.parse(phone_number_, alpha_2)
            carrier_name = carrier.name_for_number(ro_number, "en")
            time_zone = timezone.time_zones_for_number(ro_number)
            # carrier = carrier.name_for_number(sac, "en")
            if country_code_prefix == 383:
                data = {
                    "prefix": country_code_prefix,
                    "local": number_without_prefix,
                    "national": national_f,
                    "zero": number_with_zero,
                    "alpha_2": alpha_2,
                    "alpha_3": 'XXK',
                    "carrier": carrier_name,
                    "name": 'Kosovo',
                    "full": phone_number_,
                    "time_zone": time_zone,
                }
                return data
            else:
                data = {
                    "prefix": country_code_prefix,
                    "local": number_without_prefix,
                    "national": national_f,
                    "zero": number_with_zero,
                    "alpha_2": alpha_2,
                    "alpha_3": country.alpha_3,
                    "carrier": carrier_name,
                    "name": country.name,
                    "full": phone_number_,
                    "time_zone": time_zone,
                }
                return data
        except Exception as e:
            open('Logs.txt', 'a').write(f'{e} ----> Options File Error in phone_number fun : {phone_number_}\n')
            raise TypeError(f'Options File Error in phone_number fun : {phone_number_}\n')
    @staticmethod
    def random_device_id() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def parse_text(text: str, before: str, after: str) -> str:
        return re.search(f'{before}(.*?){after}', text).group(1)
    @staticmethod
    def names(sex: str = None) -> dir(): # type: ignore
        if sex is None:
            sex = random.choice(('male', 'female'))
        if sex == 'male':
            title = 'Mr'
        else:
            title = 'Ms'
        last_name = names.get_last_name()
        first_name = names.get_first_name((str(sex)))
        full_name = f'{first_name} {last_name}'
        return {'title': title, 'full_name': full_name, 'first_name': first_name, 'last_name': last_name,
                'sex': str(sex)}

    @staticmethod
    def email(domain: str = 'gmail.com') -> str:
        round_ = ['_', '.', '', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        gen = round_[random.randrange(len(round_))].strip().lower()
        login = names.get_full_name().replace(' ', gen).lower().strip()
        email = login + f'@{domain}'
        return email
    @staticmethod
    def randoms(num: int) -> str:
        return ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(int(num)))
    def random_user_agent(self) -> str:
        ua = str(self.user_agents[random.randrange(len(self.user_agents))]).strip()
        return ua
    @staticmethod
    def header_parse(headers_: str) -> dir(): # type: ignore
        headers = {}
        for i in headers_.strip().split('\n'):
            i = i.strip()
            try:
                key = i.split(': ')[0]
                value = i.split(': ')[1]
                # print(f'{key} {value}')
                headers[f'{key.lower()}'] = f'{value}'
            except:
                pass
        return headers
    @staticmethod
    def payload_parse(payloads_: str) -> dir(): # type: ignore
        decode = unquote(unquote(payloads_))
        payloads = {}
        try:
            for i in decode.split('&'):
                key = i.split('=')[0]
                value = i.split('=')[1]
                payloads[f'{key}'] = f'{value}'
        except:
            pass
        return payloads
    @staticmethod
    def image_to_base64(image):
        return base64.b64encode(image).decode()
    @staticmethod
    def proxy():
        proxy_list = Lists.proxy
        return proxy_list[random.randrange(len(proxy_list))].strip()
