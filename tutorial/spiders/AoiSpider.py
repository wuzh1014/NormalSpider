# coding:utf-8
import sys
import hashlib
import redis
import pdb
from tutorial.spiders.Tool import Tool
from purl import URL
sys.path.append("./")
sys.path.append("../../")
from tutorial.spiders.UtilSpider import UtilSpider
from tutorial.spiders.SpiderUtil import SpiderUtil


class AoiSpider(UtilSpider):
    avg_size = 0

    def __init__(self):
        pool = redis.ConnectionPool(host=Tool.service_ip, port=6479, password='fuck-u-ass-hole-guy')
        self.rlink = redis.StrictRedis(connection_pool=pool)
        super(AoiSpider, self).__init__()

    @staticmethod
    def deal_domain(response):
        opt = URL(response.url)
        page_domain = opt.domain()
        scheme = opt.scheme()
        response.page_domain = page_domain
        response.scheme = scheme
        response.page_prefix = response.scheme + '://' + response.page_domain + '/'

    def init_parse(self, response):
        self.rlink.setex(response.spider_name + 'living', 10, 1)
        response.pipe = self.rlink.pipeline()
        response.pipe.multi()
        response.all_url = {}

    def parse(self, response):
        if type(response.body).__name__ != 'bytes' and type(response.body).__name__ != 'str':
            print('not str body instead of ' + type(response.body).__name__)
            return

        response.strBody = response.body
        if type(response.body).__name__ == 'bytes':
            response.strBody = response.body.decode('utf-8')

        response.spider_name = AoiSpider.redis_name
        AoiSpider.deal_domain(response)
        self.init_parse(response)
        self.rlink.setex(response.spider_name + 'been_url:' + response.url, self.day_time * 1, 1)
        if response.page_domain == 'iguba.eastmoney.com':
            response.is_target = True

            if self.avg_size == 0:
                self.avg_size = len(response.strBody)

            if len(response.strBody) < int(self.avg_size / 2):
                print('wasted' + response.url)
                sys.exit(2)
            else:
                self.avg_size = (len(response.strBody) + self.avg_size) / 2

            body_md5 = hashlib.md5(response.strBody.encode('utf-8')).hexdigest()
            content_pre = response.spider_name + 'cache_content:' + response.url
            pre_md5 = self.rlink.get(content_pre)
            if pre_md5 == body_md5:
                print('same md5')
                return
            else:
                self.rlink.set(content_pre, body_md5)
        else:
            response.is_target = False

        if not AoiSpider.init_check(response):
            print('init_check false')
            return
        if not self.extract_url(response):
            print('extract_url false')
            return
        if hasattr(response, 'json_data'):
            if not AoiSpider.parse_date(response):
                print('parse_date false')
                return
        else:
            print('hasattr not')