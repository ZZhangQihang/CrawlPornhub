# CrawlPornhub——下载P站热门视频(初步开发，持续优化)
<div align=center><img src="https://github.com/ZZhangQihang/CrawlPornhub/blob/master/images/QQ图片20191207195612.png" width="375" alt="logo"/></div>

## 环境要求
* `python3.X`
* `scrapy`
* `redis`
* 电脑可正常访问P站 (www.pornhub.com)
## 使用说明
#### 采集视频链接与下载视频为分开执行，采用redis进行传输 
#### 进入`pornhubSpider`文件夹,编辑`settings.py`配置文件
```Python
REDIS_HOST = 'xxx.xxx.xxx.xxx'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = ''
REDIS_KEY = 'downloads_msg'

SHARPNESS = '1080p'  # 1080p/720p/480p/240p 清晰度
MAX_PAGE = 5 # 爬取最大页数
```
#### 返回进入含有scrapy.cfg文件的文件夹中运行此项目
```Python
scrapy crawl pornhub
```
#### 启动多任务下载工具
```Python
python3 downloads_video.py
```
## 示例演示
### 爬取demo
![image](https://github.com/ZZhangQihang/CrawlPornhub/blob/master/images/start_spider.gif) 
### 下载视频demo
![image](https://github.com/ZZhangQihang/CrawlPornhub/blob/master/images/download_video.gif) 
## 声明
### 此仓库仅供学习交流,严禁用于商业用途!
### 有疑问请留issue或添加微信
<img src="https://github.com/ZZhangQihang/CrawlPornhub/blob/master/images/wx.jpg" width="375" alt="logo"/>

### 提醒：P站虽好，可不要贪撸哦！！！！！！

