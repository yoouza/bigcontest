import time
import scrapy
import re
import datetime
import pandas as pd
import tqdm

class NewsFocusSpider(scrapy.Spider):

    name = "naver_news"

    # 경제일반
    url_format = 'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid2=263&sid1=101&date={0}&page={1}'
    # # 사회일반
    # url_format = 'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid2=257&sid1=102&date={0}&page={1}'
    # # 생활문화일반
    # url_format = 'https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid2=245&sid1=103&date={0}&page={1}'

    def __init__(self, start_date, end_date=None, time_break=0, **kwargs):

        super().__init__(**kwargs)

        if end_date is None:
            end_date = datetime.datetime.today().strftime("%Y%m%d")

        self.target_press = ['연합뉴스', '연합인포맥스', '이데일리', '매일경제', '한국경제', '아시아경제', '머니투데이']

        self.time_break = time_break
        self.start_date = datetime.datetime.strptime(str(start_date), "%Y%m%d")
        self.end_date = datetime.datetime.strptime(str(end_date), "%Y%m%d")
        self.cur_page = 1
        self.last_page = 0

        self.start_urls = [
            NewsFocusSpider.url_format.format(start_date, self.cur_page)
        ]
    def parse(self, response):

        # 이번페이지 크롤링
        all_articles = response.css('div#main_content div.list_body li dl')

        for article in all_articles:

            link = article.css('dt a::attr(href)').getall()[-1].strip()
            title = article.css('dt a::text').getall()[-1].strip()
            office = article.css('dd span.writing::text').get().strip()

            # 지정한 신문사만 크롤링
            if office in self.target_press:

                # 타임 브레이커
                time.sleep(self.time_break)

                # 데이터 요청
                request = scrapy.Request(link, callback=self.news_call)
                request.meta['press'] = office
                request.meta['date'] = self.start_date.strftime("%Y-%m-%d")
                request.meta['url'] = link
                request.meta['title'] = title

                yield request
                
            else:
                pass

        # 마지막 페이지 도착 이전까지
        try:
            last_page = re.search("(?!page=)[0-9]+$", response.css('div.paging a::attr(href)').getall()[-1]).group()
        except:
            # 페이지가 1페이지 밖에 없는 경우
            last_page = 1

        if self.cur_page < int(last_page):
            # 다음페이지 정보로 업데이트
            self.cur_page += 1
            # 다음페이지 호출
            str_date = self.start_date.strftime("%Y%m%d")
            next_page_url = NewsFocusSpider.url_format.format(str_date, str(self.cur_page))

            yield scrapy.Request(next_page_url, callback=self.parse)

        else:
            # 페이지 없음
            # 날짜 업데이트
            self.start_date += datetime.timedelta(days=1)
            if self.start_date <= self.end_date:
                # 신규 날짜로 1번 페이지 부터 재호출
                self.cur_page = 1
                str_date = self.start_date.strftime("%Y%m%d")
                next_date_url = NewsFocusSpider.url_format.format(str_date, str(self.cur_page))

                yield scrapy.Request(next_date_url, callback=self.parse)

            else:
                print("크롤링 종료")
                return

    def news_call(self, response):

        yield {
            'date': response.meta['date'],
            'office': response.meta['press'],
            'title': response.meta['title'],
            'url' : response.meta['url'],

            'text': re.sub('(\<[^\<\>]*\>)|▶[\s\S]+', ' ',
                           response.css('div#articleBodyContents').getall()[0]).strip().replace("// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}", "").replace('\n', ' ').replace(
                '\\', ' ').replace('\"', ' ').replace('\r', ' ').replace('\t', ' ').replace('  ', ' ').strip()
        }
