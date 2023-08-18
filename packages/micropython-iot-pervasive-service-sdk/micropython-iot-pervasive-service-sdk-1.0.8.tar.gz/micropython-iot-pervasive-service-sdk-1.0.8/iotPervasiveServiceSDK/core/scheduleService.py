from machine import Timer

# 最小间隔时间
MIN_INTERVAL_TIME = 50

'''
定时任务类
'''
class ScheduleService:
  tasks = []
  intervalTime = 1000

  def __init__(self,timer:Timer,tasks):
    self.tasks = tasks
    #intervalTime使用最大公约数来决定轮巡间隔
    intervalTime = len(tasks)>0 and tasks[0].intervalTime or 1
    for task in tasks:
      intervalTime = gcd(task.intervalTime,intervalTime)
    # 限幅  如果执行的间隔时间小于50毫秒则等于50毫秒
    self.intervalTime =intervalTime<50 and 50 or intervalTime
    # 定时中断初始化
    timer.init(period=intervalTime, mode=Timer.PERIODIC, callback=self.handleInterrupt)
    print("ScheduleService Init Success intervalTime")


  def handleInterrupt(self,timer):
    for task in self.tasks:
      task.nextRunTime = task.nextRunTime - self.intervalTime
      if(task.nextRunTime<=0):
        task.handleInterrupt()
        task.nextRunTime = task.intervalTime


# 最大公约数
def gcd(x, y):
  if y == 0:
    return x
  return gcd(y, x % y)


'''
任务基类，所有定时任务都需要继承此类
==注意== 此类所有时间单位均为ms ; 1s = 1000ms
'''
class ScheduleBase:
  #下次执行时间
  nextRunTime = 0
  #间隔时间
  intervalTime = 1000

  def __init__(self,intervalTime=1000) -> None:
    self.intervalTime =intervalTime<50 and 50 or intervalTime

  def setIntervalTime(self,intervalTime):
    self.intervalTime=intervalTime

  def handleInterrupt(self):
    print("please rewrite the handleInterrupt")