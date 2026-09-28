#监控系统运行的状态
# 
import psutil
print(psutil.cpu_count())   # CPU逻辑数量
print(psutil.cpu_count(logical=False) )  # CPU物理核心
print(psutil.cpu_times())  # CPU使用时间
print(psutil.virtual_memory())  # 内存信息
print(psutil.swap_memory())  # 交换内存信息

print(psutil.virtual_memory())  # 内存使用率
print(psutil.disk_partitions())  # 磁盘分区信息
print(psutil.disk_usage('/'))  # 磁盘使用情况
print(psutil.disk_io_counters())  # 磁盘IO
print(psutil.net_io_counters())  # 网络IO

for x in range(10):
    print(psutil.cpu_percent(interval=1, percpu=True))  # CPU使用率
 