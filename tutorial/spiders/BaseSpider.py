# coding:utf-8
import sys
import redis
import json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from tutorial.spiders.scrapy.spiders import ExRedisSpider
from tutorial.spiders.Tool import Tool
import re
sys.path.append("./")
sys.path.append("../../")


class BaseSpider(ExRedisSpider):
    name = "BaseSpider"

    default_url = 'http://guba.eastmoney.com'
    day_time = 86400
    rules = (
        Rule(LinkExtractor(), callback='parse_err', follow=True),
    )

    def parse(self, response):
        pass

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = [_f for _f in domain.split(',') if _f]
        super(BaseSpider, self).__init__()

    @staticmethod
    def extract_json_data(response):
        json_data = re.compile('var itemdata =([\s\S]*?)"me":"').search(response.body)
        if json_data:
            json_data = json_data.group(1) + '"me":""}'
            json_data = json.loads(json_data)
            response.json_data = json_data
            return json_data

    @staticmethod
    def extract_person_url(response):
        if not hasattr(response, 'all_url'):
            response.all_url = []
        if response.json_data:
            for item in response.json_data.get('re'):
                merge_url = 'http://guba.eastmoney.com/news,' + str(item.get('post_guba').get('stockbar_code')) + ',' + str(item.get('post_id')) + '.html'
                response.all_url.append(merge_url)

    @staticmethod
    def extract_normal_url(response):
        if not hasattr(response, 'all_url'):
            response.all_url = []
        response.all_url.extend(response.xpath('//a[contains(@href, "/") and not(contains(@href, "java"))]'))
        all_url = []
        for al in response.all_url:
            url = al.xpath('@href').extract()[0]
            all_url.append(url)
        response.all_url = all_url

    @staticmethod
    def init_check(response):
        if response is None or not hasattr(response, 'xpath'):
            return False
        try:
            if response.is_target:
                BaseSpider.extract_json_data(response)
                BaseSpider.extract_person_url(response)
            else:
                BaseSpider.extract_normal_url(response)
        except Exception as e:
            print('response has no text')
            print(e)
            print(response)
            return False
        return True

