# Python LXMl & Requests

<!--last modify: 20230803-->



## 0x00 XPath



```python
with requests.get(url, header) as response:
    response.encoding = 'utf-8'
    raw_data = response.text

time_frames = {3: 'overall', 4: 'month', 5: 'week', 6: 'day'}
movie_type = {1: 'film', 2: 'tv_series', 3: 'welfare', 4: 'anime', 5: 'variety_record'}

root_xpath = '/html/body/div/div[3]/div/div/div' # overall, month, week, day
sub_xpath = './div/div/div/div' # film, tv_series, welfare, anime, variety_record
rank_name_xpath = f'./div[1]/h3' # list name
top_xpath = f'./div[2]/a' # top name
href_xpath = './@href' # movie href link
top_num_xpath = f'./div[1]' # top 1-10
movie_name_xpath = f'./div[2]/span' # movie name
html = etree.HTML(raw_data)
root_elements = html.xpath(root_xpath)[2:]
movie_names = []
for root_element in root_elements:
    sub_elements = root_element.xpath(sub_xpath)
    for sub_element in sub_elements:
        rank_name_element = sub_element.xpath(rank_name_xpath)[0]
        rank_name = rank_name_element.text
        logger.debug(rank_name)

        top_elements = sub_element.xpath(top_xpath)
        for top_element in top_elements:
            href = top_element.xpath(href_xpath)[0]
            movie_url = SITE + href
            top_num_element = top_element.xpath(top_num_xpath)[0]
            top_num = top_num_element.text
            movie_name_element = top_element.xpath(movie_name_xpath)[0]
            movie_name = movie_name_element.text
            logger.debug(f"排名: {top_num}, 电影名: {movie_name}, URL: {movie_url}")

            movie_names += [movie_name]
```







## 0x01 Requests

- 可能网络原因

  ```python
  \lib\urllib\request.py", line 1351, in do_open
      raise URLError(err)
  urllib.error.URLError: <urlopen error [WinError 10060] 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。>
  ```

- 可能网络原因

  ```
  requests.exceptions.ConnectionError: ('Connection aborted.', ConnectionResetError(10054, '远程主机强迫关闭了一个现有的连接。', None, 10054, None))
  ```

  

- 发起一个完整的请求

  ```python
  with requests.get(url, header) as response:
      response.encoding = 'utf-8'
      raw_data = response.text
  ```

- ssl 模块引起的报错

  ```tex
  requests\adapters.py", line 517, in send
      raise SSLError(e, request=request)
  requests.exceptions.SSLError: HTTPSConnectionPool(host='wappass.baidu.com', port=443): Max retries exceeded with url: /static/captcha/tuxing.html?&logid=10856117453777667092&ak=c27bbc89afca0463650ac9bde68ebe06&backurl=https%3A%2F%2Fwww.baidu.com%2Fs%3Fwd%3Demail%2Bsite%253Awww.baidu.com%26pn%3D0&ext=x9G9QDmMXq%2FNo87gjGO0PyEfrpGvDFh50OHozGCUp%2FcYlU5PkiYt8z80Ez5p7Umpg1T9i%2F9aWxTqDk%2BHyX%2BPs0ChrtIMtQkyMCB6zc%2FRMjg2AIYB8EIGj5ZX8OLz1NaNu%2BrsP%2Fx0Ol1rbu5qES3n4agNjaVYFxC53U6q5godYvQ%3D&signature=f09c9cfe711a241f78b6dde280aa5d57&timestamp=1691202518 (Caused by SSLError(SSLError(1, '[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1007)')))
  ```

- 检测是否支持TLSv1.2 协议，python 从2.7.9 和3.4 开始支持TLSv1.2

  ```
  import ssl
  print(ssl.OPENSSL_VERSION)
  print(ssl.HAS_TLSv1_2)
  ```

- python 3.x 使用ssl 模块

  ```
  import ssl
  import requests
  requests.adapters.DEFAULT_RETRIES = 5
  s = requests.session()
  s.keep_alive = False
  s.mount('https://', requests.adapters.HTTPAdapter(max_retries=5))
  s.mount('http://', requests.adapters.HTTPAdapter(max_retries=5))
  s.get('https://www.baidu.com', verify=True, timeout=5)
  s.get('https://www.baidu.com', verify=True, timeout=5)
  s.get('https://www.baidu.com', verify=True, timeout=5)
  s.get('https://www.baidu.com', verify=True, timeout=5)
  s.get('https://www.baidu.com', verify=True, timeout=5)
  ```

  



## 0x02 LXML

### 0x02x000 xml.etree.ElementTree

```python
header = random.choice(HEADERS)
resp = requests.get(url, header)
resp.encoding = 'utf-8'
for i in range(3, 6 + 1):
    xpath = f'/html/body/div/div[3]/div/div/div[{i}]'
    for i_element in etree.HTML(resp.text).xpath(xpath):
        for j in range(1, 5 + 1):
            xpath = f'/div/div/div/div[{j}]'
            for j_element in i_element.xpath(xpath):

                for k in range(1, 2 + 1):
                    xpath = f'/div[{k}]'
                    for k_element in j_element.xpath(xpath):
                        print(element.attrib) # 列出element 中所有的属性
                        print(list(element)) # 列出element 的子节点
                        print(element.text) # 列出element 中所有的文本
```

`Element` 对象是 `xml.etree.ElementTree` 模块中的一个类，`element` 是一个 Element 对象，它还有以下常用方法：

- `element.get(key, default=None)`: 获取指定属性的值，如果属性不存在则返回默认值。

- `element.xpath(xpath_expression)`: 使用 XPath 表达式获取 Element 对象的子元素或属性。
- `element.getchildren()`: 获取 Element 对象的所有子元素。
- `element.getparent()`: 获取 Element 对象的父元素。
- `element.text`: 获取 Element 对象的文本内容。
- `element.tag`: 获取 Element 对象的标签名。
- `element.attrib`: 获取 Element 对象的属性字典。

[https://docs.python.org/3/library/xml.etree.elementtree.html#element-objects](https://docs.python.org/3/library/xml.etree.elementtree.html#element-objects)