import json
import os

import requests as req
import base64
import ddddocr
import flask

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
}

ocr = ddddocr.DdddOcr()

app = flask.Flask(__name__)


def get_init_cookie(ss: req.Session):
    url = "https://tagss03.pro/"
    res = ss.get(url, headers=headers)
    return res


def get_captcha_code(ss):
    url = "https://tagss03.pro/api/v1/passport/comm/getCaptchaCode"
    res = ss.get(url, headers=headers)
    return res.json()


def login(ss, data):
    url = "https://tagss03.pro/api/v1/passport/auth/login"
    res = ss.post(url, headers=headers, data=data)


def get_subscribe(ss):
    url = "https://tagss03.pro/api/v1/user/getSubscribe"
    res = ss.get(url, headers=headers)
    return res.json()


@app.route("/get_info")
def get_info():
    ss = req.Session()
    if "cookies.json" in os.listdir("./"):
        with open("cookies.json", "r") as f:
            cookies = json.load(f)
        ss.cookies.update(cookies)

    if "message" in get_subscribe(ss).keys():
        print("未登录或登陆已过期")
        get_init_cookie(ss)

        while True:
            res = get_captcha_code(ss)
            client = res["client"]
            img = res["captcha"]
            img = img.replace("data:image/jpeg;base64,", "")
            img = base64.b64decode(img)

            code = ocr.classification(img)
            if len(code) == 4:
                break

        data = {
            'email': 'xxxxxxxxxxx',
            'password': 'xxxxxxxxxxx',
            'captcha_code': code,
            'client': client
        }
        login(ss, data)

    data = get_subscribe(ss)
    cookies = ss.cookies.get_dict()
    with open("cookies.json", "w") as f:
        json.dump(cookies, f)

    total = data['data']['transfer_enable'] / 1024 / 1024 / 1024
    used = data['data']['u'] + data['data']['d']
    used = (used / 1024 / 1024 / 1024)
    used = round(used, 2)
    # 剩余百分比
    left = (total - used) / total * 100
    left = round(left, 2)
    return {
        "total": total,
        "used": used,
        "left": left,
        "update": round(data['data']['u'] / 1024 / 1024 / 1024, 2),
        "download": round(data['data']['d'] / 1024 / 1024 / 1024, 2),
    }


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001)
