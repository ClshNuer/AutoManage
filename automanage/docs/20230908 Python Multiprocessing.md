# Python Multiprocessing

<!--last modify: 20230908-->



# 0x00 multiprocessing

```
import ipaddress
import multiprocessing

def scapy_ping_scan(self, network, maxPool = 30):
    net = ipaddress.ip_network(network)
    ip_list = [str(ip) for ip in net] # ip list

    with multiprocessing.Pool(maxPool) as pool: # 多进程进程池
        results = pool.map(self.scapy_ping, ip_list) # 关联函数与参数，且提取结果到 result
```

```
报错
current\lib\multiprocessing\connection.py", line 811, in _exhaustive_wait
    res = _winapi.WaitForMultipleObjects(L, False, timeout)
ValueError: need at most 63 handles, got a sequence of length 102

解决
这个报错是因为你在 Windows 系统上使用了多于 63 个进程的 multiprocessing.pool.Pool。这是一个 Windows 的限制，因为它使用了一个 API 函数 WaitForMultipleObjects，它最多只能等待 63 个对象。12

你可以尝试减少进程的数量，或者使用 concurrent.futures.ProcessPoolExecutor 来代替 multiprocessing.pool.Pool。23
```



