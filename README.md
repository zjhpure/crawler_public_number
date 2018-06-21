+ 此项目的详细介绍：https://www.jianshu.com/p/667f3668cd70
+ 项目中用到的android按键精灵源码：https://github.com/zjhpure/PublicNumberQuickMacro


## 环境准备
+ 一台爬虫服，python3环境，建议在ubuntu16.04下，不用再装一次python3
+ 一台代理服，root权限，anyproxy环境和pm2环境，要先装好npm和node才能装anyproxy，pm2是用来控制anyproxy的
+ 至少一台android手机/模拟器（公众号越多，android就需要越多，按键精灵的点击频率根据实际调整），装上微信，登录一个微信号（建议微信号进行认证，否则很快会被禁止登录），安装上按键精灵
+ 一个mysql数据库
+ 一个redis数据库
+ 如果机器不够，可以把爬虫服、代理服、mysql、redis都放在一台机器上


## 启动前准备
+ 下载项目，git clone https://github.com/zjhpure/crawler_public_number
+ 修改项目anyproxy目录下的rule_default.js文件第三四行，指定自己的redis
+ 复制项目anyproxy目录下的rule_default.js文件到代理服的/usr/local/lib/node_modules/anyproxy/lib下
+ 在代理服启动anyproxy，首次启动需要执行sudo pm2 start anyproxy -x -- -i，之后的启动执行sudo pm2 start anyproxy
+ 在代理服的/usr/local/lib/node_modules/anyproxy目录下，执行sudo npm install redis，以增加node的redis模块
+ 在代理服可以执行sudo pm2 list，查看是否启动anyproxy成功
+ 也可以在浏览器输入：代理服ip:8002，查看anyproxy运行情况
+ 复制项目anyproxy目录下的restart_anyproxy.py文件到代理服
+ 可以在代理服执行nohup python3 -u restart_anyproxy.py &，让anyproxy每天凌晨重启一次，因为anyproxy运行太久会变卡顿
+ android连接wifi指定anyproxy代理，代理地址是代理服ip，端口是8001
+ 在代理服ip:8002网址上，点击RootCA后，屏幕出现二维码和download按钮
+ 可以点击download直接下载到电脑然后复制到手机安装CA证书，或者用手机浏览器扫二维码安装CA证书，还可以用手机浏览器访问：代理服ip:8002/fetchCrtFile安装CA证书
+ android按键精灵配置获取公众号的接口的地址，在项目目录下的api.py文件中
+ android启动按键精灵
+ 手机/模拟器进入微信，这里测试两个公众号，关注公众号：pythonbuluo（Python程序员），python-china（Python中文社区）
+ 也可以在public_number表下自己添加其他的公众号，分别需要填上公众号微信号、公众号名称和公众号biz值
+ biz值的获取，点击公众号的历史消息，点击右上角按钮，点击复制链接，在一个地方查看这个链接
+ 链接像如下：https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5NzU0MzU0Nw==&scene=123&pass_ticket={pass_ticket值}
+ 那这里的biz值就是MjM5NzU0MzU0Nw==
+ 修改项目cfg目录下的cfg_test.py和cfg.prod.py文件，配置测服和正服，指定项目的mysql、redis和按键精灵接口的端口
+ 使用项目db目录下的db.sql文件生成数据库
+ 复制项目到测服和正服，目录放在/data/crawler/下，也可以放在其他地方，但是ctl_test.sh和ctl_test.sh的ROOT就要对应地改变


## 启动项目

#### 测服
+ 进入项目目录
+ 执行chmod +x ctl_test.sh，使ctl_test.sh可执行
+ 执行sh ctl_test.sh start_api，启动按键精灵接口
+ 执行sh ctl_test.sh start，启动爬虫
+ 手机/模拟器启动按键精灵，如果没有按键精灵，可以手动点击公众号的历史消息来测试
+ 项目运行后会在项目目录下生成nohup.out文件记录运行情况

#### 正服
+ 进入项目目录
+ 执行chmod +x ctl_prod.sh，使ctl_test.sh可执行
+ 执行sh ctl_prod.sh start_api，启动按键精灵接口
+ 执行sh ctl_prod.sh start，启动爬虫
+ 手机/模拟器启动按键精灵，如果没有按键精灵，可以手动点击公众号的历史消息来测试
+ 项目运行后会在项目目录下生成nohup.out文件记录运行情况

## 说明
+ 这里的微信文章内容和封面只是保存其链接
+ 如果真的要上线，要自己实现下载封面和文章内容，然后上传到云存储上（比如：七牛云）
+ android按键精灵的流程是：间隔一定时间请求一次按键精灵接口ip:/crawler/public_number/get_click_public_number，获取到公众号名字，然后点击公众号的历史消息