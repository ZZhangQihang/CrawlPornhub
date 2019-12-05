# CrawlPornhub——下载P站热门视频(初步开发，持续优化)
## 声明
### 此仓库仅供学习交流,严禁用于商业用途!
### 提醒：P站虽好，可不要贪撸哦！
## 环境要求
* `python3.X`
* `scrapy`
* `redis`
* 电脑可正常访问P站 (www.pornhub.com)
## 使用说明
#### 采集视频链接与下载视频为分开执行，采用redis进行传输 
#### 进入`pornhubSpider`文件夹,编辑`settings.py`配置文件
```Python
REDIS_HOST = ''
REDIS_PORT = ''
REDIS_USERNAME = ''
REDIS_PASSWORD = ''
REDIS_DB = 0
```
#### 返回进入含有scrapy.cfg文件的文件夹中运行此项目
```Python
scrapy crawl pornhub
```
#### 启动多任务下载工具
```Python
python3 xxxxxx.py
```
## 示例演示
![baidu](http://www.baidu.com/img/bdlogo.gif "百度logo")  
