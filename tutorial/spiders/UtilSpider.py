# coding:utf-8
from purl import URL
import pdb
from tutorial.spiders.BaseSpider import BaseSpider
from tutorial.spiders.Tool import Tool
from tutorial.spiders.SpiderUtil import SpiderUtil


class UtilSpider(BaseSpider):
    def parse(self, response):
        pass

    def extract_url(self, response):
        if len(response.all_url) > 0:
            get_domain_list = []
            get_url_list = []
            for url in response.all_url:
                if not url:
                    continue
                end_fix = url[-4:len(url)]
                if '.jpg.png.gif.rar.zip.doc.pdf.css'.find(end_fix) != -1:
                    continue
                opt = URL(url)
                url_domain = opt.domain()
                if not url_domain:
                    url = response.page_prefix + '/' + url
                    url_domain = response.page_domain
                elif not opt.scheme():
                    url = 'http://' + url
                if url_domain.find('eastmoney') == -1:
                    continue
                response.pipe.get(response.spider_name + 'been_url:' + url)
                get_domain_list.append(url_domain)
                get_url_list.append(url)

            for url_domain in get_domain_list:
                response.pipe.get(response.spider_name + 'ban_host:' + url_domain)

            get_urlex_dmexp_list = response.pipe.execute()
            adv_len = len(get_url_list)
            if len(get_urlex_dmexp_list) == 0 or len(get_urlex_dmexp_list) != adv_len + len(get_domain_list):
                return
            for index in range(len(get_url_list)):
                url = get_url_list[index]
                exist_flag = get_urlex_dmexp_list[index]
                if exist_flag:
                    continue
                is_ban_host = get_urlex_dmexp_list[index + adv_len]
                if is_ban_host:
                    continue

                response.pipe.lpush(self.redis_key, url)
            response.pipe.execute()
        return True

    @staticmethod
    def format_item_list(response):
        input_list = []
        if hasattr(response, 'json_data'):
            for item in response.json_data.get('re'):
                date_str = str(item.get('post_publish_time'))
                post_content = str(item.get('post_content'))
                user_id = str(item.get('post_user').get('user_id'))
                post_date = Tool.parse_date(date_str)
                date_key = date_str.split(' ')[0].replace('-', '')
                input_list.append((date_key, user_id, post_content))
        return input_list

    @staticmethod
    def parse_date(response):
        input_list = UtilSpider.format_item_list(response)
        date_map = {}
        for item in input_list:
            response.pipe.hset(response.spider_name + 'content_map:' + item[0], item[1], item[2])
            date_map[item[0]] = 1
        for date in date_map:
            response.pipe.zadd(response.spider_name + 'date_list', int(date), date)
            response.pipe.hdel(response.spider_name + 'analysed_date', date)
        response.pipe.execute()
        return True
