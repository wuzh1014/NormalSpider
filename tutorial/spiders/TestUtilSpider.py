# coding:utf-8
import unittest
from tutorial.spiders.BaseSpider import *
from tutorial.spiders.AoiSpider import *
from tutorial.spiders.Tool import Tool
from tutorial.spiders import SiteContent
from lxml import etree
import urllib.request


class TestUtilSpider(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_redis(self):
        pool = redis.ConnectionPool(host=Tool.service_ip, port=6479, password='fuck-u-ass-hole-guy')
        self.rlink = redis.StrictRedis(connection_pool=pool)
        self.rlink.setex('justTest', 20, 233)
        value = self.rlink.get('justTest').decode()
        print(value)
        assert value == '233'
        return True

    def test_check_contain_chinese(self):
        test_str = '12312的3123'
        print(Tool.check_contain_chinese(test_str))
        test_str = '123123123'
        print(Tool.check_contain_chinese(test_str))
        test_str = '阿达达阿斯达'
        print(Tool.check_contain_chinese(test_str))
        return True

    def test_clean(self):
        test_str = '123123123'
        print(SpiderUtil().clean_extract_word(test_str))
        return True

    def test_return_freq_word(self):
        test_str = 'asdaaa,aaa,aaa,aaa,aaa,aaaaaaaaaa'
        print(SpiderUtil().return_freq_word(test_str))
        return True

    def test_trans_json(self):
        self.body = SiteContent.html_str
        self.strBody = self.body
        self.all_url = {}
        BaseSpider.extract_json_data(self)
        BaseSpider.extract_person_url(self)
        print(self.all_url)
        input_list = AoiSpider.format_item_list(self)
        print(input_list)

    def test_trans_date(self):
        time_str = '2018-05-26 10:22:00'
        dt = Tool.parse_date(time_str)
        print(dt)

    def test_whole_trans(self):
        self.url = SiteContent.html_url
        self.body = SiteContent.html_str
        self.xpath = etree.HTML(self.body)
        self.spider_name = AoiSpider.redis_name
        AoiSpider().parse(self)

    def test_one_trans(self):
        self.url = 'http://iguba.eastmoney.com/6712111507146464'
        res = urllib.request.urlopen(self.url)
        self.body = res.read().decode('utf-8')
        self.xpath = etree.HTML(self.body)
        self.spider_name = AoiSpider.redis_name
        AoiSpider().parse(self)

    # self.assertTrue(isinstance(d, dict))
    # self.assertEquals(d['key'], 'value')
    # self.assertRaises(KeyError)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(TestUtilSpider('test_whole_trans'))
    unittest.TextTestRunner(verbosity=2).run(suite)
    # unittest.main()