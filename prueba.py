import socket
import urllib.error
import urllib.request

try:
    response = urllib.request.urlopen(
        "http://example.com", timeout=0.5
    )  # 设置超时时间为10秒
    print(response.read())  # 打印服务器响应的内容
except urllib.error.URLError as e:
    if isinstance(e.reason, socket.timeout):
        print("请求超时")
