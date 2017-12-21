
#1.Introduction


It is written by django ,djangorestframwork,celery and so on.

As for database,I use MySQL ,Redis and Memcached.Of course,Memcache is used to be one cache.

Font End:bootstrap,jquery,datatables,vue and javascript.

The Blog provides several modules,such as article module,account management,dashboard etc.



demo:<a href="http://hbnnforever.cn">Demo</a>


#2.Function

blog,job,trip,account

#3.Project structure

<<<<<<< HEAD
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
=======

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

                      
After downloading,you should do like this below:                      
1.create your virutal enviroment using virtualenv                           
2.install python package all that needed:

      pip install -r requirements.txt in dailyblog/

3.modify config file,supervisor.conf,dailyblog.conf,gunicorn.conf.mainly the path.

4.enter virtual environment:source path/to/env/bin/activate

5.note your nginx configure file,you must create soft link: 
 
     ln -s path/to/dailyblog.conf /etc/nginx/site-enabled/dailyblog.conf 

6.start process:supervisord -c supervisor.conf

7.you can visit your web in browser:http://localhost/.

8.All above is necessary.



In fact ,you can deploy website using fabric ,I have wrote one fabfile.

but I do not add it on this code.

you can get it in my blog:<a href="http://hbnnforever.cn/article/deployweb.html">Web Deploy</a>


#5.Versions
  
   V2.1   change almost all view function to View class
   V1.1   first version


#5.Versions

 Version 2:

  2017-10-01

      1. Reconstruct code project,

      2. convert func view to class based view.


 Version 1:

   2016-05-03



#6.Author

Haibo Wang

Wechat & QQ:393993705

