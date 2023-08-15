import configparser
import subprocess
import requests
import wmi
import win32console
import win32gui
c = wmi.WMI()


class Data:
    def __init__(self):
        self.user_data = {}
        self.backend_data = {'remote': {}, 'user': {}}
        self.run()

    def run(self):
        self.terminal()
        self.user_data['hwid'] = self.hwid()
        self.user_data['session'] = self.session()
        self.append_file_data()
        self.backend_data['remote'] = self.remote_data(self.user_data['Root.key'], self.user_data['hwid']) # type: ignore
        self.fix_backend_data()

    def fix_backend_data(self):
        try:
            self.backend_data['user']['hwid'] = self.user_data['hwid']
            self.backend_data['user']['session'] = self.user_data['session']
            self.backend_data['user']['threads'] = self.user_data['01Team.threads']
            self.user_data['Name'] = self.backend_data['remote']['full_name']
            self.backend_data['remote'].pop('id')
            self.backend_data['remote'].pop('email')
            self.backend_data['remote'].pop('created_at')
            self.backend_data['remote'].pop('updated_at')
            numbers = ['max_threads', 'max_session', 'number_of_random_to_check', 'user_group']
            for key, value in self.backend_data['remote'].items():
                if key in numbers:
                    self.backend_data['remote'].update({f'{key}': int(value)})
            self.user_data.pop('hwid')
            self.user_data.pop('session')
            self.user_data.pop('Root.key')
        except Exception:
            pass

    def append_file_data(self):
        file_cfg = self.read_config_file()
        for section in file_cfg.sections():
            numbers = ['threads', ]
            true = ['true','1', 'y', 'yes']
            false = ['false','0', 'n', 'no']
            for key, value in file_cfg[f'{section}'].items():
                if value.lower() in true:
                    self.user_data[f'{section}.{key}'] = 1
                elif value.lower() in false:
                    self.user_data[f'{section}.{key}'] = 0
                elif key in numbers:
                    self.user_data[f'{section}.{key}'] = int(value)
                else:
                    self.user_data[f'{section}.{key}'] = value

    @staticmethod
    def read_config_file():
        file_cfg = configparser.ConfigParser()
        file_cfg.read('config.ini')
        return file_cfg

    @staticmethod
    def hwid():
        return str(subprocess.check_output('wmic csproduct get uuid')).split('\\r\\n')[1].strip('\\r').strip()

    @staticmethod
    def session():
        counter = 0
        title = str(win32console.GetConsoleTitle())
        if title.endswith('.exe'):
            code_name = title.split('\\')[-1]
            for process in c.Win32_Process():
                if code_name in str(process.Name):
                    counter += 0.5
        return int(counter)

    @staticmethod
    def terminal():
        title = str(win32console.GetConsoleTitle())
        appname = title.split('\\')[-1]
        block_dev = ['python.exe', 'py.txt']
        if appname not in block_dev:
            if title.endswith('.exe'):
                hwnd = win32gui.GetForegroundWindow()
                win32gui.SetWindowPos(hwnd, 0, 0, 0, 700, 300, 0)

    @staticmethod
    def remote_data(key, hwid):
        payloads = {'key': f'{key}', 'hwID': f'{hwid}'}
        req = requests.post('http://84.32.128.212:8000/api/v1/clients/detail/', json=payloads)
        # print(req.text)
        if hwid in req.text:
            return req.json()


x = Data()
userdata = x.user_data
backend_data = x.backend_data


