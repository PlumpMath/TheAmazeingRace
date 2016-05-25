import direct.directbase.DirectStart
from direct.gui.DirectGui import *
from direct.task import Task

mytimer = DirectLabel()
mytimer.reparentTo(render)
mytimer.setY(20)
mytimer.setZ(5)


def timerTask(task):
  secondsTime = int(task.time)
  minutesTime = int(secondsTime/60)
  hoursTime = int(minutesTime/60)
  mytimer['text'] = "%02d:%02d:%02d" % (hoursTime, minutesTime%60, secondsTime%60)
  return Task.cont

taskMgr.add(timerTask, 'timerTask')

run()