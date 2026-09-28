# datetime 是Python处理日期和时间的标准库。
from datetime import datetime, timezone
now = datetime.now() # 获取当前datetime
print(now) # 2020-03-16 21:19:10.123    

# 获取指定日期和时间

dt = datetime(2015, 4, 19, 12, 20) # 用指定日期时间创建datetime
print(dt) # 2015-04-19 12:20:00

# datetime转换为timestamp
dt.timestamp() # 把datetime转换为timestamp
print(dt.timestamp()) # 1429417200.0

# timestamp转换为datetime
print(datetime.fromtimestamp(1429417200.0)) # 2015-04-19 12:20:00   # 本地时间
print(datetime.utcfromtimestamp(1429417200.0)) # 2015-04-19 04:20:00   # UTC时间


# str转换为datetime
cday = datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
print(cday) # 2015-06-01 18:19:59   

# datetime转换为str
print(cday.strftime('%Y-%m-%d %H:%M:%S')) # 2015-06-01 18:19:59


# datetime加减
from datetime import timedelta
print(dt + timedelta(days=1)) # 2015-04-20 12:20:00
print(dt - timedelta(hours=1)) # 2015-04-19 11:20:00    
now = datetime.now()
print(now + timedelta(minutes=10)) # 10分钟后
print(now + timedelta(days=1, hours=2)) # 1天2小时后

# 本地时间转换为UTC时间
print(datetime.now().astimezone()) # 本地时间带时区信息
print(datetime.utcnow().astimezone()) # UTC时间带时区信息

# 时区转换
utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc) # 获取当前UTC时间，并强制设置时区为UTC+0:00
print(utc_dt) # 2020-03-16 13:19:10