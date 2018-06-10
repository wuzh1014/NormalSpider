# coding:utf-8
import threading
import time
import pdb
import time
import dateutil.parser as dateparser

class Tool:
    service_ip = '35.194.116.91'
    group_analysis_flag = True
    learning_trend_flag = True
    lock = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def check_contain_chinese(check_str):
        for ch in check_str:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False

    @staticmethod
    def go_log(context, log_type=None):
        global lock
        lock.acquire()
        try:
            f = None
            if log_type == 'ERROR':
                # f = open("/data/aoi_error.log", "a+")
                f = open("D:/aoi_error.txt", "a+")
            else:
                # f = open("/data/aoi_log.log", "a+")
                f = open("D:/aoi_log.txt", "a+")
            f.write(str(context))
            f.write('\n')
            f.close()
        finally:
            lock.release()

    @staticmethod
    def split_at_point(this_string, mark_points):
        items = []
        last_point = 0
        for i in range(len(mark_points)):
            items.append(this_string[last_point:mark_points[i]])
            last_point = mark_points[i]
        items.append(this_string[last_point:])
        return items

    @staticmethod
    def compare_len(pure_string, p, q, word_map):
        j = 0
        # charge chi and eng
        # stop at split
        while j < len(pure_string[p:]) - 1 and j < len(pure_string[q:]) - 1 \
                and pure_string[p:][j] == pure_string[q:][j]:
            if pure_string[p:][j] == ',':
                break
            j += 1
        if j > 2:
            try:
                value = word_map.get(pure_string[q:q + j])
                if value:
                    word_map[pure_string[q:q + j]] = value + 1
                else:
                    word_map[pure_string[q:q + j]] = 1
            except:
                pdb.set_trace()

    @staticmethod
    def ajust_date(clean_list, data_list):
        clean_date = []
        for i in range(len(clean_list)):
            clean_offset = clean_list[i][1]
            match_index = 0
            min_dif = abs(int(data_list[match_index][3]) - int(clean_offset))
            for x in range(len(data_list)):
                com_dif = abs(int(data_list[x][3]) - int(clean_offset))
                if com_dif < min_dif:
                    match_index = x
                    min_dif = com_dif
            clean_date.append(data_list[match_index])
        return clean_date

    @staticmethod
    def date_to_string(clean_date):
        string_date_list = []
        for i in range(len(clean_date)):
            join_date = ''.join(clean_date[i][0:3])
            string_date_list.append(join_date)
        return string_date_list

    @staticmethod
    def get_cur_time_int(cur_time):
        cur_time_str = [str(item) for item in cur_time]
        cur_time_parse = int(''.join([cur_time_str[0], (len(cur_time_str[1]) > 1 and cur_time_str[1] or '0' + cur_time_str[1]),
                                      (len(cur_time_str[2]) > 1 and cur_time_str[2] or '0' + cur_time_str[2])]))
        return cur_time_parse

    @staticmethod
    def get_today_string():
        cur_time = time.localtime()
        cur_time_num = str(cur_time[0])
        if cur_time[1] < 10:
            cur_time_num += '0'
        cur_time_num += str(cur_time[1])
        if cur_time[2] < 10:
            cur_time_num += '0'
        cur_time_num = cur_time_num + str(cur_time[2])
        return cur_time_num

    @staticmethod
    def parse_date(time_str):
        dt = dateparser.parse(time_str)
        # time.mktime(dt.timetuple())
        return dt


if __name__ == "__main__":
    pass