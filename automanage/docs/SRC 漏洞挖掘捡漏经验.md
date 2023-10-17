# SRC 漏洞挖掘捡漏经验

<!--last modify: 20231016-->

## 0x00 视频 + 源码 + PDF

- videos
  - [7天教你挖掘SRC](https://www.bilibili.com/video/BV16e4y1s7ZH/?spm_id_from=333.337.search-card.all.click&vd_source=7f220845f0d7bc792a045e75a5ac8b8d)

- 推荐视频

  [SRC 漏洞挖掘捡漏经验](https://www.bilibili.com/video/BV16e4y1s7ZH?p=2&vd_source=7f220845f0d7bc792a045e75a5ac8b8d)



## 0x01 常见困境

### 0x01x000 Nginx

- 404 Not Found
- 403 Forbidden

并非站点没有文件没有内容，知识未配置根目录下的默认页面；可fuzz 接口目录、Google 语法检索、GitHub 检索相关信息

### 0x01x001 spring

- Whitelabel Error Page

  - [actuator 配置不当漏洞](https://www.freebuf.com/news/193509.html)：枚举执行器端点路径，对站点一级、二级、三级目录探测，查看目录下是否存在actuator 端点路径；
  - swagger 未授权访问接口：通过再路径后拼接swagger-ui.html 出现swagger 控制台且接口可用；

- 识别springboot 框架

  ```
  1. web 应用程序网页标签图标 favicon.ico
  2. springboot 框架默认报错页面 (Whitelabel Error Page)
  ```

- 枚举执行器端点路径

  ```
  写脚本进行目录探测
  ```

- [最大化利用漏洞](https://dvpnet.io/detail?id=814)

  ```
  1. 认证字段获取证明可影响其他用户
  	如/trace 路径获取用户认证字段信息，除基本HTTP 请求信息(时间戳、HTTP 头等)，还有用户token、cookie 字段；
  2. 数据库账户密码泄露
  	actuator 会监控站点mysql、mangodb 等数据库服务，可通过/env 路径获取服务配置信息拿下数据库
  3. git 项目地址泄露
  	/health 路径可探测到站点git 项目地址
  4. 后台用户账号密码泄露
  	/heapdump 路径，返回GZip 压缩hprof 堆转储文件会泄露站点内存信息；github 上相关工具解析拿到包括后台用户的账号密码等信息
  ```

### 0x01x002 weblogic

- Error 404 -Not Found

- [WeblogicScan](https://github.com/rabbitmask/WeblogicScan#weblogicscan)

### 0x01x003 tomcat

- put 漏洞、爆破弱口令、ajp 文件包含漏洞(部分站点配置多端口不同版本tomcat 服务可能更换ajp 协议端口8009)

```
存在漏洞的第三方组件:网上可找到的poc
登录框:任意注册、任意用户登录、任意密码重置、短信轰炸、邮箱轰炸、找回密码逻辑漏洞、验证码绕过、认证缺陷、用户名可穷举、验证码隐藏参数等等
敏感信息接口:越权访问、jsonp劫持、CORS跨域漏洞等等
js文件:未授权访问、敏感信息泄露、路径泄露、js硬编码密码等等
参数点:xss、sql注入、任意文件读取、任意文件下裁、遍历读取、url跳转漏洞、ssrf等等
可利用端口: ajp漏洞、redis未授权、Rsync末授权、mangodb未授权、FTP末授权、Memcache未授权、ZooKeeper未授权、jenskins未授权等等
报错页面:spring、tomcat、weblogic、nginx等等to
```

## 0x02 

### 0x02x000 APK 逆向信息收集

### 0x02x001 Github 信息收集到子域目录遍历

### 0x03x002 Github 信息收集 邮箱





