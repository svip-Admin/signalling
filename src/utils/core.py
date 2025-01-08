import time


# 获取当前时间戳 到毫秒
def get_current_timestamp():
    tmp = time.time()
    timestamp = int(tmp * 1000)
    return timestamp

def get_current_time():
    tmp=time.time()
    timestamp=int(tmp)
    return timestamp

# 格式化时间戳
def get_format_time():
    tmp = time.time()
    time_array = time.localtime(int(tmp))
    format_time = time.strftime("%Y-%m-%d %H:%M:%S",time_array)
    return format_time