# -*- coding: utf-8 -*-
import scrapy
import re
import logging
from pornhubSpider.items import PornhubspiderItem
from pornhubSpider.settings import SHARPNESS,MAX_PAGE


class PornhubSpider(scrapy.Spider):
    name = 'pornhub'

    def __init__(self):
        self.headers = {
            'Host': 'www.pornhub.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Cookie':'ua=2894fb4dbf964f58ccf3d2e4e372b316; platform_cookie_reset=pc; platform=pc; bs=ohabwajt5uqz8c5n8a1j5p1v4yjowr4m; ss=323761741477995184; RNLBSERVERID=ded6968; _ga=GA1.2.1341906648.1575389406; _gid=GA1.2.242123231.1575389406; performance_timing=video; RNKEY=74831677*78541087:422303240:3343060120:1; desired_username=kim201911sd%7C770701730%40qq.com; il=v1_c0ya0KW6LrE7FZUmQlWk0TbM2AjxVL7iUNXu_pGceExNTc1NDc3MzY1YnZzdGdtdEVDeWQ0ZzJKaUJpU25xN01oSHpBanQ3WVR3b1d0RTF2Ug..; expiredEnterModalShown=1; SMPop_0=1575469948476; _gat=1'
        }
        self.sharpness = SHARPNESS
        self.page = MAX_PAGE

    def start_requests(self):
        for i in range(1, MAX_PAGE):
            yield scrapy.Request(
                url="https://www.pornhub.com/video?o=ht&page={}".format(i),
                headers=self.headers,
                callback=self.video_url_parse
            )
        # yield scrapy.Request(
        #     url="https://www.pornhub.com/view_video.php?viewkey=ph5c136751eb8a9",
        #     headers=self.headers,
        #     callback=self.seed_url_parse
        # )

    def video_url_parse(self, response):
        video_li = response.xpath('//ul[@id="videoCategory"]/li')
        for video in video_li[2:]:
            video_url = 'https://www.pornhub.com/view_video.php?viewkey='+video.xpath('./@_vkey').extract_first()
            yield scrapy.Request(
                url=video_url,
                headers=self.headers,
                callback=self.seed_url_parse
            )

    def seed_url_parse(self, response):
        item = PornhubspiderItem()
        video_title = response.xpath('//div[@class="title-container"]/h1/span/text()').extract_first()
        seed_url_js = response.xpath('//div[@id="player"]/script[1]//text()').extract_first()
        seed_url = self.seed_url_js_parse(seed_url_js)
        if not seed_url:
            logging.error("Video address parsing is abnormal, please check {}".format(response.url))
        else:
            item['title'] = video_title
            item['video_url'] = response.url
            item['seed_url'] = seed_url
            yield item

    # 视频地址解析
    def seed_url_js_parse(self, js_str):
        kv_re = re.compile("var (.*?)\;")
        try:
            kv_li = kv_re.findall(js_str)
        except Exception as e:
            return False
        kv_dic = {}
        for kv in kv_li:
            kv = re.sub("\/\*.*?\*\/", "", kv.strip().replace("\" + \"", ""))
            kv = kv.split("=")
            if len(kv) != 2:
                kv[1] = '='.join(kv[1:])
            kv_dic[kv[0]] = kv[1].strip("\"")

        # 判断清晰度
        if SHARPNESS == "1080p":
            if 'quality_1080p' in kv_dic:
                seed_url = kv_dic['quality_1080p']
            elif 'quality_720p' in kv_dic:
                seed_url = kv_dic['quality_720p']
            elif 'quality_480p' in kv_dic:
                seed_url = kv_dic['quality_480p']
            else:
                seed_url = kv_dic['quality_240p']
        elif SHARPNESS == "720p":
            if 'quality_720p' in kv_dic:
                seed_url = kv_dic['quality_720p']
            elif 'quality_480p' in kv_dic:
                seed_url = kv_dic['quality_480p']
            else:
                seed_url = kv_dic['quality_240p']
        elif SHARPNESS == "480p":
            if 'quality_480p' in kv_dic:
                seed_url = kv_dic['quality_480p']
            else:
                seed_url = kv_dic['quality_240p']
        else:
            seed_url = kv_dic['quality_240p']
        seed_url_son_li = seed_url.split("+")
        seed_url = ''
        for seed_url_son in seed_url_son_li:
            seed_url += kv_dic[seed_url_son.strip()]
        return seed_url