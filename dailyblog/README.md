
#1.Introduction

it is written by django ,celery,bootstrap,jquery,datatables,vue and javascript.
As for database,I use MySQL ,Redis and Memcached.Of course,Memcache is used to cache some resources.



demo:<a href="http://hbnnforever.cn">Demo</a>


#2.Function

blog,job,trip,account

#3.Project structure

├── apps
│   ├── account
│   ├── blog
│   ├── comment
│   ├── dashboard
│   ├── __init__.py
│   ├── job
│   └── trip
├── dailyblog
│   ├── celery.py
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── dailyblog.conf
├── docker-compose.yml
├── Dockerfile
├── gunicorn.conf
├── __init__.py
├── manage.py
├── media
│   ├── ckeditor
│   └── userimg
├── README.md
├── requirements.txt
├── restart.sh
├── static/
├── supervisor.conf
├── templates/
└── utils
    ├── baseclass/
    ├── cache.py
    ├── ....


Every app has iteself model,form ,view and url.

In additions,the api is edited in app:blog.


#4.Usage

The website should be deployed in Linux enviroment,os ubuntu.if you want to study
Django,the website provides a complete example
I use gunicorn_                        
After downloading,you should do like this below:                          10 
11 1.create your virutal enviroment using virtualenv                           
13 2.install python ppackage all that needed:pip install -r requirements.txt in daily    blog/
14 
15 3.modify config file,supervisor.conf,dailyblog.conf,gunicorn.conf.mainly the path.
16 
17 4.enter vrtual environment:source path/to/env/bin/activate
18 
19 5.note your nginx configure file,you must create soft link: ln -s path/to/dailyblo    g.conf /etc/nginx/site-enabled/dailyblog.conf 
20 
21 6.start process:supervisord -c supervisor.conf
22 
23 7.you can visit your web in browser:http://localhost/.
24 
25 8.All above is necessary.



#5.Versions



#6.Author

Haibo Wang

Wechat & QQ:393993705