
import sys, serial, argparse, re
import numpy as np
from time import sleep
from collections import deque
import datetime

import matplotlib.pyplot as plt 
import matplotlib.animation as animation

def pressure(val):
    return (float(val) - 1638)*(1+1)/(14745-1638)*51.71484

# plot class
class AnalogPlot:
  # constr
  def __init__(self, strPort, maxLen, filename):
      # open serial port
      self.ser = serial.Serial(strPort, 9600)
      self.filename = filename

      self.ay = deque([0.0]*maxLen)
      self.az = deque([0.0]*maxLen)
      self.maxLen = maxLen

  def writeToFile(self, data):
    with open(self.filename, "a") as myfile:
        strs = map(lambda x: str(x), data)
        myfile.write(";".join(strs)+"\n")


  # add to buffer
  def addToBuf(self, buf, val):
      if len(buf) < self.maxLen:
          buf.append(val)
      else:
          buf.pop()
          buf.appendleft(val)

  # add data
  def add(self, data):
      self.addToBuf(self.ay, data[1])
      self.addToBuf(self.az, data[2])

  # update plot
  def update(self, frameNum, a1, a2):
      try:
        line = self.ser.readline()
        line = line.replace("\n","")
        val1 = re.match('.*_(\d+).+',line).group(1)
        val2 = re.match('.+--(\d+).+',line).group(1)
        data = [frameNum,pressure(val1),pressure(val2)]
        print data
        self.writeToFile(data)
        self.add(data)
        a1.set_data(range(self.maxLen), self.ay)
        a2.set_data(range(self.maxLen), self.az)
      except KeyboardInterrupt:
          print('exiting')
      
      return a1, 

  # clean up
  def close(self):
      # close serial
      self.ser.flush()
      self.ser.close()    

# main() function
def main():
  # filename
  filename = datetime.datetime.now().isoformat() + ".txt"
  # create parser
  parser = argparse.ArgumentParser(description="LDR serial")
  # add expected arguments
  parser.add_argument('--port', dest='port', required=True)

  
  strPort = '/dev/cu.usbserial-AL00ERYJ'

  print('reading from serial port %s...' % strPort)

  # plot parameters
  analogPlot = AnalogPlot(strPort, 100, filename)

  print('plotting data...')

  # set up animation
  fig = plt.figure()
  ax = plt.axes(xlim=(0, 100), ylim=(-10, 50))
  a1, = ax.plot([], [])
  a2, = ax.plot([], [])
  anim = animation.FuncAnimation(fig, analogPlot.update, 
                                 fargs=(a1, a2), 
                                 interval=50)

  # show plot
  plt.show()
  
  # clean up
  analogPlot.close()

  print('exiting.')
  

# call main
if __name__ == '__main__':
  main()