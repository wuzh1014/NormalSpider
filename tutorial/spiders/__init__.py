import redis
from .AoiSpider import AoiSpider
from .Tool import Tool


rlink = redis.Redis(host=Tool.service_ip, port=6379, db=0)
pipe = rlink.pipeline()
pipe.multi()
aoi_key_len = rlink.llen(AoiSpider.redis_key)
if aoi_key_len == 0:
    rlink.lpush(AoiSpider.redis_key, AoiSpider.default_url)
    rlink.lpush(AoiSpider.redis_key, AoiSpider.default_url)
    # init_default_dict(pipe)
# rlink.delete("started_service:spider")
# rlink.delete("started_service:pull_string")
# rlink.delete("started_service:group_analysis")
# rlink.delete("started_service:full_stock")
# rlink.delete("started_service:set_lines")
# rlink.delete("started_service:learn_thread")
# scrapy runspider aoi_spider.py
