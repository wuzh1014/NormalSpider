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
        self.rlink = redis.StrictRedis(host=Tool.service_ip, port=6479, db=0, password='fuck-u-ass-hole-guy')
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
        self.rlink.setex(response.spider_name + 'living', 1, 10)
        response.pipe = self.rlink.pipeline()
        response.pipe.multi()

    def parse(self, response):
        response.spider_name = AoiSpider.redis_name
        AoiSpider.deal_domain(response)

        self.rlink.setex(response.spider_name + 'been_url:' + response.url, 1, self.day_time * 1)
        if response.page_domain == 'iguba.eastmoney.com':
            response.is_target = True

            if self.avg_size == 0:
                self.avg_size = len(response.body)

            if len(response.body) < int(self.avg_size / 2):
                print('wasted' + response.url)
                sys.exit(2)
            else:
                self.avg_size = (len(response.body) + self.avg_size) / 2

            body_md5 = hashlib.md5(response.body).hexdigest()
            content_pre = response.spider_name + 'cache_content:' + response.url
            pre_md5 = self.rlink.get(content_pre)
            if pre_md5 == body_md5:
                return
            else:
                self.rlink.set(content_pre, body_md5)
        else:
            response.is_target = False

        if not AoiSpider.init_check(response):
            return
        self.init_parse(response)
        if not self.extract_url(response):
            return
        print('clean_extract_word')
        if not SpiderUtil.clean_extract_word(response):
            return
        print('parse_date')
        if not AoiSpider.parse_date(response):
            return