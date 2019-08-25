import sys
import time
import hashlib
import requests
import urllib3
from lxml import etree



def scripts_request_with_xdaili(url,useragent):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    _version = sys.version_info

    is_python3 = (_version[0] == 3)

    orderno = "ZF20198147432HvMNOZ"
    secret = "581f8b0d7868491ca98ee6ac53fd72fd"

    ip = "forward.xdaili.cn"
    port = "80"

    ip_port = ip + ":" + port

    timestamp = str(int(time.time()))
    string = "orderno=" + orderno + "," + "secret=" + secret + "," + "timestamp=" + timestamp

    if is_python3:
        string = string.encode()

    md5_string = hashlib.md5(string).hexdigest()
    sign = md5_string.upper()
    #print(sign)
    auth = "sign=" + sign + "&" + "orderno=" + orderno + "&" + "timestamp=" + timestamp

    #print(auth)
    proxy = {"http": "http://" + ip_port,"https": "https://" + ip_port}
    headers = {
        "Proxy-Authorization": auth,
        "User-Agent": useragent,
    }
    print(proxy)
    print(headers)

    r = requests.get(url, headers=headers, proxies=proxy, verify=False,allow_redirects=False)
    r.encoding='utf8'

    return r.status_code,r.text


