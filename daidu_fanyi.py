# 主要破解sign
# pip install PyExecJS
import execjs
import requests
import json


class BaiduInterpret:
    def __init__(self, word):
        self.url_detect = "https://fanyi.baidu.com/langdetect"
        self.url_interpret = "https://fanyi.baidu.com/v2transapi?from={}&to={}"
        self.word = {"query": word}

        self.header = {'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
         'Cookie':'BIDUPSID=C6DC93E3AF28F5F0CE5E7FC86B3F437D; PSTM=1606876036; BAIDUID=C6DC93E3AF28F5F0206A08F93EFD5C99:FG=1;'
            }

    def sign(self):
        with open("./signJS.js", "r", encoding="utf8") as f:
            js = f.read()
        return execjs.compile(js).call("e", self.word["query"])

    def request(self, url, data):
        res = requests.post(url, headers=self.header, data=data)
        return json.loads(res.content.decode())

    def run(self):
        # check 语种
        res1 = self.request(url=self.url_detect, data=self.word)
        if res1["lan"] == "zh":
            self.url_interpret = self.url_interpret.format("zh", "en")
        else:
            self.url_interpret = self.url_interpret.format("en", "zh")

        # translate
        print(self.word["query"])

        data_for_trans = {
            "query": self.word["query"],
            "simple_means_flag": " 3",
            "sign": self.sign(),
            "token": "d24dcef9e8c77e6201a15ef997226090",
            "domain": "common",
        }
        res2 = self.request(self.url_interpret, data=data_for_trans)
        print(dict(res2['trans_result']['data'][0])["dst"])




if __name__ == '__main__':
    word = input("请输入您要查找的单词：")
    fanyi = BaiduInterpret(word)
    fanyi.run()