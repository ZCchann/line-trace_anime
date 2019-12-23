# Line-trace_anime

这个脚本单纯凭个人兴趣编写 若您对本项目有修改意见欢迎提交



本脚本无法在windows主机上使用

若您想搭建本环境需要有一点linux主机操作经验

### 准备工作

使用line bot之前您需要准备

一台linux服务器

一个域名

注册一个cloudflare的账号

一个saucenao的账号 并复制api token

### 部署环境

当前线上机器人运行环境

centos6 x64

python 3.6.9

NGINX-1.16.0

### Line bot设置

创建bot可以参照这篇文章  https://www.oxxostudio.tw/articles/201701/line-bot.html 

bot创建完成后请复制" Channel access token "," Channel secret "至config.json文件

同时 请把服务器的域名填写至bot的" Webhook URL "部分 

https://youdomain.com/callback

若需要更改callback 请修改脚本第26行

### https设置

因line bot的webhook需要https 单独购买证书价格不划算 推荐使用cloudflare的免费ssl代理来达到效果

具体步骤可以参考以下文章

 https://www.jianshu.com/p/24d3800f597a 

### 部署步骤

1.请先查看本机python版本 若为python2请先安装python3并且设置环境变量

2.克隆本项目至电脑任意目录 并且创建/data/images文件夹

mkdir -p /data/images

若您需要更改这个图片存放目录请修改脚本第36行

3.设置config.json 填入各项需求参数

4.安装pipenv同时安装pipenv虚拟环境

```shell
pip3 install pipenv
pipenv install -r requirements.txt
```

5.运行脚本

```shell
pipenv run python3 trace_anime.py &
```

6.设置NGINX

centos请执行以下命令安装nginx

```shell
yum -y intsall nginx
#修改nginx配置文件 设置转发以及图片目录
vi /etc/nginx/nginx.conf
#修改http模块下默认的server部分
#修改位下列 将图片目录转发至80端口
    server {
        listen       80;
        server_name  localhost;
        location / {
            root   /data/images/;
            index  index.html index.htm;
            autoindex on;
            autoindex_exact_size off;
            autoindex_localtime on;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
#新增一个server 将python脚本默认5000端口转发至指定域名
server{
                listen       80;
                server_name  youdomain.com;   #请修改youdomain
                error_page   500 502 503 504  /50x.html;

        location / {
            proxy_pass   http://127.0.0.1:5000;
            proxy_set_header   Host             $host;
            proxy_redirect off;
            proxy_set_header   X-Real-IP        $remote_addr;
            proxy_set_header   X-Forwarded-For  $proxy_add_x_forwarded_for;
        }
        }

#然后reload nginx 启动 试用浏览器访问测试
#网页可以打开即可
```

## 问题、Bug 反馈、意见和建议

如果使用过程中遇到任何问题、Bug，或有其它意见或建议，欢迎提 [issue]( https://github.com/ZCchann/line-trace_anime/issues/new )。

