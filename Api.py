import requests
import urllib3
import os.path
from datetime import datetime
from urllib3 import disable_warnings


def printmsg(msg):
    print(f"{str(datetime.now())[:-7]}\t{msg}")


session = requests.session()
path = os.path.split(os.path.realpath(__file__))[0]
if os.path.exists(path + "/jwt"):
    printmsg("cookie存在")
    with open(path + "/jwt", "r") as f:
        jwt = f.read()
else:
    jwt = input("请输入authorization(格式为Bearer zxcmzxncwqe):")

session.headers = {
    "User-Agent": "BiyaWallet/2.2.71 (iPhone; iOS 16.4.1; Scale/3.00)",
    "Authorization": jwt
}
urllib3.disable_warnings()
urls = {
    "api-wtrading": "https://api-wtrading.biya.in",
    "api-wuser": "https://api-wuser.biya.in",
    "api-se": "https://api-se.biya.in"
}

apis = {
    "自选股": "/v1/stock/followList?lang=en-us",
    "卖出直到取消": "/v1/security/limitOrder",
}


def follow_list(session):
    '''
    @:param: requests.session
    查看当前自选股
    '''
    res = session.post(f'{urls["api-wtrading"]}{apis["自选股"]}', verify=False, json={
        "language": "en-us",
        "listRows": "20",
        "lang": "en-us",
        "type": 3,
        "page": "1"
    })
    res_status = res.json()
    # print(res_status)
    if res_status["code"] != 200:
        return False
    return True


def sell_until_cancel(session):
    res = session.post(f"{urls['api-wtrading']}{apis['卖出直到取消']}", json={
        "quantity": "1",  # 数量
        "limit_price": "50.0000",  # 卖出价格
        "order_type": "LMT",
        "security_name": "英特尔,Intel Corp.",
        "symbol": "INTC",
        "action": "SELL",
        "language": "zh-cn"
        ,"lang": "zh-cn",
        "symbol_type": "1",
        "order_expired_flag": "GTC",  # 可选DAY，GTC
        "currency": "USD",
        "outside_rth": 1
    }, verify=False)
    res_status = res.json()
    printmsg(res_status["msg"])


def run(session):
    if follow_list(session):
        with open(path + "/jwt", "w") as f:
            f.write(jwt)
        sell_until_cancel(session)
    else:
        printmsg("jwt不正确，退出")




if __name__ == "__main__":
    run(session)