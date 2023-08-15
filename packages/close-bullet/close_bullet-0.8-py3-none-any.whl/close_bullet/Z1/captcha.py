import nopecha
from . import userdata
from onest_captcha import OneStCaptchaClient


class Nopecha:
    nopecha.api_key = userdata['Captcha.nopecha']
    @staticmethod
    def text_captcha(image_as_base64):
        try:
            text = nopecha.Recognition.solve(
                type='textcaptcha',
                image_data=[f'{image_as_base64}'],
            )
            return text[0]
        except:
            raise Exception("Nopecha Error")
    @staticmethod
    def reCAPTCHA2(url, key):
        try:
            token = nopecha.Token.solve(
                type='recaptcha2',
                sitekey=f'{key}',
                url=f'{url}',
            )
            print(token)
        except:
            raise Exception("Nopecha Error")
    @staticmethod
    def reCAPTCHA3(url, key, action='check'):
        try:
            token = nopecha.Token.solve(
                type='recaptcha2',
                sitekey=f'{key}',
                url=f'{url}',
                data={
                    'action': f'{action}',
                }
            )
            print(token)
        except:
            return "nopecha Error ...."

class OneStCaptcha:
    client = OneStCaptchaClient(apikey=userdata['Captcha.1st_captcha'])
    def text_captcha(self, image_as_base64):
        try:
            result = self.client.image_to_text(base64img=image_as_base64)
            if result["code"] == 0:  # success:
                # print(result["token"])
                return result['token']
            else:  # wrong
                raise Exception(result['messeage'])
        except Exception as e:
            raise Exception(f"OneStCaptcha ....{e}")
    def reCAPTCHA2(self, url, key, invisible=False):
        try:
            result = self.client.recaptcha_v2_task_proxyless(site_url=url, site_key=key, invisible=invisible)
            if result["code"] == 0:  # success:
                print(result["token"])
            else:  # wrong
                raise Exception(result["messeage"])
        except Exception as e:
            raise Exception(f"OneStCaptcha Error ....{e}")
    def reCAPTCHA3(self, url, key, action='check'):
        try:
            result = self.client.recaptcha_v3_task_proxyless(site_url=url, site_key=key, page_action=action)
            if result["code"] == 0:  # success:
                print(result["token"])
            else:  # wrong
                raise Exception(result["messeage"])
        except Exception as e:
            raise Exception(f"OneStCaptcha Error ....{e}")
