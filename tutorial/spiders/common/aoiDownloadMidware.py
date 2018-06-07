from scrapy.http import Response
class aoiDownloadMidware(object):
    def process_request(self, request, spider):
        return None
    def process_exception(self, request, exception, spider):
        return Response('127.0.0.1')

