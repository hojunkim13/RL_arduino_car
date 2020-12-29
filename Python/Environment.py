import serial
import numpy as np

class Env:
    def __init__(self):
        PORT = 'COM7'
        BaudRate = 115200
        self.ARD = serial.Serial(PORT,BaudRate)
        self.clip_distance = 200. # unit: cm 
        self.dead_distance = 8.  
        self.safety_distance = 20.
        
        self.min_action = 125.
        self.max_action = 250.

    def Decode(self, A):
        A = str(A.decode())
        if A[0]=='S':                       #첫문자 검사
            if (len(A)==13):                #문자열 갯수 검사
                dstF=int(A[1:4])
                dstL=int(A[4:7])
                dstR=int(A[7:10])
                result= [dstF, dstL, dstR]
                return result
            else: 
                print ("Error_lack of number _ %d" %len(A))
        else :
            print ("Error_Wrong Signal")
            
        
    def Ardread(self):
            while self.ARD.readable():
                LINE = self.ARD.readline()
                data = self.Decode(LINE)
                #data range: (0. ~ 999.)  >> clip(0. ~ 200.) >> (0. ~ 1.)
                data = np.clip(data, 0., self.clip_distance) / self.clip_distance
                return data
            else: 
                print("읽기 실패 from _Ardread_")


    def step(self, action):
        done = False
        action_left, action_right = self.map_action(action)
        Trans="S" + action_left + action_right  #S+000+000
        Trans= Trans.encode('utf-8')
        self.ARD.write(Trans)
        
        data = self.Ardread()

        if min(data) < (self.dead_distance/self.clip_distance):
            done = True
            reward = -10
        
        elif (self.dead_distance/self.clip_distance) <= min(data) < (self.safety_distance/self.clip_distance):
            reward = 1

        elif min(data) >= (self.safety_distance/self.clip_distance):
            reward = 2

        return data, reward, done

    def restart(self):
        Trans="RRRRR"
        Trans= Trans.encode('utf-8')
        self.ARD.write(Trans)

    def end(self):
        Trans="EEEEE"
        Trans= Trans.encode('utf-8')
        self.ARD.write(Trans)

    def map_action(self, action):
        action = np.reshape(action, (2,))
        
        action = (action + 1.)
        action = action * (self.min_action / (self.max_action / self.min_action)) + self.min_action
        
        action_left = "{:+03.0f}".format(action[0])
        action_right = "{:+03.0f}".format(action[1])
        return action_left, action_right