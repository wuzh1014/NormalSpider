import redis
from .AoiSpider import AoiSpider
from .Tool import Tool


rlink = redis.StrictRedis(host=Tool.service_ip, port=6479, db=0, password='fuck-u-ass-hole-guy')
pipe = rlink.pipeline()
pipe.multi()
aoi_key_len = rlink.llen(AoiSpider.redis_key)
if aoi_key_len == 0:
    rlink.lpush(AoiSpider.redis_key, AoiSpider.default_url)
    rlink.lpush(AoiSpider.redis_key, AoiSpider.default_url)
