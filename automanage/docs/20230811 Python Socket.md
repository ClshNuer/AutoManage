# Python Socket

<!--last modify: 20230811-->



## 0x00 socketserver

- 参考
  - docs
    - [socketserver](https://www.yii666.com/article/735690.html)


```python
import socketserver

class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # 处理客户端请求
        data = self.request.recv(1024)
        self.request.sendall(data.upper())

if __name__ == '__main__':
    # 创建 TCP 服务器
    server = socketserver.TCPServer(('localhost', 8888), MyHandler)
    # 启动服务器
    server.serve_forever()
```

基于 socket 的服务器，快速地创建 TCP 或 UDP 服务器，而无需深入了解底层的 socket 编程。`socketserver` 模块中最常用的类是 `TCPServer` 和 `UDPServer`，它们分别用于创建 TCP 和 UDP 服务器。此外，`socketserver` 还提供了一些处理器类，如 `BaseRequestHandler` 和 `StreamRequestHandler`，它们用于处理客户端请求。
