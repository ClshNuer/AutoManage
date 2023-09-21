# 乾颐堂 Python+Kali黑客全套教程

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

  ```
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

  ```
  https://<host>:<port>/api/api-version/xml
  ```

- 协议攻击

  ```
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

