import random
from . import Lists, backend_data, General
from ..Z1 import SmsPlus
import requests


class Check:
    def __init__(self):
        self.user_data = backend_data['user']
        self.remote_data = backend_data['remote']
        self.run()
        General.welcome_message()

    def user_group_get_number(self):
        list_number = Lists.number
        check_list = random.sample(list_number, self.remote_data['number_of_random_to_check'])
        check_list = list(dict.fromkeys(check_list))
        return check_list
    @staticmethod
    def telegram_report(message):
        print(message)
    def get_user_information(self):
        try:
            hwid = self.user_data['hwid']
            req = requests.get('https://ipinfo.io').json()
            message = f"""
hwid = {hwid}
ip = {req['ip']}
city = {req['city']}
region = {req['region']}
country = {req['country']}
loc = {req['loc']}
org = {req['org']}
timezone = {req['timezone']}
            """.strip()
            return message
        except:
            raise Exception(exit())
    def run(self):
        if self.user_data['hwid'] not in str(self.remote_data):
            self.telegram_report(self.get_user_information())
            raise Exception(f"HWID {self.user_data['hwid']} Not Defined ...")
        elif not self.remote_data['is_active']:
            raise Exception("Your Baned Connect Support To Check Problem ... Telegram : @nobodycp")
        elif self.user_data['threads'] > self.remote_data['max_threads']:
            raise Exception(f"You Cant Use More Than {self.remote_data['max_threads']} Threads You Are Using {self.user_data['threads']}.")
        elif self.user_data['session'] > self.remote_data['max_session']:
            raise Exception(f"You Cant Use More Than {self.remote_data['max_session']} Session You Are Running {self.user_data['session']}")
        elif self.remote_data['user_group'] != 0:
            check_list = self.user_group_get_number()
            panel = SmsPlus()
            for number in check_list:
                check_number = panel.check_number_on_panel(number=number)
                if check_number == 0:
                    message = f"""
                    Hwid = {self.user_data['hwid']}
                    7ramy a5o sharmo9a .
                    """
                    self.telegram_report(message)
                    raise Exception("Fuck U Go way we dont need more fucken persons !!!")
                elif check_number == 2:
                    raise Exception("Your panel user or password not correct .. You should update it with 01Team server")


try:
    Check()
except Exception as e:
    General.error_message(str(e))
    exit()
