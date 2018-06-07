# coding:utf-8
from tutorial.spiders.Tool import Tool


class SpiderUtil:

    @staticmethod
    def return_freq_word(pure_string):
        word_map = {}
        a_index = []
        for i in range(len(pure_string)):
            if pure_string[i] == ',':
                continue
            a_index.append(i)
        a_index.sort(key=lambda x: pure_string[x:])
        for i in range(len(a_index) - 1):
            Tool.compare_len(pure_string, a_index[i], a_index[i + 1], word_map)
        return word_map

    @staticmethod
    def clean_extract_word(response):
        try:
            text_list = response.xpath('body//div/text() | body//span/text() | body//p/text()').extract()
            if len(text_list) == 0:
                print('no body text')
                return False
            text_list = [item.strip() for item in text_list if item.strip() != '']
            response.pure_string = ','.join(text_list)
        except:
            print('no xpath')
            return False
        return True



if __name__ == "__main__":
    pass