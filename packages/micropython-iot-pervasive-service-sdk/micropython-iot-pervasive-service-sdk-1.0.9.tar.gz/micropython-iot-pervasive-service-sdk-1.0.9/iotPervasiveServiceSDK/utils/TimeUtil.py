import ntptime
import utime

# 同步并获取时间戳 （毫秒）
def getTimerMs():
  return getTimerS()*1000

# 同步并获取时间戳 （秒）
def getTimerS():
  return (utime.time()+946656000)

def setTime():
  try:
      # UTC+8偏移时间（秒）
      ntptime.NTP_DELTA = 3155644800  
        # ntp服务器，使用阿里服务器
      ntptime.host = 'ntp.ntsc.ac.cn'
        # 修改设备时间
      ntptime.settime()
  except:
      from machine import RTC
      rtc = RTC()
      rtc.datetime((2023, 3, 14, 1, 12, 48, 0, 0)) # set a specific date and time

def getNowFormatDatetime():

  return formatDatetime(utime.time())


def formatDatetime(timestamp):
    time_tuple = utime.localtime(timestamp)
    formatted_datetime = "{:04}-{:02}-{:02}T{:02}:{:02}:{:02}".format(
        time_tuple[0], time_tuple[1], time_tuple[2],
        time_tuple[3], time_tuple[4], time_tuple[5]
    )
    return formatted_datetime



