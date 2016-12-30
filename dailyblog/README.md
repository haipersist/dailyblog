
the website is used to record everying of me,including life,study,dairy etc.

it is written by django ,bootstrap,jquery and javascript.As for database,I use MySQL ,Redis and Memcahce.Of course,Memcache is used to cache some resources.

The website should be deployed in Linux enviroment,os ubuntu.if you want to study
Django,the website provides a complete example

I use gunicorn + supervisor + nginx + fabric,later,I want to use ansible and docker to deploy web

After downloading,you should do like this below:

1.create your virutal enviroment using virtualenv

2.install python package all that needed:pip install -r requirements.txt in dailyblog/

3.modify config file,supervisor.conf,dailyblog.conf,gunicorn.conf.mainly the path.

4.enter vrtual environment:source path/to/env/bin/activate

5.note your nginx configure file,you must create soft link: ln -s path/to/dailyblog.conf /etc/nginx/site-enabled/dailyblog.conf

6.start process:supervisord -c supervisor.conf

7.you can visit your web in browser:http://localhost/.

8.All above is necessary.

