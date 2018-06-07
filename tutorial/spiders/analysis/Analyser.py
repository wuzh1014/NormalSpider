# coding:utf-8
import threading
import redis
import traceback
import time
import sys
sys.path.append("../../../")
from tutorial.spiders.scrapy.spiders import RedisMixin
from tutorial.spiders.Tool import Tool
from tutorial.spiders.SpiderUtil import SpiderUtil


class Analyser:
    rlink = None
    pipe = None

    date_pointer = 0

    def __init__(self):
        self.rlink = redis.StrictRedis(host=Tool.service_ip, port=6379, db=0)
        pipe = self.rlink.pipeline()
        pipe.multi()

    def do_analysis(self):
        while True:
            try:
                while RedisMixin.site_no_add_content_count == 0:
                    print('RedisMixin 1')
                    time.sleep(1)

                fetch_date = self.rlink.zrange(RedisMixin.name + 'date_list', self.date_pointer, self.date_pointer + 1)
                analysed = self.rlink.hget(RedisMixin.name + 'analysed_date', self.date_pointer)
                if analysed:
                    time.sleep(1)
                    continue
                if fetch_date:
                    self.rlink.hset(RedisMixin.name + 'analysed_date', self.date_pointer, 1)
                    date_str_set = self.rlink.hvals(RedisMixin.name + 'content_map:' + fetch_date)
                    date_str = ','.join(date_str_set)
                    print('cal_most_freq_word')
                    self.cal_most_freq_word(date_str, fetch_date)
                else:
                    self.date_pointer = 0
                    continue
                self.date_pointer += 1
            except Exception as ex:
                print(ex)
                traceback.print_exc()

    def cal_most_freq_word(self, date_str, fetch_date):
        word_map = SpiderUtil.return_freq_word(date_str)
        clean_list = self.clean_with_ban_list(word_map)
        if len(clean_list) == 0:
            return False
        clean_list.sort(key=lambda x: x[1])
        for i in range(len(clean_list)):
            if clean_list[i][1] > 1:
                if Tool.check_contain_chinese(clean_list[i][0]):
                    self.pipe.hincrby(RedisMixin.name + 'freq_count_date:' + str(fetch_date), clean_list[i][0], 1)
        self.pipe.execute()

    def clean_with_ban_list(self, word_map):
        clean_list = []
        for i in word_map:
            self.pipe.get(RedisMixin.name + 'ban_freq_word:' + i)
        ban_list = self.pipe.execute()
        index = -1
        for i in word_map:
            index += 1
            if ban_list[index]:
                continue
            clean_list.append((i, word_map[i]))
        return clean_list

if __name__ != "__main__":
    pass
    # threads = [threading.Thread(target=Analyser().do_analysis(), args=())]
    # threads[0].setDaemon(True)
    # threads[0].start()
    

