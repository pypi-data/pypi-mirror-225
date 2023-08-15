import random
import time
from colorama import Style, Fore
from pystyle import *
from . import userdata


class Lists:
    def __init__(self):
        self.proxy = self._proxy()
        self.number = self._number()
    @staticmethod
    def _proxy(settings_proxy_list_name=userdata['Proxy.list']):
        try:
            with open(settings_proxy_list_name) as proxylist:
                # print("Open proxy")
                proxylist = proxylist.readlines()
            return proxylist
        except Exception as e:
            raise Exception(f"proxy.txt Have error ---> {e}")

    @staticmethod
    def _number(list_name=userdata['Number.list'], random_=userdata['Number.list.randomize']):
        try:
            with open(list_name) as list_:
                list_ = list_.readlines()
                if random_:
                    list_ = random.sample(list_, len(list_))
                    return list(map(lambda s: s.strip(), list_))
                else:
                    return list(map(lambda s: s.strip(), list_))
        except Exception as e:
            raise e

Lists = Lists() # type: ignore
class General:
    @staticmethod
    def welcome_message():
        # print(f"{Fore.GREEN}{Back.RED}{Style.DIM}Hello")
        name = userdata['Name']
        _Hello = Box.Lines(f'Welcome ⚡ {name}\nCoded By : 01 Team', pepite=' 💀 ')
        # ✅ ❌ 💲❗❓
        color = Colors.all_colors[random.randrange(0, len(Colors.all_colors))]
        Write.Print(_Hello, color, interval=0.02)

    @staticmethod
    def error_message(message, timeout=10):
        color = Colors.all_colors[random.randrange(0, len(Colors.all_colors))]
        Write.Print(message + '❗', color, interval=0.1)
        time.sleep(int(timeout))

class ProcessBar:
    Successfully = 0
    Retry = []
    Failed = 0
    Bad = []
    counter = 0
    total = len(Lists.number)

    def print_res(self):
        # print(f"This is {Fore.GREEN}color{Style.RESET_ALL}!")
        print(
            f"{Style.RESET_ALL}\r [ {self.counter} From {self.total}] | {Fore.GREEN}🗸 {self.Successfully}{Style.RESET_ALL} | "
            f"{Fore.RED}✘ {len(self.Bad)}{Style.RESET_ALL} | "
            f"{Fore.YELLOW + Style.BRIGHT}♺ {len(set(self.Retry))}{Style.RESET_ALL} ", end='')
        # print(retry)
    def save_bad_data(self):
        with open('bad_retry.txt', 'a') as bad_data:
            for bad in self.Bad:
                bad_data.write(f'{bad}\n')
            bad_data.close()

    def check_bad(self, data):
        if data in self.Bad: return 1
        elif self.Retry.count(data) >= 5:
            self.Bad.append(data)
            self.Failed += 1
            try:
                self.Retry.remove(data)
                self.Retry.remove(data)
                self.Retry.remove(data)
                self.Retry.remove(data)
                self.Retry.remove(data)
            except:
                pass
            return 1
        else: return 0