# coding:utf-8
import threading
import redis
import traceback
import sys
sys.path.append("../")
from tool import *
# convert date has '-' to without '-'


def temp_format_stock_data():
    global service_ip
    rlink = redis.StrictRedis(host=service_ip, port=6479, db=0)
    pipe = rlink.pipeline()
    pipe.multi()
    try:
        pipe.lrange('stock_list_code', 0, -1)
        excute_result = pipe.execute()
        stock_list_code = excute_result[0]

        for stock_i in range(len(stock_list_code)):
            stock_code = stock_list_code[stock_i].decode()
            stock_day_list = rlink.hkeys('stock_data_list:' + stock_code)
            if len(stock_day_list) == 0:
                continue
            for si in range(len(stock_day_list)):
                ori_date = stock_day_list[si].decode()
                if ori_date.find('-') != -1:
                    date_split = ori_date.split('-')
                    item_year = date_split[0]
                    item_month = date_split[1]
                    item_day = date_split[2]
                    cur_time_num = item_year + item_month + item_day
                    detail_data = rlink.hget('stock_data_list:' + stock_code, ori_date)
                    rlink.hset('stock_data_list:' + stock_code, cur_time_num, detail_data)
                    rlink.hdel('stock_data_list:' + stock_code, ori_date)
    except Exception as ex:
        print(ex)
        traceback.print_exc()
if __name__ == "__main__":
    temp_format_stock_data()
else:
    threads = [threading.Thread(target=temp_format_stock_data, args=())]
    threads[0].setDaemon(True)
    threads[0].start()
    

