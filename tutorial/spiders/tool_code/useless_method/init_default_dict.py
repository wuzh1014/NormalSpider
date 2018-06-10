# coding:utf-8
# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import redis


default_dict = ['你'
                ,'我','他','她','它','是','不是','有','给','把'
                ,'拿','做','作','收获','购买','股市','商家','商品','购物'
                ,'男人','女人','老人','小孩','政府','官员','生活','费用','政策'
                ,'雾霾','北京','上海','广州','深圳','工作','工资','小学','高中'
                ,'大学','幼儿园','利息','贷款','讲话','说','打开','收藏','发票'
                ,'字典','单词','百姓','人民','顾客','学生','编程','工人','程序员'
                ,'代码','速度','效率','豪车','赌博','世界','金钱','美女','房子'
                ,'美食','吃','喝','玩','快乐','痛苦','投资','手机','科技'
                ,'莫斯科','中国','国家','美国','日本','德国','澳大利亚','韩国','朝鲜'
                ,'武装','设备','足球','女孩','妹子','广告','腾讯','360','谷歌'
                ,'网易','游戏','美媒','国内','媒体','岁','年','今年','明年'
                ,'收入','手机','海外','创业','士兵','进口','出口','打','问'
                ,'回答','提问','道路','交通','慈善','发表','言论','表示','疑问'
                ,'如何','称','网友','网络','好处','博客','微博','新浪','阿里'
                ,'马云','医药','人','要','不要','发现','话题','迪拜','台湾'
                ,'独立','发生','制止','好评','体育','娱乐','新闻','教育','汽车','专业','马尔代夫','东南'
                ,'广东']
def init_default_dict(pipe):
    for x in range(len(default_dict)):
        set_str = 'dict:' + default_dict[x]
#         pipe.setex(set_str, 1, 1000000000)
        pipe.set(set_str, 1)
    pipe.execute()
    
if __name__ == "__main__":
    global service_ip
    rlink = redis.StrictRedis(host=service_ip, port=6479, db=0, password='fuck-u-ass-hole-guy')
    pipe = rlink.pipeline()
    pipe.multi()
    init_default_dict(pipe)
    print('finish')