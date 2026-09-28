# requests。它是一个Python第三方库，处理URL资源特别方便。

import requests

r = requests.get('https://www.example.com')
print(r.status_code)
print(r.encoding)
print(r.cookies)
print(r.content)
print(r.headers['Content-Type'])
print(r.text)


r = requests.post('https://accounts.douban.com/login', data={'form_email': 'abc@example.com', 'form_password': '123456'})
print(r.status_code)

# requests默认使用application/x-www-form-urlencoded对POST数据编码。如果要传递JSON数据，可以直接传入json参数：
r = requests.post('https://accounts.douban.com/login', json={'form_email': 'abc@example.com', 'form_password': '123456'})
print(r.status_code)

