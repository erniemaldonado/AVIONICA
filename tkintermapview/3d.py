from vpython import *
from time import *
import numpy as np
import math
import serial
try:
     ad=serial.Serial('COM3',115200)
except:
     ad=[1,-1,1]
#time.sleep(1)


scene.range=5
toRad=2*np.pi/360
toDeg=1/toRad
scene.forward=vector(-1,-1,-1)

scene.width=600
scene.height=600

xarrow=arrow(lenght=2, shaftwidth=.1, color=color.red,axis=vector(1,0,0))
yarrow=arrow(lenght=2, shaftwidth=.1, color=color.green,axis=vector(0,1,0))
zarrow=arrow(lenght=4, shaftwidth=.1, color=color.blue,axis=vector(0,0,1))
frontArrow=arrow(length=4,shaftwidth=.1,color=color.purple,axis=vector(1,0,0))
upArrow=arrow(length=1,shaftwidth=.1,color=color.magenta,axis=vector(0,1,0))
sideArrow=arrow(length=2,shaftwidth=.1,color=color.orange,axis=vector(0,0,1))
cyli=cylinder(length=6,radio=2,pos=vector(0,0,0),axis=vector(0,1,0),color=color.white)
aleta0=box(length=2,width=1,height=.1,pos=vector(0,1,-1),axis=vector(0,1,.5),color=color.purple)
aleta1=box(length=2,width=1,height=.1, pos=vector(0,1,1),axis=vector(0,1,-.5),color=color.blue) 
aleta3=box(length=2,width=.1,height=1,pos=vector(1,1,0),axis=vector(-.3,.5,0),color=color.red)
aleta4=box(length=2,width=.1,height=1,pos=vector(-1,1,0),axis=vector(0.4,1,0),color=color.green)
con=cone(length=2, radio=2,pos=vector(0,6,0),axis=vector(0,1,0),color=color.purple)
myObj=compound([cyli,con,aleta1,aleta0,aleta3, aleta4])

#myObj=compound([cyli,con])
o=["-40,90,3","40,90,3","40,-90,3","40,-90,30"]
i=0
while (True):
#    while (ad.inWaiting()==0):
#         pass
   dataPacket=o[i%3]
   i+=1
  # dataPacket=str(dataPacket,'utf-8')
   splitPacket=dataPacket.split(",")
   roll=float(splitPacket[0])*toRad
   print(splitPacket[0])
   pitch=float(splitPacket[1])*toRad
   yaw=float(splitPacket[2])*toRad+np.pi
   print("Roll=",roll*toDeg," Pitch=",pitch*toDeg,"Yaw=",yaw*toDeg)

   rate(1)
   k=vector(cos(yaw)*cos(pitch), sin(pitch),sin(yaw)*cos(pitch))
   y=vector(0,1,0)
   s=cross(k,y)
   v=cross(s,k)

   frontArrow.axis=k
   sideArrow.axis=s
   upArrow.axis=v
   myObj.axis=k
   myObj.up=v
   sideArrow.length=2
   frontArrow.length=4
   upArrow.length=1